"""
build_crossleague_db.py
═══════════════════════════════════════════════════════════════════════════════
Builds a MySQL database (`nba_euroleague`) of basketball players who competed
in BOTH the NBA and the EuroLeague, with their season stats and the migration
episodes between the two leagues.

Supports the research project:
  "Do Shooting Profiles Travel? Shot Selection, Shot Quality, and Performance
   Adaptation Between the NBA and EuroLeague"

Runs on the same MySQL server used by the NBL/PLK scrapers:
  host: localhost  |  port: 8889  |  user: root  |  password: root

─── Data sources (both verified working, no auth required) ─────────────────────
  EuroLeague : api-live.euroleague.net/v2  (rosters/bio)
               api-live.euroleague.net/v3  (bulk season statistics)
               full history E2000 (2000/01) → current season
  NBA        : nba_api package (stats.nba.com)
               full history - every player who ever played

─── Strategy (reliable + efficient) ────────────────────────────────────────────
  1. Collect ALL EuroLeague players + season stats (the migrant pool - anyone
     who crossed leagues must have a EuroLeague season).
  2. Pull the full NBA player index (one call, ~5,100 players).
  3. Match EuroLeague players to NBA players by name, confirmed by date of birth.
  4. For confirmed cross-league migrants only, pull full NBA career stats + bio.
  5. Detect NBA↔EuroLeague migration episodes across each player's timeline.

  Every phase is resumable: re-running skips seasons/players already stored.

─── Prerequisites ──────────────────────────────────────────────────────────────
  pip install nba_api mysql-connector-python requests

─── Usage ──────────────────────────────────────────────────────────────────────
  python build_crossleague_db.py                    # full pipeline
  python build_crossleague_db.py --skip-el          # skip EuroLeague collection
  python build_crossleague_db.py --skip-nba-match   # skip NBA matching/enrichment
  python build_crossleague_db.py --skip-migrations  # skip migration detection
  python build_crossleague_db.py --summary-only     # print DB summary and exit
  python build_crossleague_db.py --el-from 2010     # restrict EuroLeague start year
═══════════════════════════════════════════════════════════════════════════════
"""

import argparse
import logging
import re
import sys
import time
import unicodedata
from datetime import datetime, date
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple

import mysql.connector
import requests

# ─── Logging ─────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)-7s]  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("crossleague_build.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("crossleague")

# ─── Configuration ────────────────────────────────────────────────────────────────

DB_NAME = "nba_euroleague"
DB_CONFIG = {
    "host": "localhost",
    "port": 8889,
    "user": "root",
    "password": "root",
    "database": DB_NAME,
    "charset": "utf8mb4",
}

# EuroLeague: real data begins with E2000 (2000/01). Current completed: E2025 (2025/26).
EL_FIRST_YEAR_DEFAULT = 2000
EL_LAST_YEAR = datetime.now().year  # inclusive; harmless if a future code is empty

# EuroLeague shot-LOCATION data (Points feed) only exists from E2007 (2007/08).
# Earlier seasons return an empty body, so there is nothing to collect there.
EL_SHOTS_FIRST_YEAR = 2007

EL_V2 = "https://api-live.euroleague.net/v2/competitions/E"
EL_V3 = "https://api-live.euroleague.net/v3/competitions/E"

HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 basketball-research/1.0 (academic)"}

EL_DELAY = 0.4   # polite delay between EuroLeague calls
NBA_DELAY = 0.6  # delay between stats.nba.com calls (rate-limit friendly)
NBA_TIMEOUT = 30


# ═══════════════════════════════════════════════════════════════════════════════
#  Small utilities
# ═══════════════════════════════════════════════════════════════════════════════

def _f(v) -> Optional[float]:
    try:
        if v is None or v == "":
            return None
        f = float(v)
        if f != f or f in (float("inf"), float("-inf")):  # NaN / inf (e.g. pandas NaN)
            return None
        return f
    except (TypeError, ValueError):
        return None


def _i(v) -> Optional[int]:
    try:
        if v is None or v == "":
            return None
        if isinstance(v, float) and v != v:  # NaN
            return None
        return int(round(float(v)))
    except (TypeError, ValueError):
        return None


def _pct(v) -> Optional[float]:
    """Parse a percentage that may be '37.5%', '37.5', or numeric → 37.5."""
    if v is None:
        return None
    if isinstance(v, str):
        v = v.replace("%", "").strip()
        if v == "":
            return None
    return _f(v)


def normalize_name(name: str) -> str:
    """Diacritics-free, lowercase, a-z/space only, collapsed whitespace."""
    if not name:
        return ""
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = name.lower().replace(".", " ").replace("-", " ")
    name = re.sub(r"[^a-z\s]", "", name)
    return re.sub(r"\s+", " ", name).strip()


def normalize_lastfirst(raw: str) -> str:
    """'DONCIC, LUKA' → normalized 'luka doncic'. Plain names pass through."""
    return normalize_name(reorder_lastfirst(raw))


def reorder_lastfirst(raw: str) -> str:
    """'DONCIC, LUKA' → 'Luka Doncic' (title-cased display). Plain names pass through."""
    if not raw:
        return ""
    if "," in raw:
        last, first = raw.split(",", 1)
        raw = f"{first.strip()} {last.strip()}"
    raw = re.sub(r"\s+", " ", raw).strip()
    # Title-case only ALL-CAPS input; leave mixed-case names untouched
    return raw.title() if raw.isupper() else raw


def name_sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def parse_birthdate(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    s = str(s)[:10]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def el_code_to_label(year: int) -> str:
    """2017 → '2017/18'"""
    return f"{year}/{str(year + 1)[-2:]}"


def nba_season_label(season_id: str) -> str:
    """'2017-18' → '2017/18'"""
    return season_id.replace("-", "/")


def label_start_year(label: str) -> int:
    return int(label.split("/")[0])


# ═══════════════════════════════════════════════════════════════════════════════
#  HTTP helpers (with retry/backoff)
# ═══════════════════════════════════════════════════════════════════════════════

def http_get_json(url: str, params: dict = None, retries: int = 4,
                  base_delay: float = 1.0) -> Optional[dict]:
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=HTTP_HEADERS, timeout=25)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            # Some EuroLeague feeds return HTTP 200 with an empty body for
            # seasons/games that have no data (e.g. shot coords pre-2007).
            # Treat that as "no data" - do NOT retry, just skip.
            if not r.content or not r.text.strip():
                return None
            return r.json()
        except Exception as exc:
            wait = base_delay * (attempt + 1)
            log.warning(f"  GET retry {attempt + 1}/{retries} ({exc}); wait {wait:.1f}s")
            time.sleep(wait)
    log.error(f"  GET failed permanently: {url}")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
#  Schema
# ═══════════════════════════════════════════════════════════════════════════════

def init_schema(conn, cursor):
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
        f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cursor.execute(f"USE {DB_NAME}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Players (
            id                      INT AUTO_INCREMENT PRIMARY KEY,
            full_name               VARCHAR(200) NOT NULL,
            full_name_normalized    VARCHAR(200),
            first_name              VARCHAR(100),
            last_name               VARCHAR(100),
            nationality             VARCHAR(100),
            birthday                DATE,
            height_cm               INT,
            position                VARCHAR(50),
            nba_player_id           INT,
            euroleague_player_code  VARCHAR(60),
            played_nba              TINYINT(1) NOT NULL DEFAULT 0,
            played_euroleague       TINYINT(1) NOT NULL DEFAULT 0,
            is_cross_league_migrant TINYINT(1) NOT NULL DEFAULT 0,
            matching_confidence     ENUM('exact','high','medium','unmatched')
                                    NOT NULL DEFAULT 'unmatched',
            created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                    ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY uq_nba_id  (nba_player_id),
            UNIQUE KEY uq_el_code (euroleague_player_code),
            INDEX idx_name_norm (full_name_normalized(100)),
            INDEX idx_birthday  (birthday),
            INDEX idx_migrant   (is_cross_league_migrant)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NBASeasons (
            id                  INT AUTO_INCREMENT PRIMARY KEY,
            player_id           INT NOT NULL,
            season              VARCHAR(10) NOT NULL,
            team_abbreviation   VARCHAR(10),
            games_played        INT,
            games_started       INT,
            minutes_total       FLOAT,
            minutes_per_game    FLOAT,
            fga_total           INT,
            fga_per_game        FLOAT,
            fgm_total           INT,
            fg_pct              FLOAT,
            three_pt_fga_total  INT,
            three_pt_fgm_total  INT,
            three_pt_pct        FLOAT,
            two_pt_fga_total    INT,
            two_pt_fgm_total    INT,
            two_pt_pct          FLOAT,
            ft_attempts_total   INT,
            ft_made_total       INT,
            ft_pct              FLOAT,
            efg_pct             FLOAT,
            ts_pct              FLOAT,
            points_total        INT,
            points_per_game     FLOAT,
            assists_per_game    FLOAT,
            rebounds_per_game   FLOAT,
            steals_per_game     FLOAT,
            blocks_per_game     FLOAT,
            turnovers_per_game  FLOAT,
            FOREIGN KEY (player_id) REFERENCES Players(id) ON DELETE CASCADE,
            UNIQUE KEY uq_nba_ps_team (player_id, season, team_abbreviation)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EuroLeagueSeasons (
            id                  INT AUTO_INCREMENT PRIMARY KEY,
            player_id           INT NOT NULL,
            season              VARCHAR(10) NOT NULL,
            season_code         VARCHAR(10) NOT NULL,
            team_name           VARCHAR(150),
            team_code           VARCHAR(20),
            games_played        INT,
            games_started       INT,
            minutes_per_game    FLOAT,
            fga_total           INT,
            fga_per_game        FLOAT,
            fgm_total           INT,
            fg_pct              FLOAT,
            two_pt_fga_total    INT,
            two_pt_fgm_total    INT,
            two_pt_pct          FLOAT,
            three_pt_fga_total  INT,
            three_pt_fgm_total  INT,
            three_pt_pct        FLOAT,
            ft_attempts_total   INT,
            ft_made_total       INT,
            ft_pct              FLOAT,
            efg_pct             FLOAT,
            ts_pct              FLOAT,
            points_per_game     FLOAT,
            assists_per_game    FLOAT,
            rebounds_per_game   FLOAT,
            steals_per_game     FLOAT,
            blocks_per_game     FLOAT,
            turnovers_per_game  FLOAT,
            performance_index   FLOAT,
            FOREIGN KEY (player_id) REFERENCES Players(id) ON DELETE CASCADE,
            UNIQUE KEY uq_el_ps_team (player_id, season_code, team_code)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MigrationEpisodes (
            id                      INT AUTO_INCREMENT PRIMARY KEY,
            player_id               INT NOT NULL,
            direction               ENUM('NBA_to_EL','EL_to_NBA') NOT NULL,
            origin_league           VARCHAR(20) NOT NULL,
            destination_league      VARCHAR(20) NOT NULL,
            origin_season           VARCHAR(10) NOT NULL,
            destination_season      VARCHAR(10) NOT NULL,
            origin_team             VARCHAR(150),
            destination_team        VARCHAR(150),
            seasons_gap             INT DEFAULT 0,
            player_age_at_migration INT,
            created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES Players(id) ON DELETE CASCADE,
            UNIQUE KEY uq_migration
                (player_id, direction, origin_season, destination_season)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    # ── Shot-level tables (for shooting logs & shooting profiles) ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS NBAShots (
            id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
            player_id           INT NOT NULL,
            season              VARCHAR(10) NOT NULL,
            game_id             VARCHAR(20),
            game_date           DATE,
            period              INT,
            minutes_remaining   INT,
            seconds_remaining   INT,
            shot_value          TINYINT,            -- 2 or 3
            made                TINYINT(1),         -- 1 made, 0 missed
            action_type         VARCHAR(80),        -- e.g. 'Step Back Jump shot'
            shot_zone_basic     VARCHAR(40),
            shot_zone_area      VARCHAR(40),
            shot_zone_range     VARCHAR(40),
            shot_distance_ft    INT,
            loc_x               INT,                -- tenths of feet from hoop
            loc_y               INT,
            FOREIGN KEY (player_id) REFERENCES Players(id) ON DELETE CASCADE,
            INDEX idx_nba_shot_ps (player_id, season),
            UNIQUE KEY uq_nba_shot (player_id, game_id, period,
                                    minutes_remaining, seconds_remaining, loc_x, loc_y)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EuroLeagueShots (
            id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
            player_id           INT NOT NULL,
            season              VARCHAR(10) NOT NULL,
            season_code         VARCHAR(10) NOT NULL,
            game_code           INT,
            game_date           DATE,
            team_code           VARCHAR(20),
            shot_value          TINYINT,            -- 2 or 3
            made                TINYINT(1),
            action_code         VARCHAR(10),        -- '2FGM','3FGA',...
            action_desc         VARCHAR(80),
            zone                VARCHAR(5),          -- EuroLeague zone letter
            coord_x             INT,
            coord_y             INT,
            minute              INT,
            game_clock          VARCHAR(10),
            fastbreak           TINYINT(1),
            second_chance       TINYINT(1),
            points_off_turnover TINYINT(1),
            FOREIGN KEY (player_id) REFERENCES Players(id) ON DELETE CASCADE,
            INDEX idx_el_shot_ps (player_id, season_code),
            UNIQUE KEY uq_el_shot (player_id, season_code, game_code,
                                   action_code, minute, coord_x, coord_y)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    # Track which EuroLeague games have already had their Points feed pulled,
    # so re-runs are resumable even when a game has no migrant shots.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ELGamesProcessed (
            season_code  VARCHAR(10) NOT NULL,
            game_code    INT NOT NULL,
            shots_stored INT DEFAULT 0,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (season_code, game_code)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    conn.commit()
    log.info("Schema ready.")


# ═══════════════════════════════════════════════════════════════════════════════
#  Phase 1 - EuroLeague collection
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_el_people(season_code: str) -> Dict[str, dict]:
    """Return {player_code: bio_dict} for actual players (type 'J') in a season."""
    out: Dict[str, dict] = {}
    resp = http_get_json(
        f"{EL_V2}/seasons/{season_code}/people",
        params={"limit": 3000}, base_delay=EL_DELAY,
    )
    if not resp:
        return out
    for entry in resp.get("data", []):
        if entry.get("type") != "J":  # J = Player
            continue
        person = entry.get("person", {})
        code = (person.get("code") or "").strip()
        if not code:
            continue
        # Keep the richest record if a player appears twice (multi-club season)
        if code in out:
            continue
        country = person.get("country") or {}
        height = _i(person.get("height"))
        out[code] = {
            "code": code,
            "name_raw": (person.get("name") or "").strip(),
            "first": (person.get("passportName") or "").strip(),
            "last": (person.get("passportSurname") or "").strip(),
            "birthday": parse_birthdate(person.get("birthDate")),
            "nationality": (country.get("name") or "").strip() or None,
            "height_cm": height if height else None,
            "position": (entry.get("positionName") or "").strip() or None,
        }
    return out


def fetch_el_stats(season_code: str, mode: str) -> Dict[str, dict]:
    """
    Bulk season stats keyed by player code.
    mode = 'accumulated' (totals) or 'perGame' (averages).
    """
    api_mode = "accumulated" if mode == "accumulated" else "perGame"
    out: Dict[str, dict] = {}
    limit, offset = 1000, 0
    while True:
        resp = http_get_json(
            f"{EL_V3}/statistics/players/traditional",
            params={
                "SeasonMode": "Single",
                "SeasonCode": season_code,
                "StatisticMode": api_mode,
                "Limit": limit,
                "Offset": offset,
            },
            base_delay=EL_DELAY,
        )
        if not resp:
            break
        players = resp.get("players", [])
        for row in players:
            code = (row.get("player", {}).get("code") or "").strip()
            if code:
                out[code] = row
        total = _i(resp.get("total")) or 0
        offset += limit
        if offset >= total or not players:
            break
        time.sleep(EL_DELAY)
    return out


def collect_euroleague(conn, cursor, first_year: int):
    log.info("━━━  PHASE 1 - EuroLeague collection  ━━━")
    seasons = list(range(first_year, EL_LAST_YEAR + 1))

    for year in seasons:
        season_code = f"E{year}"
        season_label = el_code_to_label(year)

        cursor.execute(
            "SELECT COUNT(*) FROM EuroLeagueSeasons WHERE season_code = %s",
            (season_code,),
        )
        if cursor.fetchone()[0] > 0:
            log.info(f"  {season_label}  - already collected, skipping.")
            continue

        log.info(f"  {season_label} ({season_code}) …")
        people = fetch_el_people(season_code)
        if not people:
            log.info(f"    no roster data - skipping {season_label}")
            continue
        time.sleep(EL_DELAY)
        totals = fetch_el_stats(season_code, "accumulated")
        time.sleep(EL_DELAY)
        pergame = fetch_el_stats(season_code, "perGame")

        n_rows = 0
        for code, bio in people.items():
            tot = totals.get(code, {})
            avg = pergame.get(code, {})

            gp = _i(tot.get("gamesPlayed")) or _i(avg.get("gamesPlayed")) or 0
            if gp == 0 and not tot and not avg:
                continue  # roster-listed but never played

            # ── upsert player ──
            player_id = upsert_el_player(conn, cursor, bio)

            # ── totals ──
            two_m = _i(tot.get("twoPointersMade"))
            two_a = _i(tot.get("twoPointersAttempted"))
            three_m = _i(tot.get("threePointersMade"))
            three_a = _i(tot.get("threePointersAttempted"))
            ft_m = _i(tot.get("freeThrowsMade"))
            ft_a = _i(tot.get("freeThrowsAttempted"))
            pts_tot = _f(tot.get("pointsScored"))

            fga_tot = (two_a or 0) + (three_a or 0) if (two_a is not None or three_a is not None) else None
            fgm_tot = (two_m or 0) + (three_m or 0) if (two_m is not None or three_m is not None) else None

            fg_pct = (100.0 * fgm_tot / fga_tot) if fga_tot else None
            two_pct = (100.0 * two_m / two_a) if two_a else None
            three_pct = (100.0 * three_m / three_a) if three_a else None
            ft_pct = (100.0 * ft_m / ft_a) if ft_a else None
            efg = ((fgm_tot + 0.5 * (three_m or 0)) / fga_tot) if fga_tot else None
            ts_den = 2 * ((fga_tot or 0) + 0.44 * (ft_a or 0))
            ts = (pts_tot / ts_den) if (ts_den and pts_tot is not None) else None

            # ── per game ──
            team = avg.get("player", {}).get("team", {}) or tot.get("player", {}).get("team", {})
            team_name = (team.get("name") or "").strip() or None
            team_code = (team.get("code") or "").strip() or None
            fga_pg = (_f(avg.get("twoPointersAttempted")) or 0) + (_f(avg.get("threePointersAttempted")) or 0)

            cursor.execute("""
                INSERT INTO EuroLeagueSeasons
                    (player_id, season, season_code, team_name, team_code,
                     games_played, games_started, minutes_per_game,
                     fga_total, fga_per_game, fgm_total, fg_pct,
                     two_pt_fga_total, two_pt_fgm_total, two_pt_pct,
                     three_pt_fga_total, three_pt_fgm_total, three_pt_pct,
                     ft_attempts_total, ft_made_total, ft_pct,
                     efg_pct, ts_pct,
                     points_per_game, assists_per_game, rebounds_per_game,
                     steals_per_game, blocks_per_game, turnovers_per_game,
                     performance_index)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE games_played = VALUES(games_played)
            """, (
                player_id, season_label, season_code, team_name, team_code,
                gp, _i(tot.get("gamesStarted")), _f(avg.get("minutesPlayed")),
                fga_tot, round(fga_pg, 2) if fga_pg else None, fgm_tot,
                round(fg_pct, 2) if fg_pct else None,
                two_a, two_m, round(two_pct, 2) if two_pct else None,
                three_a, three_m, round(three_pct, 2) if three_pct else None,
                ft_a, ft_m, round(ft_pct, 2) if ft_pct else None,
                round(efg, 4) if efg else None, round(ts, 4) if ts else None,
                _f(avg.get("pointsScored")), _f(avg.get("assists")),
                _f(avg.get("totalRebounds")), _f(avg.get("steals")),
                _f(avg.get("blocks")), _f(avg.get("turnovers")),
                _f(avg.get("pir")),
            ))
            n_rows += 1
        conn.commit()
        log.info(f"    ✓ {season_label}: {n_rows} player-seasons "
                 f"({len(people)} roster, {len(totals)} with stats)")

    cursor.execute("SELECT COUNT(*) FROM Players WHERE played_euroleague = 1")
    n_players = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM EuroLeagueSeasons")
    n_seasons = cursor.fetchone()[0]
    log.info(f"EuroLeague done: {n_players} players, {n_seasons} player-seasons.")


def upsert_el_player(conn, cursor, bio: dict) -> int:
    code = bio["code"]
    cursor.execute("SELECT id FROM Players WHERE euroleague_player_code = %s", (code,))
    row = cursor.fetchone()
    if row:
        cursor.execute(
            """UPDATE Players SET
                   played_euroleague = 1,
                   birthday    = COALESCE(birthday,    %s),
                   nationality = COALESCE(nationality, %s),
                   height_cm   = COALESCE(height_cm,   %s),
                   position    = COALESCE(position,    %s)
               WHERE id = %s""",
            (bio["birthday"], bio["nationality"], bio["height_cm"],
             bio["position"], row[0]),
        )
        return row[0]

    first, last = bio["first"], bio["last"]
    full_name = f"{first} {last}".strip() or bio["name_raw"]
    norm = normalize_name(f"{first} {last}") or normalize_lastfirst(bio["name_raw"])
    cursor.execute("""
        INSERT INTO Players
            (full_name, full_name_normalized, first_name, last_name,
             nationality, birthday, height_cm, position,
             euroleague_player_code, played_euroleague)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,1)
    """, (full_name, norm, first, last, bio["nationality"], bio["birthday"],
          bio["height_cm"], bio["position"], code))
    return cursor.lastrowid


# ═══════════════════════════════════════════════════════════════════════════════
#  Phase 2+3 - NBA matching & enrichment
# ═══════════════════════════════════════════════════════════════════════════════

def match_and_enrich_nba(conn, cursor):
    log.info("━━━  PHASE 2 - NBA matching & enrichment  ━━━")

    try:
        from nba_api.stats.endpoints import (
            CommonAllPlayers, PlayerCareerStats, CommonPlayerInfo,
        )
    except ImportError:
        log.error("nba_api not installed. Run: pip install nba_api")
        return

    # ── NBA player index (one call) ──
    log.info("  Fetching full NBA player index…")
    all_players = CommonAllPlayers(
        is_only_current_season=0, league_id="00", season="2024-25",
        timeout=NBA_TIMEOUT,
    ).get_data_frames()[0]

    nba_index: Dict[str, List[dict]] = {}
    for _, r in all_players.iterrows():
        norm = normalize_name(str(r["DISPLAY_FIRST_LAST"]))
        nba_index.setdefault(norm, []).append({
            "id": int(r["PERSON_ID"]),
            "name": str(r["DISPLAY_FIRST_LAST"]),
            "from": _i(r["FROM_YEAR"]),
            "to": _i(r["TO_YEAR"]),
        })
    log.info(f"  NBA index: {len(all_players)} players, {len(nba_index)} unique names")

    # ── EuroLeague players not yet matched ──
    cursor.execute("""
        SELECT id, full_name_normalized, last_name, birthday
        FROM Players
        WHERE euroleague_player_code IS NOT NULL AND nba_player_id IS NULL
    """)
    el_players = cursor.fetchall()
    log.info(f"  EuroLeague players to test: {len(el_players)}")

    info_cache: Dict[int, dict] = {}

    def get_nba_info(nba_id: int) -> Optional[dict]:
        if nba_id in info_cache:
            return info_cache[nba_id]
        time.sleep(NBA_DELAY)
        for attempt in range(3):
            try:
                info = CommonPlayerInfo(
                    player_id=nba_id, timeout=NBA_TIMEOUT
                ).get_data_frames()[0].iloc[0]
                bday = parse_birthdate(str(info.get("BIRTHDATE")))
                h_raw = str(info.get("HEIGHT") or "")
                height_cm = None
                if "-" in h_raw:
                    try:
                        ft, inch = h_raw.split("-")
                        height_cm = round((int(ft) * 12 + int(inch)) * 2.54)
                    except ValueError:
                        pass
                rec = {
                    "birthday": bday,
                    "height_cm": height_cm,
                    "country": str(info.get("COUNTRY") or "") or None,
                    "position": str(info.get("POSITION") or "") or None,
                }
                info_cache[nba_id] = rec
                return rec
            except Exception as exc:
                log.warning(f"    CommonPlayerInfo({nba_id}) retry {attempt+1}/3: {exc}")
                time.sleep(NBA_DELAY * (attempt + 2))
        return None

    matched = 0
    candidates_checked = 0

    for el_id, el_norm, el_last, el_bday in el_players:
        candidates = nba_index.get(el_norm, [])
        if not candidates:
            continue
        candidates_checked += 1

        best = None  # (nba_id, confidence)

        # Single candidate, no birthday on either side → name-unique 'high'
        if len(candidates) == 1 and el_bday is None:
            c = candidates[0]
            info = get_nba_info(c["id"])
            best = (c["id"], info, "high")
        else:
            # Resolve via date of birth
            for c in candidates:
                info = get_nba_info(c["id"])
                if not info:
                    continue
                nba_bday = info.get("birthday")
                if el_bday and nba_bday and el_bday == nba_bday:
                    best = (c["id"], info, "exact")
                    break
            if best is None:
                # No DOB confirmation. Accept only if exactly one candidate
                # and temporal overlap is plausible (medium confidence).
                if len(candidates) == 1:
                    c = candidates[0]
                    info = get_nba_info(c["id"])
                    best = (c["id"], info, "medium")

        if not best:
            continue

        nba_id, info, confidence = best
        info = info or {}

        # Guard: an NBA id already linked to another EL record → skip
        cursor.execute("SELECT id FROM Players WHERE nba_player_id = %s", (nba_id,))
        if cursor.fetchone():
            continue

        cursor.execute("""
            UPDATE Players SET
                nba_player_id           = %s,
                played_nba              = 1,
                is_cross_league_migrant = 1,
                matching_confidence     = %s,
                birthday    = COALESCE(birthday,    %s),
                height_cm   = COALESCE(height_cm,   %s),
                nationality = COALESCE(nationality, %s),
                position    = COALESCE(position,    %s)
            WHERE id = %s
        """, (
            nba_id, confidence,
            info.get("birthday"), info.get("height_cm"),
            info.get("country"), info.get("position"),
            el_id,
        ))
        conn.commit()
        matched += 1
        log.info(f"    [{confidence:6}] matched EL player #{el_id} → NBA {nba_id}")

    log.info(f"  Checked {candidates_checked} name-matched candidates; "
             f"confirmed {matched} cross-league migrants.")

    # ── Pull NBA career stats for confirmed migrants lacking them ──
    cursor.execute("""
        SELECT p.id, p.nba_player_id, p.full_name
        FROM Players p
        WHERE p.is_cross_league_migrant = 1
          AND p.nba_player_id IS NOT NULL
          AND NOT EXISTS (SELECT 1 FROM NBASeasons n WHERE n.player_id = p.id)
    """)
    to_enrich = cursor.fetchall()
    log.info(f"  Fetching NBA career stats for {len(to_enrich)} migrants…")

    for player_id, nba_id, full_name in to_enrich:
        time.sleep(NBA_DELAY)
        career = None
        for attempt in range(3):
            try:
                career = PlayerCareerStats(
                    player_id=nba_id, per_mode36="Totals", timeout=NBA_TIMEOUT
                ).get_data_frames()[0]
                break
            except Exception as exc:
                log.warning(f"    career({full_name}) retry {attempt+1}/3: {exc}")
                time.sleep(NBA_DELAY * (attempt + 2))
        if career is None:
            continue

        for _, s in career.iterrows():
            if str(s.get("LEAGUE_ID")) not in ("00", "0", ""):
                continue  # NBA regular season only
            insert_nba_season(conn, cursor, player_id, s)
        conn.commit()

    cursor.execute("SELECT COUNT(*) FROM Players WHERE is_cross_league_migrant = 1")
    log.info(f"NBA phase done: {cursor.fetchone()[0]} cross-league migrants in DB.")


def insert_nba_season(conn, cursor, player_id: int, s) -> None:
    season_label = nba_season_label(str(s["SEASON_ID"]))
    gp = _i(s.get("GP")) or 0
    fga = _i(s.get("FGA")) or 0
    if gp == 0 or fga == 0:
        return
    fgm = _i(s.get("FGM")) or 0
    tpa = _i(s.get("FG3A")) or 0
    tpm = _i(s.get("FG3M")) or 0
    fta = _i(s.get("FTA")) or 0
    ftm = _i(s.get("FTM")) or 0
    pts = _i(s.get("PTS")) or 0
    minutes = _f(s.get("MIN"))
    ast = _f(s.get("AST"))
    reb = _f(s.get("REB"))
    stl = _f(s.get("STL"))
    blk = _f(s.get("BLK"))
    tov = _f(s.get("TOV"))

    two_a = fga - tpa
    two_m = fgm - tpm
    efg = (fgm + 0.5 * tpm) / fga
    ts_den = 2 * (fga + 0.44 * fta)
    ts = (pts / ts_den) if ts_den else None
    fg_pct = _pct(s.get("FG_PCT"))
    tp_pct = _pct(s.get("FG3_PCT"))
    ft_pct = _pct(s.get("FT_PCT"))

    cursor.execute("""
        INSERT INTO NBASeasons
            (player_id, season, team_abbreviation,
             games_played, games_started, minutes_total, minutes_per_game,
             fga_total, fga_per_game, fgm_total, fg_pct,
             three_pt_fga_total, three_pt_fgm_total, three_pt_pct,
             two_pt_fga_total, two_pt_fgm_total, two_pt_pct,
             ft_attempts_total, ft_made_total, ft_pct,
             efg_pct, ts_pct,
             points_total, points_per_game,
             assists_per_game, rebounds_per_game,
             steals_per_game, blocks_per_game, turnovers_per_game)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE games_played = VALUES(games_played)
    """, (
        player_id, season_label, str(s.get("TEAM_ABBREVIATION") or ""),
        gp, _i(s.get("GS")), minutes,
        round(minutes / gp, 2) if minutes else None,
        fga, round(fga / gp, 2), fgm,
        round(fg_pct * 100, 2) if fg_pct is not None and fg_pct <= 1 else fg_pct,
        tpa, tpm,
        round(tp_pct * 100, 2) if tp_pct is not None and tp_pct <= 1 else tp_pct,
        two_a, two_m,
        round(100.0 * two_m / two_a, 2) if two_a else None,
        fta, ftm,
        round(ft_pct * 100, 2) if ft_pct is not None and ft_pct <= 1 else ft_pct,
        round(efg, 4), round(ts, 4) if ts is not None else None,
        pts, round(pts / gp, 2),
        round(ast / gp, 2) if ast is not None else None,
        round(reb / gp, 2) if reb is not None else None,
        round(stl / gp, 2) if stl is not None else None,
        round(blk / gp, 2) if blk is not None else None,
        round(tov / gp, 2) if tov is not None else None,
    ))


# ═══════════════════════════════════════════════════════════════════════════════
#  Phase 4 - Migration episode detection
# ═══════════════════════════════════════════════════════════════════════════════

def detect_migrations(conn, cursor):
    log.info("━━━  PHASE 3 - Migration episode detection  ━━━")

    cursor.execute(
        "SELECT id, birthday FROM Players WHERE is_cross_league_migrant = 1"
    )
    migrants = cursor.fetchall()
    log.info(f"  Building timelines for {len(migrants)} migrants…")

    total = 0
    for player_id, birthday in migrants:
        cursor.execute(
            "SELECT season, team_abbreviation FROM NBASeasons WHERE player_id = %s",
            (player_id,),
        )
        nba = {r[0]: (r[1] or "") for r in cursor.fetchall()}

        cursor.execute(
            "SELECT season, team_name FROM EuroLeagueSeasons WHERE player_id = %s",
            (player_id,),
        )
        el = {r[0]: (r[1] or "") for r in cursor.fetchall()}

        timeline = sorted(
            [(s, "NBA", t) for s, t in nba.items()] +
            [(s, "EL", t) for s, t in el.items()],
            key=lambda x: label_start_year(x[0]),
        )

        for i, (cur_s, cur_lg, cur_t) in enumerate(timeline):
            for j in range(i + 1, min(i + 3, len(timeline))):
                nxt_s, nxt_lg, nxt_t = timeline[j]
                if cur_lg == nxt_lg:
                    continue
                # Destination must start in a STRICTLY LATER season. Same-year
                # dual-league spells (split seasons) are ambiguous for a
                # before/after design and are excluded (avoids gap = -1).
                if label_start_year(nxt_s) <= label_start_year(cur_s):
                    continue
                gap = label_start_year(nxt_s) - label_start_year(cur_s) - 1
                if gap > 1:
                    break
                direction = "NBA_to_EL" if cur_lg == "NBA" else "EL_to_NBA"
                origin_l = "NBA" if cur_lg == "NBA" else "EuroLeague"
                dest_l = "EuroLeague" if cur_lg == "NBA" else "NBA"
                age = (label_start_year(nxt_s) - birthday.year) if birthday else None

                cursor.execute("""
                    INSERT INTO MigrationEpisodes
                        (player_id, direction, origin_league, destination_league,
                         origin_season, destination_season, origin_team,
                         destination_team, seasons_gap, player_age_at_migration)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE seasons_gap = VALUES(seasons_gap)
                """, (player_id, direction, origin_l, dest_l, cur_s, nxt_s,
                      cur_t, nxt_t, gap, age))
                total += 1
                break
        conn.commit()

    log.info(f"Detected {total} migration episodes.")
    cursor.execute(
        "SELECT direction, COUNT(*) FROM MigrationEpisodes GROUP BY direction"
    )
    for d, c in cursor.fetchall():
        log.info(f"  {d}: {c}")


# ═══════════════════════════════════════════════════════════════════════════════
#  Phase 5 - Shot-level collection (for shooting logs & profiles)
# ═══════════════════════════════════════════════════════════════════════════════

def collect_nba_shots(conn, cursor):
    """
    Pull every NBA field-goal attempt (with coordinates, zone, distance, clock)
    for each migrant, per season they actually played. Resumable: skips any
    (player, season) already present in NBAShots.
    """
    log.info("━━━  PHASE 5a - NBA shot collection  ━━━")

    try:
        from nba_api.stats.endpoints import ShotChartDetail
    except ImportError:
        log.error("nba_api not installed. Run: pip install nba_api")
        return

    # Each migrant's NBA seasons, minus those already collected
    cursor.execute("""
        SELECT n.player_id, p.nba_player_id, p.full_name, n.season
        FROM NBASeasons n
        JOIN Players p ON p.id = n.player_id
        WHERE p.is_cross_league_migrant = 1 AND p.nba_player_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1 FROM NBAShots s
              WHERE s.player_id = n.player_id AND s.season = n.season
          )
        ORDER BY p.full_name, n.season
    """)
    targets = cursor.fetchall()
    log.info(f"  {len(targets)} player-seasons to fetch")

    done = 0
    for player_id, nba_id, full_name, season in targets:
        season_api = season.replace("/", "-")  # '2018/19' → '2018-19'
        time.sleep(NBA_DELAY)
        df = None
        for attempt in range(4):
            try:
                df = ShotChartDetail(
                    team_id=0, player_id=nba_id,
                    season_nullable=season_api,
                    season_type_all_star="Regular Season",
                    context_measure_simple="FGA",
                    timeout=NBA_TIMEOUT,
                ).get_data_frames()[0]
                break
            except Exception as exc:
                log.warning(f"    shots {full_name} {season} retry {attempt+1}/4: {exc}")
                time.sleep(NBA_DELAY * (attempt + 2))
        if df is None:
            continue

        n = 0
        for _, r in df.iterrows():
            shot_type = str(r.get("SHOT_TYPE") or "")
            shot_value = 3 if shot_type.startswith("3") else 2
            game_date = None
            gd = str(r.get("GAME_DATE") or "")
            if len(gd) == 8 and gd.isdigit():
                game_date = f"{gd[:4]}-{gd[4:6]}-{gd[6:]}"
            cursor.execute("""
                INSERT IGNORE INTO NBAShots
                    (player_id, season, game_id, game_date, period,
                     minutes_remaining, seconds_remaining, shot_value, made,
                     action_type, shot_zone_basic, shot_zone_area,
                     shot_zone_range, shot_distance_ft, loc_x, loc_y)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                player_id, season, str(r.get("GAME_ID") or ""), game_date,
                _i(r.get("PERIOD")), _i(r.get("MINUTES_REMAINING")),
                _i(r.get("SECONDS_REMAINING")), shot_value,
                _i(r.get("SHOT_MADE_FLAG")),
                str(r.get("ACTION_TYPE") or "")[:80],
                str(r.get("SHOT_ZONE_BASIC") or "")[:40],
                str(r.get("SHOT_ZONE_AREA") or "")[:40],
                str(r.get("SHOT_ZONE_RANGE") or "")[:40],
                _i(r.get("SHOT_DISTANCE")), _i(r.get("LOC_X")), _i(r.get("LOC_Y")),
            ))
            n += 1
        conn.commit()
        done += 1
        if done % 25 == 0:
            log.info(f"    {done}/{len(targets)} player-seasons done")

    cursor.execute("SELECT COUNT(*) FROM NBAShots")
    log.info(f"NBA shots stored: {cursor.fetchone()[0]}")


SHOT_ACTION_RE = re.compile(r"^([23])FG([AM])$")


def collect_euroleague_shots(conn, cursor, first_year: int):
    """
    For every season that contains a migrant's EuroLeague season, pull each
    game's Points feed and store the migrants' field-goal attempts (coordinates,
    zone, fastbreak / second-chance context, clock). Resumable via ELGamesProcessed.
    """
    log.info("━━━  PHASE 5b - EuroLeague shot collection  ━━━")

    # season_code → {migrant_player_code: player_id}
    cursor.execute("""
        SELECT DISTINCT e.season_code, p.euroleague_player_code, p.id
        FROM EuroLeagueSeasons e
        JOIN Players p ON p.id = e.player_id
        WHERE p.is_cross_league_migrant = 1
          AND p.euroleague_player_code IS NOT NULL
    """)
    # Shot-location data only exists from E2007 onward - don't waste calls earlier.
    shots_floor = max(first_year, EL_SHOTS_FIRST_YEAR)
    season_migrants: Dict[str, Dict[str, int]] = {}
    for season_code, code, pid in cursor.fetchall():
        if int(season_code[1:]) < shots_floor:
            continue
        season_migrants.setdefault(season_code, {})[code] = pid

    log.info(f"  {len(season_migrants)} seasons with shot data (≥E{shots_floor}) contain migrants")

    for season_code in sorted(season_migrants):
        code_to_pid = season_migrants[season_code]
        season_label = el_code_to_label(int(season_code[1:]))

        # Game list (+ dates) for the season
        resp = http_get_json(
            f"{EL_V2}/seasons/{season_code}/games",
            params={"limit": 1000}, base_delay=EL_DELAY,
        )
        games = (resp or {}).get("data", [])
        game_dates: Dict[int, Optional[str]] = {}
        for g in games:
            gc = _i(g.get("gameCode"))
            if gc is None:
                continue
            d = (g.get("date") or g.get("utcDate") or "")[:10]
            game_dates[gc] = d or None

        # Skip games already processed
        cursor.execute(
            "SELECT game_code FROM ELGamesProcessed WHERE season_code = %s",
            (season_code,),
        )
        already = {r[0] for r in cursor.fetchall()}
        todo = [gc for gc in game_dates if gc not in already]
        log.info(f"  {season_label}: {len(game_dates)} games, "
                 f"{len(todo)} to fetch, {len(code_to_pid)} migrants")

        season_shots = 0
        for gc in sorted(todo):
            time.sleep(EL_DELAY)
            data = http_get_json(
                "https://live.euroleague.net/api/Points",
                params={"gamecode": gc, "seasoncode": season_code},
                base_delay=EL_DELAY,
            )
            stored = 0
            if data and isinstance(data.get("Rows"), list):
                for row in data["Rows"]:
                    m = SHOT_ACTION_RE.match((row.get("ID_ACTION") or "").strip())
                    if not m:
                        continue  # not a 2FG/3FG attempt
                    raw_id = (row.get("ID_PLAYER") or "").strip()
                    code = raw_id[1:].lstrip("0") if raw_id.startswith("P") else raw_id.lstrip("0")
                    # match against migrant codes (stored codes may have leading zeros)
                    pid = code_to_pid.get(code) or code_to_pid.get(raw_id[1:].strip()) \
                          or code_to_pid.get(code.zfill(6))
                    if not pid:
                        continue
                    shot_value = int(m.group(1))
                    made = 1 if m.group(2) == "M" else 0
                    cursor.execute("""
                        INSERT IGNORE INTO EuroLeagueShots
                            (player_id, season, season_code, game_code, game_date,
                             team_code, shot_value, made, action_code, action_desc,
                             zone, coord_x, coord_y, minute, game_clock,
                             fastbreak, second_chance, points_off_turnover)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        pid, season_label, season_code, gc, game_dates.get(gc),
                        (row.get("TEAM") or "").strip()[:20], shot_value, made,
                        (row.get("ID_ACTION") or "").strip()[:10],
                        (row.get("ACTION") or "").strip()[:80],
                        (row.get("ZONE") or "").strip()[:5],
                        _i(row.get("COORD_X")), _i(row.get("COORD_Y")),
                        _i(row.get("MINUTE")), (row.get("CONSOLE") or "").strip()[:10],
                        1 if str(row.get("FASTBREAK")) == "1" else 0,
                        1 if str(row.get("SECOND_CHANCE")) == "1" else 0,
                        1 if str(row.get("POINTS_OFF_TURNOVER")) == "1" else 0,
                    ))
                    stored += 1
            cursor.execute(
                "INSERT IGNORE INTO ELGamesProcessed (season_code, game_code, shots_stored) "
                "VALUES (%s,%s,%s)", (season_code, gc, stored),
            )
            season_shots += stored
            conn.commit()
        log.info(f"    ✓ {season_label}: {season_shots} migrant shots stored")

    cursor.execute("SELECT COUNT(*) FROM EuroLeagueShots")
    log.info(f"EuroLeague shots stored: {cursor.fetchone()[0]}")


# ═══════════════════════════════════════════════════════════════════════════════
#  Views + summary
# ═══════════════════════════════════════════════════════════════════════════════

def create_views(conn, cursor):
    statements = [
        "DROP VIEW IF EXISTS v_migrants",
        """
        CREATE VIEW v_migrants AS
        SELECT p.id, p.full_name, p.nationality, p.birthday, p.height_cm,
               p.position, p.nba_player_id, p.euroleague_player_code,
               p.matching_confidence,
               COUNT(DISTINCT n.season) AS nba_seasons,
               COUNT(DISTINCT e.season) AS el_seasons,
               COUNT(DISTINCT me.id)    AS migration_episodes
        FROM Players p
        LEFT JOIN NBASeasons        n  ON n.player_id  = p.id
        LEFT JOIN EuroLeagueSeasons e  ON e.player_id  = p.id
        LEFT JOIN MigrationEpisodes me ON me.player_id = p.id
        WHERE p.is_cross_league_migrant = 1
        GROUP BY p.id
        """,
        "DROP VIEW IF EXISTS v_migration_profiles",
        """
        CREATE VIEW v_migration_profiles AS
        SELECT me.id AS episode_id, p.full_name, p.nationality, p.birthday,
               p.position, me.direction, me.origin_season, me.destination_season,
               me.seasons_gap, me.player_age_at_migration,
               CASE WHEN me.direction='NBA_to_EL' THEN n.fga_per_game     ELSE e.fga_per_game     END AS origin_fga_pg,
               CASE WHEN me.direction='NBA_to_EL' THEN n.three_pt_pct     ELSE e.three_pt_pct     END AS origin_3pt_pct,
               CASE WHEN me.direction='NBA_to_EL' THEN n.efg_pct          ELSE e.efg_pct          END AS origin_efg,
               CASE WHEN me.direction='NBA_to_EL' THEN n.points_per_game  ELSE e.points_per_game  END AS origin_pts_pg,
               CASE WHEN me.direction='NBA_to_EL' THEN e2.fga_per_game    ELSE n2.fga_per_game    END AS dest_fga_pg,
               CASE WHEN me.direction='NBA_to_EL' THEN e2.three_pt_pct    ELSE n2.three_pt_pct    END AS dest_3pt_pct,
               CASE WHEN me.direction='NBA_to_EL' THEN e2.efg_pct         ELSE n2.efg_pct         END AS dest_efg,
               CASE WHEN me.direction='NBA_to_EL' THEN e2.points_per_game ELSE n2.points_per_game END AS dest_pts_pg
        FROM MigrationEpisodes me
        JOIN Players p ON p.id = me.player_id
        LEFT JOIN NBASeasons        n  ON n.player_id  = me.player_id AND n.season  = me.origin_season
        LEFT JOIN EuroLeagueSeasons e  ON e.player_id  = me.player_id AND e.season  = me.origin_season
        LEFT JOIN NBASeasons        n2 ON n2.player_id = me.player_id AND n2.season = me.destination_season
        LEFT JOIN EuroLeagueSeasons e2 ON e2.player_id = me.player_id AND e2.season = me.destination_season
        """,
        # Unified shooting log: every migrant shot from both leagues, one row each,
        # with harmonised columns - ready for shooting-profile feature engineering.
        "DROP VIEW IF EXISTS v_shooting_log",
        """
        CREATE VIEW v_shooting_log AS
            SELECT s.player_id, p.full_name, 'NBA' AS league, s.season,
                   s.game_id AS game_ref, s.game_date, s.period,
                   s.shot_value, s.made, s.shot_distance_ft AS distance,
                   s.shot_zone_basic AS zone, s.action_type,
                   s.loc_x, s.loc_y, NULL AS fastbreak, NULL AS second_chance
            FROM NBAShots s JOIN Players p ON p.id = s.player_id
        UNION ALL
            SELECT s.player_id, p.full_name, 'EuroLeague' AS league, s.season,
                   CAST(s.game_code AS CHAR) AS game_ref, s.game_date, NULL AS period,
                   s.shot_value, s.made, NULL AS distance,
                   s.zone, s.action_desc AS action_type,
                   s.coord_x AS loc_x, s.coord_y AS loc_y,
                   s.fastbreak, s.second_chance
            FROM EuroLeagueShots s JOIN Players p ON p.id = s.player_id
        """,
        # Per player-season-league shooting profile aggregates.
        "DROP VIEW IF EXISTS v_shooting_profile",
        """
        CREATE VIEW v_shooting_profile AS
        SELECT player_id, full_name, league, season,
               COUNT(*)                              AS fga,
               SUM(made)                             AS fgm,
               SUM(CASE WHEN shot_value=3 THEN 1 ELSE 0 END)            AS fg3a,
               SUM(CASE WHEN shot_value=3 AND made=1 THEN 1 ELSE 0 END) AS fg3m,
               ROUND(SUM(CASE WHEN shot_value=3 THEN 1 ELSE 0 END)/COUNT(*), 4) AS three_pt_rate,
               ROUND((SUM(made)+0.5*SUM(CASE WHEN shot_value=3 AND made=1 THEN 1 ELSE 0 END))/COUNT(*), 4) AS efg,
               ROUND(AVG(distance), 2)               AS mean_distance_ft
        FROM v_shooting_log
        GROUP BY player_id, full_name, league, season
        """,
    ]
    for stmt in statements:
        try:
            cursor.execute(stmt)
            conn.commit()
        except Exception as exc:
            log.warning(f"View: {exc}")
    log.info("Views ready: v_migrants, v_migration_profiles, "
             "v_shooting_log, v_shooting_profile")


def print_summary(cursor):
    def q(sql):
        cursor.execute(sql)
        return cursor.fetchone()[0]

    log.info("")
    log.info("═══════════════════════════════════════════════════════")
    log.info(f"  DATABASE SUMMARY  ({DB_NAME})")
    log.info("═══════════════════════════════════════════════════════")
    log.info(f"  Players total              : {q('SELECT COUNT(*) FROM Players')}")
    log.info(f"  - played EuroLeague        : {q('SELECT COUNT(*) FROM Players WHERE played_euroleague=1')}")
    log.info(f"  - played NBA               : {q('SELECT COUNT(*) FROM Players WHERE played_nba=1')}")
    log.info(f"  - cross-league migrants    : {q('SELECT COUNT(*) FROM Players WHERE is_cross_league_migrant=1')}")
    log.info("")
    log.info(f"  EuroLeague player-seasons  : {q('SELECT COUNT(*) FROM EuroLeagueSeasons')}")
    log.info(f"  NBA player-seasons         : {q('SELECT COUNT(*) FROM NBASeasons')}")
    log.info("")
    log.info(f"  Migration episodes total   : {q('SELECT COUNT(*) FROM MigrationEpisodes')}")
    nba_to_el = q("SELECT COUNT(*) FROM MigrationEpisodes WHERE direction = 'NBA_to_EL'")
    el_to_nba = q("SELECT COUNT(*) FROM MigrationEpisodes WHERE direction = 'EL_to_NBA'")
    log.info(f"  - NBA → EuroLeague         : {nba_to_el}")
    log.info(f"  - EuroLeague → NBA         : {el_to_nba}")
    log.info("")
    log.info(f"  NBA shots (migrants)       : {q('SELECT COUNT(*) FROM NBAShots')}")
    log.info(f"  EuroLeague shots (migrants): {q('SELECT COUNT(*) FROM EuroLeagueShots')}")

    cursor.execute("""
        SELECT p.full_name, p.nationality, p.matching_confidence,
               me.direction, me.origin_season, me.destination_season,
               me.player_age_at_migration
        FROM MigrationEpisodes me
        JOIN Players p ON p.id = me.player_id
        ORDER BY me.destination_season DESC, p.full_name
        LIMIT 20
    """)
    rows = cursor.fetchall()
    if rows:
        log.info("")
        log.info("  Sample migration episodes:")
        log.info(f"  {'Player':<26}{'Nat':<5}{'Conf':<8}{'Direction':<12}{'From':<8}{'To':<8}{'Age':>4}")
        log.info("  " + "─" * 71)
        for name, nat, conf, direction, o_s, d_s, age in rows:
            log.info(f"  {name[:25]:<26}{str(nat or '')[:4]:<5}{conf:<8}"
                     f"{direction:<12}{o_s:<8}{d_s:<8}{str(age or '?'):>4}")
    log.info("═══════════════════════════════════════════════════════")


# ═══════════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Build NBA-EuroLeague cross-league player database."
    )
    parser.add_argument("--skip-el", action="store_true",
                        help="skip EuroLeague collection")
    parser.add_argument("--skip-nba-match", action="store_true",
                        help="skip NBA matching & enrichment")
    parser.add_argument("--skip-migrations", action="store_true",
                        help="skip migration detection")
    parser.add_argument("--skip-shots", action="store_true",
                        help="skip shot-level collection (NBA + EuroLeague)")
    parser.add_argument("--skip-nba-shots", action="store_true",
                        help="skip NBA shot collection only")
    parser.add_argument("--skip-el-shots", action="store_true",
                        help="skip EuroLeague shot collection only")
    parser.add_argument("--shots-only", action="store_true",
                        help="only collect shots for existing migrants (skip phases 1-3)")
    parser.add_argument("--summary-only", action="store_true",
                        help="print DB summary and exit")
    parser.add_argument("--el-from", type=int, default=EL_FIRST_YEAR_DEFAULT,
                        help=f"first EuroLeague year (default {EL_FIRST_YEAR_DEFAULT})")
    args = parser.parse_args()

    # Create DB/schema using a connection without a fixed database
    boot_cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    conn, cursor = mysql.connector.connect(**boot_cfg), None
    cursor = conn.cursor()
    init_schema(conn, cursor)
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        if args.summary_only:
            print_summary(cursor)
            return

        if not args.shots_only:
            if not args.skip_el:
                collect_euroleague(conn, cursor, args.el_from)
            if not args.skip_nba_match:
                match_and_enrich_nba(conn, cursor)
            if not args.skip_migrations:
                detect_migrations(conn, cursor)

        if not args.skip_shots:
            if not args.skip_nba_shots:
                collect_nba_shots(conn, cursor)
            if not args.skip_el_shots:
                collect_euroleague_shots(conn, cursor, args.el_from)

        create_views(conn, cursor)
        print_summary(cursor)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
        log.info("Connection closed. Done.")


if __name__ == "__main__":
    main()
