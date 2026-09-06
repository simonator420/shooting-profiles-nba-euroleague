# Do Shooting Profiles Travel?
### Shot Selection, Shot Quality, and Performance Adaptation Between the NBA and EuroLeague

---

## Repository Structure

```
shooting-profiles-nba-euroleague/
├── notebooks/
│   └── shooting_profiles_travel_reproducibility.ipynb   # Reproducible analysis from included files
├── data/
│   ├── shot_level_scored.csv                            # Migrant shot-level data with out-of-fold sxSV
│   ├── player_season_boxscore.csv                       # NBA and EuroLeague player-season box scores
│   ├── migration_episodes.csv                           # NBA-EuroLeague migration episodes
│   ├── players.csv                                      # Player index
│   ├── control_pool_nba.csv                             # NBA non-migrant seasons for matched controls
│   ├── sxsv_model_metrics.csv                           # Out-of-fold sxSV model performance
│   └── sxsv_calibration_bins.csv                        # Reliability-curve bins for sxSV models
├── tables/
│   ├── supplementary_output_tables.xlsx                 # Numbered supplementary tables
│   └── *.csv, *.md                                      # Revision, robustness, and diagnostic outputs
├── scripts/
│   ├── build_crossleague_db.py                          # Database rebuild script
│   └── collect_*_shots.py                               # Source-data collection scripts
├── requirements.txt
├── CITATION.cff
├── ZENODO_UPLOAD.md
├── README.md
└── LICENSE
```

---

## Reproducing the Results

The statistical results reported in the manuscript can be reproduced from the
files included in this repository, without access to the local MySQL database
used during data collection.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Open `notebooks/shooting_profiles_travel_reproducibility.ipynb`.
3. Run all cells from top to bottom.
4. The final section prints the paper statistics and reproduces the main output
   tables from the included data files.

The notebook covers sxSV model performance, sample construction, included versus
excluded episodes, within-player pre-post changes, field-goal-attempt threshold
sensitivity, matched-control comparisons, dependence checks, direct versus
one-season-gap transitions, playing time and usage, player-season shooting
profiles by league, profile transferability, repeated-measures models, and
exploratory analyses.

---

## Notes on the Data

**Spatial expected shot value (sxSV).** `shot_level_scored.csv` contains
out-of-fold predicted make probabilities for every migrant field-goal attempt
under two specifications:

- `*_harmonised` - identical predictors in both leagues: shot distance, shot
  angle, harmonised shot zone, and shot value.
- `*_league_specific` - the manuscript specification, which adds the limited
  context exposed by each competition feed: period for the NBA, and fastbreak
  and second-chance flags for the EuroLeague.

Both specifications use five-fold `GroupKFold` out-of-fold predictions grouped
by player. The full shot populations used to fit those models contain about
4.0 million NBA attempts and 0.54 million EuroLeague attempts. They are not
stored as raw population files in this repository, but the fitted out-of-fold
predictions for the analysed migrant shots are included.

**Sample sizes.** The broad box-score migration sample contains 589 episodes
from 283 players. The shot-coordinate sample used for the spatial analysis is
smaller because EuroLeague shot coordinates are available only from 2007/08 and
both sides of an episode must clear the attempt threshold: 31 episodes from 11
players at the primary 100-attempt threshold. The notebook reports robustness
checks under player-clustered, one-episode-per-move, and one-episode-per-player
restrictions.

**Source data.** EuroLeague data were collected from publicly accessible
EuroLeague endpoints (`api-live.euroleague.net` and `live.euroleague.net`).
NBA data were collected from `stats.nba.com` through the `nba_api` package. The
files in `data/` and `tables/` are processed research outputs derived from those
public sources.

---

## Supplementary Tables

The `tables/` directory includes the supplementary workbook and the revision
tables used for robustness checks and diagnostics, including threshold
sensitivity, matched-control balance, dependence checks, direct versus
one-season-gap transitions, usage changes, and specification agreement.

Manuscript figure files are not included in this analysis archive.

---

## Rebuilding the Source Database

The repository is designed so that the paper results can be reproduced from the
included processed files. For a full source-data rebuild, use the scripts in
`scripts/`:

```bash
python scripts/build_crossleague_db.py
python scripts/collect_nba_population_shots.py
python scripts/collect_el_population_shots.py
```

The rebuild expects a local MySQL database named `nba_euroleague`. Default
credentials used in the scripts are:

```python
DB_CONFIG = dict(host="localhost", port=8889, user="root",
                 password="root", database="nba_euroleague", charset="utf8mb4")
```

The full rebuild is rate-limit dependent and may take several hours. The scripts
are resumable and skip records already stored.

---

## Citation

If you use this repository, please cite the archived Zenodo release. The DOI
will be added here after publication of the first Zenodo release.

---

## License

Code released under the [MIT License](LICENSE). The license covers repository
code. It does not grant rights in the underlying NBA or EuroLeague source data.
