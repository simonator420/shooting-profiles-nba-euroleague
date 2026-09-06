"""
collect_nba_controls.py
Collects box-score seasons for NON-MIGRANT NBA players (active 2007+) into table
`NBANonMigrantSeasons`, so the matched-control DiD can run for the NBA→EuroLeague
direction too. Box stats only (no shots). Resumable.

Run:  python collect_nba_controls.py
"""
import time
import logging
import sys
import mysql.connector

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s",
                    datefmt="%H:%M:%S", handlers=[logging.StreamHandler(sys.stdout)])
log = logging.getLogger("nbactrl")

DB = dict(host="localhost", port=8889, user="root", password="root",
          database="nba_euroleague", charset="utf8mb4")
DELAY = 0.6
FROM_YEAR = 2007  # era with EuroLeague shot data / migrant overlap


def f(v):
    try:
        x = float(v); return None if x != x else x
    except (TypeError, ValueError):
        return None


def i(v):
    try:
        x = float(v); return None if x != x else int(round(x))
    except (TypeError, ValueError):
        return None


def retry(fn, tries=6, base=2.0):
    """Call fn() with exponential backoff; return None if all attempts fail."""
    for a in range(tries):
        try:
            return fn()
        except Exception as exc:
            wait = base * (a + 1)
            log.info(f"  nba.com retry {a + 1}/{tries} ({type(exc).__name__}); wait {wait:.0f}s")
            time.sleep(wait)
    return None


def season_label(s):  # '2018-19'
    y = int(s[:4]); return f"{y}-{str(y + 1)[-2:]}"


def main():
    # Bulk endpoint: one call returns EVERY player's season totals - ~18 calls
    # total instead of ~1900 per-player calls (far gentler on stats.nba.com).
    from nba_api.stats.endpoints import LeagueDashPlayerStats

    conn = mysql.connector.connect(**DB); cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS NBANonMigrantSeasons (
            id              INT AUTO_INCREMENT PRIMARY KEY,
            nba_player_id   INT NOT NULL,
            full_name       VARCHAR(200),
            season          VARCHAR(10) NOT NULL,
            games_played    INT,
            fga_per_game    FLOAT,
            efg_pct         FLOAT,
            three_pt_pct    FLOAT,
            points_per_game FLOAT,
            UNIQUE KEY uq_ctrl (nba_player_id, season)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    conn.commit()

    cur.execute("SELECT nba_player_id FROM Players WHERE nba_player_id IS NOT NULL")
    migrant_ids = {r[0] for r in cur.fetchall()}

    seasons = [season_label(f"{y}") for y in range(FROM_YEAR, 2025)]  # 2007-08 .. 2024-25
    # A full season has ~450 players via the bulk endpoint; <150 rows means only
    # partial data exists (e.g. from an earlier interrupted per-player run), so
    # re-fetch it. ON DUPLICATE KEY UPDATE makes the bulk insert idempotent.
    for season in seasons:
        season_slash = season.replace("-", "/")
        cur.execute("SELECT COUNT(*) FROM NBANonMigrantSeasons WHERE season = %s", (season_slash,))
        if cur.fetchone()[0] >= 150:
            log.info(f"  {season}: already collected ({cur.rowcount}), skipping.")
            continue

        time.sleep(DELAY)
        df = retry(lambda: LeagueDashPlayerStats(
            season=season, season_type_all_star="Regular Season",
            per_mode_detailed="Totals", timeout=60).get_data_frames()[0], tries=5)
        if df is None:
            log.info(f"  {season}: unavailable (nba.com), will retry on next run.")
            continue

        n = 0
        for _, s in df.iterrows():
            pid = i(s.get("PLAYER_ID"))
            if pid is None or pid in migrant_ids:
                continue
            gp = i(s.get("GP")) or 0; fga = i(s.get("FGA")) or 0
            if gp == 0 or fga == 0:
                continue
            fgm = i(s.get("FGM")) or 0; tpa = i(s.get("FG3A")) or 0; tpm = i(s.get("FG3M")) or 0
            pts = i(s.get("PTS")) or 0
            efg = (fgm + 0.5 * tpm) / fga
            tp_pct = f(s.get("FG3_PCT"))
            cur.execute("""
                INSERT INTO NBANonMigrantSeasons
                    (nba_player_id, full_name, season, games_played,
                     fga_per_game, efg_pct, three_pt_pct, points_per_game)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE games_played = VALUES(games_played)
            """, (pid, str(s.get("PLAYER_NAME") or ""), season_slash, gp,
                  round(fga / gp, 2), round(efg, 4),
                  round(tp_pct * 100, 2) if tp_pct is not None else None,
                  round(pts / gp, 2)))
            n += 1
        conn.commit()
        log.info(f"  {season}: stored {n} non-migrant player-seasons")

    cur.execute("SELECT COUNT(DISTINCT nba_player_id), COUNT(*) FROM NBANonMigrantSeasons")
    p, r = cur.fetchone()
    log.info(f"Done. NBA non-migrant controls: {p} players, {r} player-seasons.")
    cur.close(); conn.close()


if __name__ == "__main__":
    main()
