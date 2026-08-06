# Do Shooting Profiles Travel?
### Shot Selection, Shot Quality, and Performance Adaptation Between the NBA and EuroLeague

---

## Repository Structure

```
shooting-profiles-nba-euroleague/
├── notebooks/
│   └── shooting_profiles_travel_reproducibility.ipynb   # Full analysis pipeline
├── data/
│   ├── shot_level_scored.csv          # Migrant shot-level data with out-of-fold sxSV
│   ├── player_season_boxscore.csv     # NBA and EuroLeague player-season box scores
│   ├── migration_episodes.csv         # 589 NBA-EuroLeague migration episodes
│   ├── players.csv                    # Player index with position, height, birth year
│   ├── control_pool_nba.csv           # NBA non-migrant seasons (matched-control pool)
│   ├── sxsv_model_metrics.csv         # Out-of-fold sxSV model performance
│   └── sxsv_calibration_bins.csv      # Reliability-curve bins for the sxSV models
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Reproducing the Results

The statistical results reported in the paper can be reproduced from the provided data
files without any additional data access. The one exception is noted below.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Open `notebooks/shooting_profiles_travel_reproducibility.ipynb`
3. Run all cells from top to bottom
4. The final cell (**Paper Statistics Extraction**) prints all reported numbers

The notebook covers, in order: sxSV model performance, sample construction, included
vs excluded episodes, within-player pre-post changes, attempt-threshold sensitivity,
the matched-control comparison of changes, dependence robustness, direct vs
one-season-gap transitions, playing time and usage, player-season shooting profiles by
league, profile transferability, repeated-measures models, and the exploratory cluster
and random-forest analyses.

**Not reproducible from this repository:** fitting the sxSV models themselves, and
therefore the temporal-validation robustness check. That step needs the full shot
populations of both leagues, which are too large to distribute here (see below). The
fitted out-of-fold predictions those models produced are included, so every analysis
built on sxSV is reproducible.

---

## Notes on the Data

**Spatial expected shot value (sxSV).** `shot_level_scored.csv` carries out-of-fold
predicted make probabilities for every migrant field-goal attempt, under two
specifications:

- `*_harmonised` - identical predictors in both leagues (shot distance, shot angle,
  shot zone, shot value)
- `*_league_specific` - the specification used in the manuscript, which adds the
  limited context each competition's feed exposes (period for the NBA; fastbreak and
  second-chance flags for the EuroLeague)

Both are five-fold `GroupKFold` out-of-fold predictions grouped by player, fitted on
the full shot population of each league. The population files themselves (about 4.0
million NBA and 0.54 million EuroLeague attempts) are too large to distribute here;
`sxsv_model_metrics.csv` and `sxsv_calibration_bins.csv` report what those fits
produced, and the shot-level file carries the resulting predictions used downstream.

**Sample sizes.** The broad box-score migration sample contains 589 episodes from 283
players. The shot-coordinate subsample used for the spatial analysis is smaller,
because EuroLeague shot coordinates are available only from 2007/08 and both sides of
an episode must clear the attempt threshold: 31 episodes from 11 players at the
primary 100-attempt threshold. Because direct and one-season-gap transitions are both
retained, these 31 episodes correspond to 19 distinct moves. The notebook reports
results under player-clustered, one-episode-per-move and one-episode-per-player
restrictions alongside the full sample.

**Source data.** EuroLeague data were collected from the public EuroLeague API
(`api-live.euroleague.net`); NBA data from `stats.nba.com` via the `nba_api` package.
The files here are the processed, analysis-ready outputs of that collection.

---

## Citation

> *Will be updated upon publication.*

---

## License

Code released under the [MIT License](LICENSE).
