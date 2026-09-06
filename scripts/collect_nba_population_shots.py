"""
collect_nba_population_shots.py
Collects ALL NBA field-goal attempts from 2007-08 onward into `NBAPopulationShots`
by iterating all 30 teams × 19 seasons (570 API calls total).  Each per-team call
returns ~3-4k shots - well below the API page limit that truncated the old
league-wide approach to ~100k shots (first half of season only).

Purpose: train NBA sxSV on the full league population.  Migrant NBA shots are a
subset; their OOF predictions are transferred via (nba_player_id, game_id, loc_x,
loc_y) matching.

Resumable - skips (season, team_id) pairs already collected (≥100 rows).

Run:  python collect_nba_population_shots.py
      python collect_nba_population_shots.py --from-year 2015
      python collect_nba_population_shots.py --dry-run
"""

import argparse
import logging
import sys
import time
from typing import Optional

import mysql.connector

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("collect_nba_population_shots.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("nbapop")

DB = dict(host="localhost", port=8889, user="root", password="root",
          database="nba_euroleague", charset="utf8mb4")

FROM_YEAR   = 2007
LAST_YEAR   = 2025   # includes 2025-26 season
NBA_DELAY   = 1.2    # seconds between API calls
SKIP_THRESH = 100    # (season, team_id) pairs with ≥100 rows are considered complete

# All 30 current NBA franchises (stable IDs used throughout this era)
NBA_TEAM_IDS = [
    1610612737,  # ATL
    1610612738,  # BOS
    1610612739,  # CLE
    1610612740,  # NOP
    1610612741,  # CHI
    1610612742,  # DAL
    1610612743,  # DEN
    1610612744,  # GSW
    1610612745,  # HOU
    1610612746,  # LAC
    1610612747,  # LAL
    1610612748,  # MIA
    1610612749,  # MIL
    1610612750,  # MIN
    1610612751,  # BKN
    1610612752,  # NYK
    1610612753,  # ORL
    1610612754,  # IND
    1610612755,  # PHI
    1610612756,  # PHX
    1610612757,  # POR
    1610612758,  # SAC
    1610612759,  # SAS
    1610612760,  # OKC
    1610612761,  # TOR
    1610612762,  # UTA
    1610612763,  # MEM
    1610612764,  # WAS
    1610612765,  # DET
    1610612766,  # CHA
]


def f(v) -> Optional[float]:
    try:
        x = float(v)
        return None if x != x else x
    except (TypeError, ValueError):
        return None


def i(v) -> Optional[int]:
    try:
        x = float(v)
        return None if x != x else int(round(x))
    except (TypeError, ValueError):
        return None


def season_label(y: int) -> str:
    return f"{y}-{str(y + 1)[-2:]}"


DDL = """
    CREATE TABLE IF NOT EXISTS NBAPopulationShots (
        id              BIGINT AUTO_INCREMENT PRIMARY KEY,
        nba_player_id   INT NOT NULL,
        player_name     VARCHAR(200),
        team_id         INT,
        season          VARCHAR(10) NOT NULL,
        game_id         VARCHAR(20),
        game_date       DATE,
        period          TINYINT,
        shot_value      TINYINT NOT NULL,
        made            TINYINT NOT NULL,
        action_type     VARCHAR(80),
        shot_zone_basic VARCHAR(40),
        loc_x           INT,
        loc_y           INT,
        shot_distance   INT,
        INDEX idx_nbapop_season  (season),
        INDEX idx_nbapop_player  (nba_player_id),
        INDEX idx_nbapop_team    (team_id),
        UNIQUE KEY uq_nbapop (nba_player_id, game_id, period, loc_x, loc_y, shot_value, made)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""


def init_tables(conn, cur):
    cur.execute(DDL)
    conn.commit()
    log.info("Table NBAPopulationShots ready.")


def collect(conn, cur, from_year: int, dry_run: bool):
    from nba_api.stats.endpoints import ShotChartDetail

    seasons = [season_label(y) for y in range(from_year, LAST_YEAR + 1)]
    grand_total = 0

    for season in seasons:
        season_new = 0
        season_skipped = 0

        for team_id in NBA_TEAM_IDS:
            cur.execute(
                "SELECT COUNT(*) FROM NBAPopulationShots WHERE season=%s AND team_id=%s",
                (season, team_id),
            )
            n_existing = cur.fetchone()[0]
            if n_existing >= SKIP_THRESH:
                season_skipped += 1
                continue

            if dry_run:
                log.info(f"  [dry-run] {season} team {team_id}: would fetch")
                continue

            time.sleep(NBA_DELAY)
            try:
                df = ShotChartDetail(
                    team_id=team_id,
                    player_id=0,
                    season_nullable=season,
                    season_type_all_star="Regular Season",
                    context_measure_simple="FGA",
                    timeout=120,
                ).get_data_frames()[0]
            except Exception as exc:
                log.warning(f"  {season} team {team_id}: fetch failed ({exc}), skipping.")
                time.sleep(5)
                continue

            if df.empty:
                continue

            n = 0
            for _, row in df.iterrows():
                shot_val = 3 if (row.get("SHOT_TYPE") or "").startswith("3") else 2
                made = 1 if row.get("SHOT_MADE_FLAG") == 1 else 0
                gd = (str(row.get("GAME_DATE") or ""))[:10] or None
                try:
                    cur.execute(
                        """
                        INSERT IGNORE INTO NBAPopulationShots
                            (nba_player_id, player_name, team_id, season, game_id,
                             game_date, period, shot_value, made,
                             action_type, shot_zone_basic, loc_x, loc_y, shot_distance)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """,
                        (
                            i(row.get("PLAYER_ID")),
                            str(row.get("PLAYER_NAME") or "")[:200],
                            i(row.get("TEAM_ID")),
                            season,
                            str(row.get("GAME_ID") or "")[:20],
                            gd,
                            i(row.get("PERIOD")),
                            shot_val, made,
                            str(row.get("ACTION_TYPE") or "")[:80],
                            str(row.get("SHOT_ZONE_BASIC") or "")[:40],
                            i(row.get("LOC_X")), i(row.get("LOC_Y")),
                            i(row.get("SHOT_DISTANCE")),
                        ),
                    )
                    n += 1
                except mysql.connector.Error as e:
                    log.warning(f"    INSERT error: {e}")

            conn.commit()
            season_new += n

        if not dry_run:
            if season_skipped == len(NBA_TEAM_IDS):
                log.info(f"  {season}: all 30 teams already collected, skipping.")
            else:
                cur.execute(
                    "SELECT COUNT(*) FROM NBAPopulationShots WHERE season=%s", (season,)
                )
                total_season = cur.fetchone()[0]
                log.info(
                    f"  ✓ {season}: +{season_new:,} new shots "
                    f"({season_skipped}/30 teams skipped) → {total_season:,} total"
                )
            grand_total += season_new

    if not dry_run:
        cur.execute("SELECT COUNT(*) FROM NBAPopulationShots")
        grand = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT nba_player_id) FROM NBAPopulationShots")
        players = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT season) FROM NBAPopulationShots")
        seasons_done = cur.fetchone()[0]
        log.info(
            f"\nDone. NBAPopulationShots: {grand:,} shots | "
            f"{players:,} distinct players | {seasons_done} seasons"
        )
    else:
        log.info("\n[dry-run] complete.")


def main():
    parser = argparse.ArgumentParser(
        description="Collect all NBA shots (full population) for sxSV training."
    )
    parser.add_argument("--from-year", type=int, default=FROM_YEAR)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    log.info(
        f"NBA population shot collection (per-team)  |  "
        f"{season_label(args.from_year)}-{season_label(LAST_YEAR)}"
        f"{'  [DRY RUN]' if args.dry_run else ''}"
    )

    conn = mysql.connector.connect(**DB)
    cur = conn.cursor()
    init_tables(conn, cur)
    collect(conn, cur, from_year=args.from_year, dry_run=args.dry_run)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
