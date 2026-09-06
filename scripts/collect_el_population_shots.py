"""
collect_el_population_shots.py
Collects ALL EuroLeague field-goal attempts (every player, not just migrants)
from E2007 (2007/08) onward into table `ELPopulationShots`.

Purpose: train sxSV (spatial expected shot value) on the full league population
instead of the migrant-only subsample. The full population model can then be
applied out-of-fold to migrants for unbiased expected-value estimates.

Separate tracking table `ELPopGamesProcessed` keeps this run independent of the
migrant-only ELGamesProcessed table - safe to run alongside or after the main
build_crossleague_db.py pipeline.

Estimated time: ~90-120 min for all seasons (E2007-E2025, ~18 seasons × ~250 games
× ~0.4 s/call). Fully resumable - re-running skips already-processed games.

Run:  python collect_el_population_shots.py
      python collect_el_population_shots.py --from-year 2015   # restart from season
      python collect_el_population_shots.py --dry-run          # count games, no writes
"""

import argparse
import logging
import re
import sys
import time
from datetime import datetime
from typing import Optional

import mysql.connector
import requests

# ── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("collect_el_population_shots.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("elpop")

# ── Config ────────────────────────────────────────────────────────────────────

DB = dict(host="localhost", port=8889, user="root", password="root",
          database="nba_euroleague", charset="utf8mb4")

EL_SHOTS_FIRST_YEAR = 2007
EL_LAST_YEAR = datetime.now().year
EL_V2 = "https://api-live.euroleague.net/v2/competitions/E"
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 basketball-research/1.0 (academic)"}
EL_DELAY = 0.4

SHOT_ACTION_RE = re.compile(r"^([23])FG([AM])$")

# ── Helpers ───────────────────────────────────────────────────────────────────

def _i(v) -> Optional[int]:
    try:
        if v is None or v == "":
            return None
        x = float(v)
        return None if x != x else int(round(x))
    except (TypeError, ValueError):
        return None


def http_get_json(url: str, params: dict = None, retries: int = 4,
                  base_delay: float = 1.0) -> Optional[dict]:
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=HTTP_HEADERS, timeout=25)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            if not r.content or not r.text.strip():
                return None
            return r.json()
        except Exception as exc:
            wait = base_delay * (attempt + 1)
            log.warning(f"  retry {attempt + 1}/{retries} ({exc}); wait {wait:.1f}s")
            time.sleep(wait)
    log.error(f"  failed permanently: {url}")
    return None


# ── Schema ────────────────────────────────────────────────────────────────────

DDL = [
    """
    CREATE TABLE IF NOT EXISTS ELPopulationShots (
        id              BIGINT AUTO_INCREMENT PRIMARY KEY,
        season_code     VARCHAR(10) NOT NULL,
        season_label    VARCHAR(10),
        game_code       INT NOT NULL,
        game_date       DATE,
        team_code       VARCHAR(20),
        player_code     VARCHAR(30),        -- raw EL player code (no FK)
        shot_value      TINYINT NOT NULL,   -- 2 or 3
        made            TINYINT NOT NULL,   -- 1=made, 0=missed
        action_code     VARCHAR(10),
        zone            VARCHAR(5),
        coord_x         INT,               -- centimetres, basket at (0,0)
        coord_y         INT,
        minute          INT,
        game_clock      VARCHAR(10),
        fastbreak       TINYINT NOT NULL DEFAULT 0,
        second_chance   TINYINT NOT NULL DEFAULT 0,
        pts_off_turnover TINYINT NOT NULL DEFAULT 0,
        INDEX idx_pop_season (season_code),
        INDEX idx_pop_player (player_code),
        UNIQUE KEY uq_pop_shot (season_code, game_code, player_code,
                                shot_value, made, minute, coord_x, coord_y)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS ELPopGamesProcessed (
        season_code     VARCHAR(10) NOT NULL,
        game_code       INT NOT NULL,
        shots_stored    INT NOT NULL DEFAULT 0,
        processed_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (season_code, game_code)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
]


def init_tables(conn, cur):
    for ddl in DDL:
        cur.execute(ddl)
    conn.commit()
    log.info("Tables ELPopulationShots + ELPopGamesProcessed ready.")


# ── Collection ────────────────────────────────────────────────────────────────

def collect(conn, cur, from_year: int, dry_run: bool):
    seasons = [f"E{y}" for y in range(from_year, EL_LAST_YEAR + 1)]
    total_shots = 0
    total_games = 0

    for season_code in seasons:
        yr = int(season_code[1:])
        season_label = f"{yr}-{str(yr + 1)[-2:]}"

        resp = http_get_json(f"{EL_V2}/seasons/{season_code}/games",
                             params={"limit": 1000}, base_delay=EL_DELAY)
        games = (resp or {}).get("data", [])
        if not games:
            log.info(f"  {season_label}: no game list - skipping")
            continue

        game_dates: dict = {}
        for g in games:
            gc = _i(g.get("gameCode"))
            if gc is None:
                continue
            d = (g.get("date") or g.get("utcDate") or "")[:10]
            game_dates[gc] = d or None

        cur.execute(
            "SELECT game_code FROM ELPopGamesProcessed WHERE season_code = %s",
            (season_code,),
        )
        already = {r[0] for r in cur.fetchall()}
        todo = sorted(gc for gc in game_dates if gc not in already)

        log.info(f"  {season_label}: {len(game_dates)} games total, "
                 f"{len(todo)} remaining, {len(already)} already done")

        if dry_run:
            continue

        season_shots = 0
        for gc in todo:
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
                        continue
                    raw_id = (row.get("ID_PLAYER") or "").strip()
                    player_code = raw_id[1:].lstrip("0") if raw_id.startswith("P") else raw_id.lstrip("0")
                    if not player_code:
                        continue
                    shot_value = int(m.group(1))
                    made = 1 if m.group(2) == "M" else 0
                    try:
                        cur.execute("""
                            INSERT IGNORE INTO ELPopulationShots
                                (season_code, season_label, game_code, game_date,
                                 team_code, player_code, shot_value, made,
                                 action_code, zone, coord_x, coord_y,
                                 minute, game_clock,
                                 fastbreak, second_chance, pts_off_turnover)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, (
                            season_code, season_label, gc, game_dates.get(gc),
                            (row.get("TEAM") or "").strip()[:20],
                            player_code[:30],
                            shot_value, made,
                            (row.get("ID_ACTION") or "").strip()[:10],
                            (row.get("ZONE") or "").strip()[:5],
                            _i(row.get("COORD_X")), _i(row.get("COORD_Y")),
                            _i(row.get("MINUTE")),
                            (row.get("CONSOLE") or "").strip()[:10],
                            1 if str(row.get("FASTBREAK")) == "1" else 0,
                            1 if str(row.get("SECOND_CHANCE")) == "1" else 0,
                            1 if str(row.get("POINTS_OFF_TURNOVER")) == "1" else 0,
                        ))
                        stored += 1
                    except mysql.connector.Error as e:
                        log.warning(f"    INSERT error game {gc}: {e}")

            cur.execute(
                "INSERT IGNORE INTO ELPopGamesProcessed "
                "(season_code, game_code, shots_stored) VALUES (%s,%s,%s)",
                (season_code, gc, stored),
            )
            season_shots += stored
            conn.commit()

        log.info(f"    ✓ {season_label}: {season_shots:,} shots stored "
                 f"({len(todo)} games)")
        total_shots += season_shots
        total_games += len(todo)

    if not dry_run:
        cur.execute("SELECT COUNT(*) FROM ELPopulationShots")
        grand = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT player_code) FROM ELPopulationShots")
        players = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT season_code) FROM ELPopulationShots")
        seasons_done = cur.fetchone()[0]
        log.info(
            f"\nDone. ELPopulationShots: {grand:,} shots | "
            f"{players:,} distinct players | {seasons_done} seasons"
        )
    else:
        log.info("\n[dry-run] No data written.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Collect all EuroLeague shots (full population) for sxSV training."
    )
    parser.add_argument("--from-year", type=int, default=EL_SHOTS_FIRST_YEAR,
                        help=f"First EL season year to collect (default {EL_SHOTS_FIRST_YEAR})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print game counts but write nothing to DB")
    args = parser.parse_args()

    from_year = max(args.from_year, EL_SHOTS_FIRST_YEAR)
    log.info(f"EL population shot collection  |  E{from_year}-E{EL_LAST_YEAR}"
             f"{'  [DRY RUN]' if args.dry_run else ''}")

    conn = mysql.connector.connect(**DB)
    cur = conn.cursor()

    init_tables(conn, cur)
    collect(conn, cur, from_year=from_year, dry_run=args.dry_run)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
