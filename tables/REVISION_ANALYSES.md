# Supplementary analyses for the revision

Manuscript: *Do Shooting Profiles Travel? Shot Selection, Shot Quality, and Performance Adaptation Between the NBA and EuroLeague* (RPAN-2026-0646).

All tables were produced by `step1_sxsv.py` and `step2_reviewer_analyses.py` against the `nba_euroleague` database. Every sxSV estimate is an out-of-fold prediction from a five-fold GroupKFold grouped by player, fitted on the full shot population of the respective league.

## Reviewer 3.2 / 3.3 - Harmonised sxSV specification

### `sxsv_model_metrics.csv`

Out-of-fold sxSV model performance: harmonised (identical predictors in both leagues) vs the league-specific specification used in the submitted paper. Five-fold GroupKFold grouped by player on the full shot population of each league.

| spec            | league     | features                                               |       N |   n_players |    AUC |   LogLoss |   Brier |    ECE |
|:----------------|:-----------|:-------------------------------------------------------|--------:|------------:|-------:|----------:|--------:|-------:|
| harmonised      | NBA        | dist_m,angle,zone_h,shot_value                         | 4010977 |        2470 | 0.6292 |    0.6561 |  0.2321 | 0.0011 |
| harmonised      | EuroLeague | dist_m,angle,zone_h,shot_value                         |  540415 |        2057 | 0.6506 |    0.6361 |  0.2238 | 0.001  |
| league_specific | NBA        | dist_m,angle,zone_h,shot_value,period                  | 4010977 |        2470 | 0.6299 |    0.656  |  0.232  | 0.001  |
| league_specific | EuroLeague | dist_m,angle,zone_h,shot_value,fastbreak,second_chance |  540415 |        2057 | 0.6873 |    0.5863 |  0.2059 | 0.001  |

### `C3_primary_harmonised_vs_leaguespecific.csv`

Primary (>=100 FGA, 31 episodes) pre-post results under both sxSV specifications.

| spec            | group     | metric        |   n |   mean_pre |   mean_post |   mean_delta |   ci_lo |   ci_hi |   rank_biserial |   wilcoxon_p |
|:----------------|:----------|:--------------|----:|-----------:|------------:|-------------:|--------:|--------:|----------------:|-------------:|
| harmonised      | ALL       | efg           |  31 |     0.5157 |      0.493  |      -0.0226 | -0.0489 |  0.0038 |         -0.0968 |       0.1757 |
| harmonised      | ALL       | pps           |  31 |     1.0313 |      0.986  |      -0.0453 | -0.0978 |  0.0076 |         -0.0968 |       0.1757 |
| harmonised      | ALL       | sxsv          |  31 |     1.0345 |      1.0253 |      -0.0092 | -0.0312 |  0.0111 |         -0.0968 |       0.5294 |
| harmonised      | ALL       | smoe          |  31 |     0.0008 |     -0.0143 |      -0.0151 | -0.0354 |  0.0045 |         -0.0968 |       0.3271 |
| harmonised      | ALL       | three_rate    |  31 |     0.4653 |      0.4415 |      -0.0238 | -0.0899 |  0.0392 |          0.0968 |       0.8092 |
| harmonised      | ALL       | mean_dist     |  31 |     4.9399 |      4.8466 |      -0.0933 | -0.4525 |  0.2547 |          0.0323 |       0.8393 |
| harmonised      | ALL       | pps_over_sxsv |  31 |    -0.0032 |     -0.0393 |      -0.0361 | -0.0853 |  0.0123 |         -0.1613 |       0.3468 |
| harmonised      | EL_to_NBA | efg           |  19 |     0.5404 |      0.489  |      -0.0513 | -0.0845 | -0.0164 |         -0.4737 |       0.0124 |
| harmonised      | EL_to_NBA | pps           |  19 |     1.0807 |      0.9781 |      -0.1026 | -0.1689 | -0.0329 |         -0.4737 |       0.0124 |
| harmonised      | EL_to_NBA | sxsv          |  19 |     1.0371 |      1.0255 |      -0.0115 | -0.0418 |  0.0158 |         -0.0526 |       0.6226 |
| harmonised      | EL_to_NBA | smoe          |  19 |     0.0197 |     -0.0158 |      -0.0355 | -0.0615 | -0.0092 |         -0.4737 |       0.0204 |
| harmonised      | EL_to_NBA | three_rate    |  19 |     0.4863 |      0.4581 |      -0.0283 | -0.1145 |  0.0575 |         -0.0526 |       0.7086 |
| harmonised      | EL_to_NBA | mean_dist     |  19 |     4.976  |      4.9305 |      -0.0455 | -0.4999 |  0.4283 |         -0.0526 |       0.8906 |
| harmonised      | EL_to_NBA | pps_over_sxsv |  19 |     0.0436 |     -0.0475 |      -0.0911 | -0.1524 | -0.0283 |         -0.6842 |       0.0095 |
| harmonised      | NBA_to_EL | efg           |  12 |     0.4766 |      0.4993 |       0.0228 | -0.0039 |  0.05   |          0.5    |       0.1763 |
| harmonised      | NBA_to_EL | pps           |  12 |     0.9531 |      0.9987 |       0.0456 | -0.0079 |  0.1    |          0.5    |       0.1763 |
| harmonised      | NBA_to_EL | sxsv          |  12 |     1.0305 |      1.025  |      -0.0054 | -0.0351 |  0.0232 |         -0.1667 |       0.791  |
| harmonised      | NBA_to_EL | smoe          |  12 |    -0.029  |     -0.012  |       0.017  | -0.0044 |  0.0368 |          0.5    |       0.1294 |
| harmonised      | NBA_to_EL | three_rate    |  12 |     0.4321 |      0.4153 |      -0.0168 | -0.1267 |  0.0793 |          0.3333 |       0.6772 |
| harmonised      | NBA_to_EL | mean_dist     |  12 |     4.8829 |      4.7138 |      -0.1691 | -0.7657 |  0.3688 |          0.1667 |       0.9697 |
| harmonised      | NBA_to_EL | pps_over_sxsv |  12 |    -0.0773 |     -0.0264 |       0.051  |  0.0013 |  0.0964 |          0.6667 |       0.0522 |
| league_specific | ALL       | efg           |  31 |     0.5157 |      0.493  |      -0.0226 | -0.0489 |  0.0038 |         -0.0968 |       0.1757 |
| league_specific | ALL       | pps           |  31 |     1.0313 |      0.986  |      -0.0453 | -0.0978 |  0.0076 |         -0.0968 |       0.1757 |
| league_specific | ALL       | sxsv          |  31 |     1.0294 |      1.0192 |      -0.0102 | -0.0353 |  0.0157 |         -0.4194 |       0.3176 |
| league_specific | ALL       | smoe          |  31 |     0.0031 |     -0.0117 |      -0.0148 | -0.0353 |  0.005  |         -0.0968 |       0.2639 |
| league_specific | ALL       | three_rate    |  31 |     0.4653 |      0.4415 |      -0.0238 | -0.0899 |  0.0392 |          0.0968 |       0.8092 |
| league_specific | ALL       | mean_dist     |  31 |     4.9399 |      4.8466 |      -0.0933 | -0.4525 |  0.2547 |          0.0323 |       0.8393 |
| league_specific | ALL       | pps_over_sxsv |  31 |     0.0019 |     -0.0331 |      -0.0351 | -0.0843 |  0.0129 |         -0.0968 |       0.3082 |
| league_specific | EL_to_NBA | efg           |  19 |     0.5404 |      0.489  |      -0.0513 | -0.0845 | -0.0164 |         -0.4737 |       0.0124 |
| league_specific | EL_to_NBA | pps           |  19 |     1.0807 |      0.9781 |      -0.1026 | -0.1689 | -0.0329 |         -0.4737 |       0.0124 |
| league_specific | EL_to_NBA | sxsv          |  19 |     1.0306 |      1.0227 |      -0.0079 | -0.0379 |  0.0239 |         -0.4737 |       0.3955 |
| league_specific | EL_to_NBA | smoe          |  19 |     0.0227 |     -0.0147 |      -0.0373 | -0.0619 | -0.0129 |         -0.4737 |       0.0108 |
| league_specific | EL_to_NBA | three_rate    |  19 |     0.4863 |      0.4581 |      -0.0283 | -0.1145 |  0.0575 |         -0.0526 |       0.7086 |
| league_specific | EL_to_NBA | mean_dist     |  19 |     4.976  |      4.9305 |      -0.0455 | -0.4999 |  0.4283 |         -0.0526 |       0.8906 |
| league_specific | EL_to_NBA | pps_over_sxsv |  19 |     0.0501 |     -0.0446 |      -0.0947 | -0.1521 | -0.0358 |         -0.4737 |       0.0095 |
| league_specific | NBA_to_EL | efg           |  12 |     0.4766 |      0.4993 |       0.0228 | -0.0039 |  0.05   |          0.5    |       0.1763 |
| league_specific | NBA_to_EL | pps           |  12 |     0.9531 |      0.9987 |       0.0456 | -0.0079 |  0.1    |          0.5    |       0.1763 |
| league_specific | NBA_to_EL | sxsv          |  12 |     1.0275 |      1.0137 |      -0.0139 | -0.0565 |  0.0291 |         -0.3333 |       0.6221 |
| league_specific | NBA_to_EL | smoe          |  12 |    -0.0279 |     -0.007  |       0.0209 | -0.0035 |  0.0433 |          0.5    |       0.1294 |
| league_specific | NBA_to_EL | three_rate    |  12 |     0.4321 |      0.4153 |      -0.0168 | -0.1267 |  0.0793 |          0.3333 |       0.6772 |
| league_specific | NBA_to_EL | mean_dist     |  12 |     4.8829 |      4.7138 |      -0.1691 | -0.7657 |  0.3688 |          0.1667 |       0.9697 |
| league_specific | NBA_to_EL | pps_over_sxsv |  12 |    -0.0744 |     -0.015  |       0.0594 |  0.006  |  0.1075 |          0.5    |       0.0522 |

### `H4_spec_agreement_corrected.csv`

Episode-level agreement between the two sxSV specifications in the primary sample.

|   n_episodes |   pearson_r_sxSV_pre |   pearson_r_sxSV_post |   pearson_r_delta_sxSV |   spearman_r_delta_sxSV |   mean_delta_harmonised |   mean_delta_league_specific |   mean_abs_diff_delta |   sign_agreement_% |
|-------------:|---------------------:|----------------------:|-----------------------:|------------------------:|------------------------:|-----------------------------:|----------------------:|-------------------:|
|           31 |               0.9361 |                 0.978 |                 0.8157 |                  0.8395 |                 -0.0092 |                      -0.0102 |                0.0377 |             83.871 |

### `H5_player_season_spec_agreement.csv`

Player-season sxSV under the two specifications, by league.

| league     |   n_player_seasons |   pearson_r_sxSV |   spearman_r_sxSV |   mean_sxSV_harmonised |   mean_sxSV_league_specific |   mean_abs_diff |
|:-----------|-------------------:|-----------------:|------------------:|-----------------------:|----------------------------:|----------------:|
| EuroLeague |                308 |           0.8967 |            0.9066 |                 1.0759 |                      1.0614 |          0.0422 |
| NBA        |                120 |           0.9989 |            0.998  |                 1.0273 |                      1.0269 |          0.0025 |

## Reviewer 3.8 - Flow diagram and included vs excluded

### `A_flow_counts.csv`

Sample flow from database to primary analysis sample.

| stage                                         |    n |   NBA→EL |   EL→NBA | note                                                |
|:----------------------------------------------|-----:|---------:|---------:|:----------------------------------------------------|
| Players in cross-league database              | 3075 |      nan |      nan | EL players 2000/01+ matched against full NBA index  |
| Players identified as cross-league migrants   |  402 |      nan |      nan | name + date-of-birth confirmed                      |
| Migration episodes detected (all season gaps) |  589 |      346 |      243 | nan                                                 |
| Migration episodes retained (gap 0 or 1)      |  589 |      346 |      243 | analysis population; unique players = 283           |
| … with box-score season data on both sides    |  589 |      346 |      243 | broad box-score migration sample                    |
| … with any shot-coordinate data on both sides |   83 |       46 |       37 | EuroLeague shot coordinates exist from 2007/08 only |
| … passing ≥50 FGA on BOTH sides               |   46 |       24 |       22 | sensitivity; unique players = 16                    |
| … passing ≥100 FGA on BOTH sides              |   31 |       12 |       19 | PRIMARY analysis sample; unique players = 11        |
| … passing ≥150 FGA on BOTH sides              |   19 |        4 |       15 | sensitivity; unique players = 9                     |
| … passing ≥200 FGA on BOTH sides              |   12 |        2 |       10 | sensitivity; unique players = 6                     |

### `A2_exclusion_reasons.csv`

Why episodes drop out of the primary sample.

| reason                                 |   EL_to_NBA |   NBA_to_EL |   total |
|:---------------------------------------|------------:|------------:|--------:|
| no shot-coordinate data on either side |          92 |         108 |     200 |
| no shot-coordinate data on one side    |         114 |         192 |     306 |
| shot data on both sides but <100 FGA   |          18 |          34 |      52 |

### `B_included_vs_excluded_continuous.csv`

Included (n=31) vs excluded episodes on continuous covariates, with standardised mean differences and Mann-Whitney tests.

| variable                         |   n_incl |   incl_mean |   incl_sd |   n_excl |   excl_mean |   excl_sd |     SMD |   MWU_p |   avail_incl_% |   avail_excl_% |
|:---------------------------------|---------:|------------:|----------:|---------:|------------:|----------:|--------:|--------:|---------------:|---------------:|
| Age at migration (years)         |       31 |     28.6452 |    3.536  |      558 |     26.3889 |    3.8159 |  0.6133 |  0.0003 |       100      |       100      |
| Height (cm)                      |       31 |    199.839  |    9.1837 |      554 |    201.852  |    9.3577 | -0.2172 |  0.2456 |       100      |        99.2832 |
| Games played (origin season)     |       31 |     36.6129 |   14.5457 |      558 |     25.8297 |   20.9035 |  0.5988 |  0.0001 |       100      |       100      |
| Minutes per game (origin season) |       31 |     20.8078 |    5.7819 |      469 |     15.3919 |    8.2719 |  0.7589 |  0.0001 |       100      |        84.0502 |
| FGA per game (origin season)     |       31 |      6.8539 |    2.7027 |      469 |      4.8252 |    3.087  |  0.6992 |  0.0001 |       100      |        84.0502 |
| eFG (origin season, 0-1)         |       31 |      0.5108 |    0.0684 |      553 |      0.4685 |    0.1342 |  0.3974 |  0.0379 |       100      |        99.1039 |
| 3P% (origin season, 0-100)       |       31 |     34.901  |    6.9815 |      500 |     25.8127 |   18.1262 |  0.6617 |  0.0035 |       100      |        89.6057 |
| Points per game (origin season)  |       31 |      8.6226 |    3.8949 |      469 |      5.9062 |    4.4194 |  0.6521 |  0.0001 |       100      |        84.0502 |
| FGA per game (season t−1)        |       21 |      7.0681 |    2.2685 |      308 |      5.4159 |    2.9239 |  0.6314 |  0.0045 |        67.7419 |        55.1971 |
| eFG (season t−1, 0-1)            |       22 |      0.5196 |    0.0554 |      336 |      0.4863 |    0.1086 |  0.3862 |  0.0739 |        70.9677 |        60.2151 |
| 3P% (season t−1, 0-100)          |       22 |     36.0418 |    7.473  |      312 |     27.2129 |   17.5198 |  0.6555 |  0.0154 |        70.9677 |        55.914  |

### `B2_included_vs_excluded_categorical.csv`

Included vs excluded episodes on position and migration direction.

| variable   | level            |   included_n |   included_% |   excluded_n |   excluded_% |
|:-----------|:-----------------|-------------:|-------------:|-------------:|-------------:|
| position   | Center           |            7 |      22.5806 |          136 |      24.3728 |
| position   | Forward          |            6 |      19.3548 |          218 |      39.0681 |
| position   | Guard            |           18 |      58.0645 |          204 |      36.5591 |
| position   | - chi-square p - |          nan |     nan      |          nan |       0.0361 |
| direction  | EL_to_NBA        |           19 |      61.2903 |          224 |      40.1434 |
| direction  | NBA_to_EL        |           12 |      38.7097 |          334 |      59.8566 |
| direction  | - chi-square p - |          nan |     nan      |          nan |       0.0323 |

## Reviewer 3.10 / 3.23 - FGA-threshold sensitivity

### `C1_threshold_sample_sizes.csv`

Paired sample size at each threshold.

| spec            |   threshold |   n_episodes |   n_players |   n_NBA→EL |   n_EL→NBA |   median_FGA_pre |   median_FGA_post |
|:----------------|------------:|-------------:|------------:|-----------:|-----------:|-----------------:|------------------:|
| harmonised      |          50 |           46 |          16 |         24 |         22 |            210   |             197   |
| harmonised      |         100 |           31 |          11 |         12 |         19 |            229   |             312   |
| harmonised      |         150 |           19 |           9 |          4 |         15 |            231   |             321   |
| harmonised      |         200 |           12 |           6 |          2 |         10 |            260.5 |             330.5 |
| league_specific |          50 |           46 |          16 |         24 |         22 |            210   |             197   |
| league_specific |         100 |           31 |          11 |         12 |         19 |            229   |             312   |
| league_specific |         150 |           19 |           9 |          4 |         15 |            231   |             321   |
| league_specific |         200 |           12 |           6 |          2 |         10 |            260.5 |             330.5 |

### `C2_threshold_sensitivity_core.csv`

Mean change in eFG, PPS, sxSV and SMOE at 50/100/150/200 FGA, overall and by direction, with bootstrap 95% CIs.

| spec            |   threshold | group     | metric   |   n |   n_players |   mean_delta |   ci_lo |   ci_hi |   rank_biserial |   wilcoxon_p |
|:----------------|------------:|:----------|:---------|----:|------------:|-------------:|--------:|--------:|----------------:|-------------:|
| harmonised      |          50 | ALL       | efg      |  46 |          16 |      -0.0067 | -0.0313 |  0.0178 |         -0.087  |       0.5807 |
| harmonised      |          50 | ALL       | pps      |  46 |          16 |      -0.0133 | -0.0625 |  0.0356 |         -0.087  |       0.5807 |
| harmonised      |          50 | ALL       | sxsv     |  46 |          16 |      -0.026  | -0.0565 | -0      |         -0.2174 |       0.1634 |
| harmonised      |          50 | ALL       | smoe     |  46 |          16 |       0.0037 | -0.0138 |  0.0201 |          0.087  |       0.4351 |
| harmonised      |          50 | EL_to_NBA | efg      |  22 |          11 |      -0.0309 | -0.069  |  0.0082 |         -0.3636 |       0.1129 |
| harmonised      |          50 | EL_to_NBA | pps      |  22 |          11 |      -0.0617 | -0.1379 |  0.0164 |         -0.3636 |       0.1129 |
| harmonised      |          50 | EL_to_NBA | sxsv     |  22 |          11 |       0.0012 | -0.0301 |  0.0308 |          0      |       0.9493 |
| harmonised      |          50 | EL_to_NBA | smoe     |  22 |          11 |      -0.0253 | -0.0508 | -0.0005 |         -0.3636 |       0.0917 |
| harmonised      |          50 | NBA_to_EL | efg      |  24 |          14 |       0.0155 | -0.0147 |  0.0454 |          0.1667 |       0.3902 |
| harmonised      |          50 | NBA_to_EL | pps      |  24 |          14 |       0.031  | -0.0293 |  0.0908 |          0.1667 |       0.3902 |
| harmonised      |          50 | NBA_to_EL | sxsv     |  24 |          14 |      -0.0509 | -0.1008 | -0.0112 |         -0.4167 |       0.0491 |
| harmonised      |          50 | NBA_to_EL | smoe     |  24 |          14 |       0.0302 |  0.0133 |  0.047  |          0.5    |       0.0028 |
| harmonised      |         100 | ALL       | efg      |  31 |          11 |      -0.0226 | -0.0489 |  0.0038 |         -0.0968 |       0.1757 |
| harmonised      |         100 | ALL       | pps      |  31 |          11 |      -0.0453 | -0.0978 |  0.0076 |         -0.0968 |       0.1757 |
| harmonised      |         100 | ALL       | sxsv     |  31 |          11 |      -0.0092 | -0.0312 |  0.0111 |         -0.0968 |       0.5294 |
| harmonised      |         100 | ALL       | smoe     |  31 |          11 |      -0.0151 | -0.0354 |  0.0045 |         -0.0968 |       0.3271 |
| harmonised      |         100 | EL_to_NBA | efg      |  19 |          11 |      -0.0513 | -0.0845 | -0.0164 |         -0.4737 |       0.0124 |
| harmonised      |         100 | EL_to_NBA | pps      |  19 |          11 |      -0.1026 | -0.1689 | -0.0329 |         -0.4737 |       0.0124 |
| harmonised      |         100 | EL_to_NBA | sxsv     |  19 |          11 |      -0.0115 | -0.0418 |  0.0158 |         -0.0526 |       0.6226 |
| harmonised      |         100 | EL_to_NBA | smoe     |  19 |          11 |      -0.0355 | -0.0615 | -0.0092 |         -0.4737 |       0.0204 |
| harmonised      |         100 | NBA_to_EL | efg      |  12 |           8 |       0.0228 | -0.0039 |  0.05   |          0.5    |       0.1763 |
| harmonised      |         100 | NBA_to_EL | pps      |  12 |           8 |       0.0456 | -0.0079 |  0.1    |          0.5    |       0.1763 |
| harmonised      |         100 | NBA_to_EL | sxsv     |  12 |           8 |      -0.0054 | -0.0351 |  0.0232 |         -0.1667 |       0.791  |
| harmonised      |         100 | NBA_to_EL | smoe     |  12 |           8 |       0.017  | -0.0044 |  0.0368 |          0.5    |       0.1294 |
| harmonised      |         150 | ALL       | efg      |  19 |           9 |      -0.0421 | -0.0753 | -0.0103 |         -0.3684 |       0.023  |
| harmonised      |         150 | ALL       | pps      |  19 |           9 |      -0.0843 | -0.1506 | -0.0207 |         -0.3684 |       0.023  |
| harmonised      |         150 | ALL       | sxsv     |  19 |           9 |      -0.009  | -0.0397 |  0.0171 |         -0.0526 |       0.7983 |
| harmonised      |         150 | ALL       | smoe     |  19 |           9 |      -0.0272 | -0.051  | -0.0047 |         -0.3684 |       0.0446 |
| harmonised      |         150 | EL_to_NBA | efg      |  15 |           9 |      -0.0623 | -0.0975 | -0.0316 |         -0.6    |       0.0012 |
| harmonised      |         150 | EL_to_NBA | pps      |  15 |           9 |      -0.1247 | -0.195  | -0.0632 |         -0.6    |       0.0012 |
| harmonised      |         150 | EL_to_NBA | sxsv     |  15 |           9 |      -0.0186 | -0.0515 |  0.0132 |         -0.2    |       0.3894 |
| harmonised      |         150 | EL_to_NBA | smoe     |  15 |           9 |      -0.0384 | -0.0644 | -0.0158 |         -0.6    |       0.0043 |
| harmonised      |         150 | NBA_to_EL | efg      |   4 |           3 |       0.0337 | -0.0096 |  0.077  |          0.5    |       0.375  |
| harmonised      |         150 | NBA_to_EL | pps      |   4 |           3 |       0.0674 | -0.0191 |  0.154  |          0.5    |       0.375  |
| harmonised      |         150 | NBA_to_EL | sxsv     |   4 |           3 |       0.027  |  0.0011 |  0.0476 |          0.5    |       0.25   |
| harmonised      |         150 | NBA_to_EL | smoe     |   4 |           3 |       0.015  | -0.0293 |  0.0536 |          0.5    |       0.625  |
| harmonised      |         200 | ALL       | efg      |  12 |           6 |      -0.0254 | -0.0512 |  0.0026 |         -0.1667 |       0.1514 |
| harmonised      |         200 | ALL       | pps      |  12 |           6 |      -0.0507 | -0.1025 |  0.0052 |         -0.1667 |       0.1514 |
| harmonised      |         200 | ALL       | sxsv     |  12 |           6 |      -0.0252 | -0.0633 |  0.0089 |         -0.1667 |       0.4238 |
| harmonised      |         200 | ALL       | smoe     |  12 |           6 |      -0.0048 | -0.0195 |  0.0118 |         -0.1667 |       0.4697 |
| harmonised      |         200 | EL_to_NBA | efg      |  10 |           6 |      -0.0381 | -0.0626 | -0.0128 |         -0.4    |       0.0273 |
| harmonised      |         200 | EL_to_NBA | pps      |  10 |           6 |      -0.0761 | -0.1253 | -0.0256 |         -0.4    |       0.0273 |
| harmonised      |         200 | EL_to_NBA | sxsv     |  10 |           6 |      -0.0317 | -0.0779 |  0.0085 |         -0.2    |       0.3223 |
| harmonised      |         200 | EL_to_NBA | smoe     |  10 |           6 |      -0.0127 | -0.0249 | -0.0001 |         -0.4    |       0.1309 |
| league_specific |          50 | ALL       | efg      |  46 |          16 |      -0.0067 | -0.0313 |  0.0178 |         -0.087  |       0.5807 |
| league_specific |          50 | ALL       | pps      |  46 |          16 |      -0.0133 | -0.0625 |  0.0356 |         -0.087  |       0.5807 |
| league_specific |          50 | ALL       | sxsv     |  46 |          16 |      -0.027  | -0.064  |  0.0051 |         -0.3478 |       0.2071 |
| league_specific |          50 | ALL       | smoe     |  46 |          16 |       0.0045 | -0.0141 |  0.0227 |          0.1304 |       0.5298 |
| league_specific |          50 | EL_to_NBA | efg      |  22 |          11 |      -0.0309 | -0.069  |  0.0082 |         -0.3636 |       0.1129 |
| league_specific |          50 | EL_to_NBA | pps      |  22 |          11 |      -0.0617 | -0.1379 |  0.0164 |         -0.3636 |       0.1129 |
| league_specific |          50 | EL_to_NBA | sxsv     |  22 |          11 |       0.0073 | -0.0271 |  0.0441 |         -0.3636 |       0.8486 |
| league_specific |          50 | EL_to_NBA | smoe     |  22 |          11 |      -0.0279 | -0.0519 | -0.005  |         -0.2727 |       0.0501 |
| league_specific |          50 | NBA_to_EL | efg      |  24 |          14 |       0.0155 | -0.0147 |  0.0454 |          0.1667 |       0.3902 |
| league_specific |          50 | NBA_to_EL | pps      |  24 |          14 |       0.031  | -0.0293 |  0.0908 |          0.1667 |       0.3902 |
| league_specific |          50 | NBA_to_EL | sxsv     |  24 |          14 |      -0.0585 | -0.1198 | -0.0074 |         -0.3333 |       0.1074 |
| league_specific |          50 | NBA_to_EL | smoe     |  24 |          14 |       0.0342 |  0.0131 |  0.0559 |          0.5    |       0.0072 |
| league_specific |         100 | ALL       | efg      |  31 |          11 |      -0.0226 | -0.0489 |  0.0038 |         -0.0968 |       0.1757 |
| league_specific |         100 | ALL       | pps      |  31 |          11 |      -0.0453 | -0.0978 |  0.0076 |         -0.0968 |       0.1757 |
| league_specific |         100 | ALL       | sxsv     |  31 |          11 |      -0.0102 | -0.0353 |  0.0157 |         -0.4194 |       0.3176 |
| league_specific |         100 | ALL       | smoe     |  31 |          11 |      -0.0148 | -0.0353 |  0.005  |         -0.0968 |       0.2639 |
| league_specific |         100 | EL_to_NBA | efg      |  19 |          11 |      -0.0513 | -0.0845 | -0.0164 |         -0.4737 |       0.0124 |
| league_specific |         100 | EL_to_NBA | pps      |  19 |          11 |      -0.1026 | -0.1689 | -0.0329 |         -0.4737 |       0.0124 |
| league_specific |         100 | EL_to_NBA | sxsv     |  19 |          11 |      -0.0079 | -0.0379 |  0.0239 |         -0.4737 |       0.3955 |
| league_specific |         100 | EL_to_NBA | smoe     |  19 |          11 |      -0.0373 | -0.0619 | -0.0129 |         -0.4737 |       0.0108 |
| league_specific |         100 | NBA_to_EL | efg      |  12 |           8 |       0.0228 | -0.0039 |  0.05   |          0.5    |       0.1763 |
| league_specific |         100 | NBA_to_EL | pps      |  12 |           8 |       0.0456 | -0.0079 |  0.1    |          0.5    |       0.1763 |
| league_specific |         100 | NBA_to_EL | sxsv     |  12 |           8 |      -0.0139 | -0.0565 |  0.0291 |         -0.3333 |       0.6221 |
| league_specific |         100 | NBA_to_EL | smoe     |  12 |           8 |       0.0209 | -0.0035 |  0.0433 |          0.5    |       0.1294 |
| league_specific |         150 | ALL       | efg      |  19 |           9 |      -0.0421 | -0.0753 | -0.0103 |         -0.3684 |       0.023  |
| league_specific |         150 | ALL       | pps      |  19 |           9 |      -0.0843 | -0.1506 | -0.0207 |         -0.3684 |       0.023  |
| league_specific |         150 | ALL       | sxsv     |  19 |           9 |      -0.0167 | -0.0443 |  0.0117 |         -0.5789 |       0.1336 |
| league_specific |         150 | ALL       | smoe     |  19 |           9 |      -0.0243 | -0.0475 | -0.0012 |         -0.3684 |       0.0663 |
| league_specific |         150 | EL_to_NBA | efg      |  15 |           9 |      -0.0623 | -0.0975 | -0.0316 |         -0.6    |       0.0012 |
| league_specific |         150 | EL_to_NBA | pps      |  15 |           9 |      -0.1247 | -0.195  | -0.0632 |         -0.6    |       0.0012 |
| league_specific |         150 | EL_to_NBA | sxsv     |  15 |           9 |      -0.027  | -0.0562 |  0.0055 |         -0.7333 |       0.0413 |
| league_specific |         150 | EL_to_NBA | smoe     |  15 |           9 |      -0.0359 | -0.0597 | -0.0151 |         -0.6    |       0.0043 |
| league_specific |         150 | NBA_to_EL | efg      |   4 |           3 |       0.0337 | -0.0096 |  0.077  |          0.5    |       0.375  |
| league_specific |         150 | NBA_to_EL | pps      |   4 |           3 |       0.0674 | -0.0191 |  0.154  |          0.5    |       0.375  |
| league_specific |         150 | NBA_to_EL | sxsv     |   4 |           3 |       0.0217 | -0.0312 |  0.0745 |          0      |       0.625  |
| league_specific |         150 | NBA_to_EL | smoe     |   4 |           3 |       0.0191 | -0.0403 |  0.0656 |          0.5    |       0.625  |
| league_specific |         200 | ALL       | efg      |  12 |           6 |      -0.0254 | -0.0512 |  0.0026 |         -0.1667 |       0.1514 |
| league_specific |         200 | ALL       | pps      |  12 |           6 |      -0.0507 | -0.1025 |  0.0052 |         -0.1667 |       0.1514 |
| league_specific |         200 | ALL       | sxsv     |  12 |           6 |      -0.0364 | -0.0608 | -0.0135 |         -0.8333 |       0.0122 |
| league_specific |         200 | ALL       | smoe     |  12 |           6 |      -0.0009 | -0.0164 |  0.0184 |         -0.1667 |       0.6221 |
| league_specific |         200 | EL_to_NBA | efg      |  10 |           6 |      -0.0381 | -0.0626 | -0.0128 |         -0.4    |       0.0273 |
| league_specific |         200 | EL_to_NBA | pps      |  10 |           6 |      -0.0761 | -0.1253 | -0.0256 |         -0.4    |       0.0273 |
| league_specific |         200 | EL_to_NBA | sxsv     |  10 |           6 |      -0.0374 | -0.067  | -0.0099 |         -0.8    |       0.0371 |
| league_specific |         200 | EL_to_NBA | smoe     |  10 |           6 |      -0.0114 | -0.0221 |  0.0001 |         -0.4    |       0.1309 |

## Reviewer 3.11 / 3.14 - Matched-control robustness

### `D1_control_pool_availability.csv`

Covariate availability in each control pool.

| pool                                                                  |   n_player_seasons |   fga_per_game_% |   efg_pct_% |   three_pt_pct_% |   minutes_per_game_% |   age_% |   position_% |   experience_% |   season_% |
|:----------------------------------------------------------------------|-------------------:|-----------------:|------------:|-----------------:|---------------------:|--------:|-------------:|---------------:|-----------:|
| EuroLeague non-migrants (control pool for EL→NBA migrants)            |               2224 |              100 |         100 |              100 |                  100 |     100 |          100 |            100 |        100 |
| NBA non-migrants (NBANonMigrantSeasons; controls for NBA→EL migrants) |               6183 |              100 |         100 |              100 |                    0 |       0 |            0 |            100 |        100 |

### `D2_did_covariate_sets.csv`

Matched-control DiD under base and extended matching covariate sets.

| direction   | matching                                      | outcome      |   n_episodes |   n_players |   migrant_delta |   control_delta |     DiD |    ci_lo |   ci_hi |   ci_lo_clustered |   ci_hi_clustered |   wilcoxon_p | covariates_used                                                   | covariates_dropped   |   control_pool_n |
|:------------|:----------------------------------------------|:-------------|-------------:|------------:|----------------:|----------------:|--------:|---------:|--------:|------------------:|------------------:|-------------:|:------------------------------------------------------------------|:---------------------|-----------------:|
| EL_to_NBA   | base (paper)                                  | efg_pct      |          128 |          87 |         -0.0675 |         -0.0052 | -0.0635 |  -0.0832 | -0.0455 |           -0.0863 |           -0.043  |       0      | fga_per_game+efg_pct+three_pt_pct                                 | -                    |             2224 |
| EL_to_NBA   | base (paper)                                  | three_pt_pct |          110 |          79 |         -8.4862 |          0.4269 | -7.8111 | -10.3765 | -5.3287 |          -10.9086 |           -4.8067 |       0      | fga_per_game+efg_pct+three_pt_pct                                 | -                    |             2224 |
| EL_to_NBA   | base (paper)                                  | fga_per_game |           47 |          39 |         -2.9895 |         -0.8119 | -2.8749 |  -3.7711 | -2.03   |           -3.9382 |           -1.9004 |       0      | fga_per_game+efg_pct+three_pt_pct                                 | -                    |             2224 |
| EL_to_NBA   | base (paper) + exact position                 | efg_pct      |          130 |          87 |         -0.0675 |         -0.01   | -0.0556 |  -0.0735 | -0.0387 |           -0.0755 |           -0.0365 |       0      | fga_per_game+efg_pct+three_pt_pct                                 | -                    |             2224 |
| EL_to_NBA   | base (paper) + exact position                 | three_pt_pct |          105 |          74 |         -8.4862 |         -0.5112 | -7.7143 | -10.5883 | -4.9184 |          -11.1068 |           -4.3538 |       0      | fga_per_game+efg_pct+three_pt_pct                                 | -                    |             2224 |
| EL_to_NBA   | base (paper) + exact position                 | fga_per_game |           40 |          32 |         -2.9895 |         -0.726  | -2.35   |  -3.1883 | -1.5152 |           -3.4208 |           -1.4477 |       0      | fga_per_game+efg_pct+three_pt_pct                                 | -                    |             2224 |
| EL_to_NBA   | + minutes                                     | efg_pct      |          127 |          85 |         -0.0675 |         -0.0076 | -0.0597 |  -0.0784 | -0.0418 |           -0.0821 |           -0.0396 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game                | -                    |             2224 |
| EL_to_NBA   | + minutes                                     | three_pt_pct |          108 |          77 |         -8.4862 |          0.2651 | -7.5936 | -10.0972 | -5.1788 |          -10.5984 |           -4.8684 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game                | -                    |             2224 |
| EL_to_NBA   | + minutes                                     | fga_per_game |           46 |          41 |         -2.9895 |         -0.9874 | -2.9635 |  -3.838  | -2.1019 |           -3.9337 |           -2.0097 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game                | -                    |             2224 |
| EL_to_NBA   | + minutes + exact position                    | efg_pct      |          131 |          88 |         -0.0675 |         -0.009  | -0.0563 |  -0.0728 | -0.0404 |           -0.0752 |           -0.0392 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game                | -                    |             2224 |
| EL_to_NBA   | + minutes + exact position                    | three_pt_pct |          102 |          75 |         -8.4862 |         -0.4022 | -8.2828 | -11.0859 | -5.6234 |          -11.4903 |           -5.4231 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game                | -                    |             2224 |
| EL_to_NBA   | + minutes + exact position                    | fga_per_game |           43 |          39 |         -2.9895 |         -0.5456 | -2.1135 |  -2.8547 | -1.3272 |           -2.9044 |           -1.3369 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game                | -                    |             2224 |
| EL_to_NBA   | + minutes + age + experience                  | efg_pct      |          131 |          87 |         -0.0675 |         -0.0068 | -0.0621 |  -0.0812 | -0.0453 |           -0.0825 |           -0.0432 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game+age+experience | -                    |             2224 |
| EL_to_NBA   | + minutes + age + experience                  | three_pt_pct |          115 |          82 |         -8.4862 |         -0.3068 | -7.3225 | -10.021  | -4.8074 |          -10.377  |           -4.3892 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game+age+experience | -                    |             2224 |
| EL_to_NBA   | + minutes + age + experience                  | fga_per_game |           49 |          45 |         -2.9895 |         -0.622  | -3.0855 |  -4.1125 | -2.0686 |           -4.1583 |           -2.0381 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game+age+experience | -                    |             2224 |
| EL_to_NBA   | + minutes + age + experience + exact position | efg_pct      |          132 |          88 |         -0.0675 |         -0.0087 | -0.0565 |  -0.0735 | -0.0408 |           -0.0754 |           -0.0386 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game+age+experience | -                    |             2224 |
| EL_to_NBA   | + minutes + age + experience + exact position | three_pt_pct |          118 |          82 |         -8.4862 |         -0.2508 | -8.0222 | -10.5417 | -5.6709 |          -11.0238 |           -5.2363 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game+age+experience | -                    |             2224 |
| EL_to_NBA   | + minutes + age + experience + exact position | fga_per_game |           47 |          43 |         -2.9895 |         -0.4128 | -2.8909 |  -3.6867 | -2.1247 |           -3.7034 |           -2.1304 |       0      | fga_per_game+efg_pct+three_pt_pct+minutes_per_game+age+experience | -                    |             2224 |
| NBA_to_EL   | base (paper)                                  | efg_pct      |          216 |         146 |          0.0479 |          0.0247 |  0.024  |   0.0067 |  0.0405 |            0.0055 |            0.0416 |       0.0001 | fga_per_game+efg_pct+three_pt_pct                                 | -                    |             6183 |
| NBA_to_EL   | base (paper)                                  | three_pt_pct |          170 |         113 |          7.4404 |          2.1509 |  6.0799 |   3.7112 |  8.6042 |            3.5107 |            8.8599 |       0      | fga_per_game+efg_pct+three_pt_pct                                 | -                    |             6183 |
| NBA_to_EL   | base (paper)                                  | fga_per_game |          101 |          66 |          2.9002 |          0.5454 |  2.4608 |   1.8954 |  3      |            1.8117 |            3.1268 |       0      | fga_per_game+efg_pct+three_pt_pct                                 | -                    |             6183 |
| NBA_to_EL   | + minutes                                     | efg_pct      |          216 |         146 |          0.0479 |          0.0247 |  0.024  |   0.0067 |  0.0405 |            0.0055 |            0.0416 |       0.0001 | fga_per_game+efg_pct+three_pt_pct                                 | minutes_per_game     |             6183 |
| NBA_to_EL   | + minutes                                     | three_pt_pct |          170 |         113 |          7.4404 |          2.1509 |  6.0799 |   3.7112 |  8.6042 |            3.5107 |            8.8599 |       0      | fga_per_game+efg_pct+three_pt_pct                                 | minutes_per_game     |             6183 |
| NBA_to_EL   | + minutes                                     | fga_per_game |          101 |          66 |          2.9002 |          0.5454 |  2.4608 |   1.8954 |  3      |            1.8117 |            3.1268 |       0      | fga_per_game+efg_pct+three_pt_pct                                 | minutes_per_game     |             6183 |
| NBA_to_EL   | + minutes + age + experience                  | efg_pct      |          185 |         123 |          0.0537 |          0.0304 |  0.0239 |   0.0094 |  0.0386 |            0.0068 |            0.0407 |       0.0007 | fga_per_game+efg_pct+three_pt_pct+experience                      | minutes_per_game+age |             6183 |
| NBA_to_EL   | + minutes + age + experience                  | three_pt_pct |          145 |          96 |          7.2415 |          1.9923 |  6.22   |   3.9325 |  8.4939 |            3.6194 |            8.9871 |       0      | fga_per_game+efg_pct+three_pt_pct+experience                      | minutes_per_game+age |             6183 |
| NBA_to_EL   | + minutes + age + experience                  | fga_per_game |           86 |          55 |          2.6897 |          0.6255 |  2.1411 |   1.61   |  2.6724 |            1.5326 |            2.7482 |       0      | fga_per_game+efg_pct+three_pt_pct+experience                      | minutes_per_game+age |             6183 |

### `D2b_did_not_estimable.csv` - not produced

*Matching specifications that could not be estimated.*

### `D3_did_balance.csv`

Covariate balance (SMD) for each matching specification.

| direction   | matching                                      | covariate        |   migrant_mean |   matched_control_mean |   unmatched_pool_mean |   SMD_before |   SMD_after |
|:------------|:----------------------------------------------|:-----------------|---------------:|-----------------------:|----------------------:|-------------:|------------:|
| EL_to_NBA   | base (paper)                                  | fga_per_game     |         7.9526 |                 7.7744 |                6.3183 |       0.5878 |      0.0641 |
| EL_to_NBA   | base (paper)                                  | efg_pct          |         0.5342 |                 0.5328 |                0.5311 |       0.0442 |      0.0202 |
| EL_to_NBA   | base (paper)                                  | three_pt_pct     |        35.6742 |                35.8    |               36.3188 |      -0.0664 |     -0.013  |
| EL_to_NBA   | base (paper) + exact position                 | fga_per_game     |         7.9526 |                 7.7803 |                6.3183 |       0.5878 |      0.062  |
| EL_to_NBA   | base (paper) + exact position                 | efg_pct          |         0.5342 |                 0.5327 |                0.5311 |       0.0442 |      0.0211 |
| EL_to_NBA   | base (paper) + exact position                 | three_pt_pct     |        35.6742 |                35.8997 |               36.3188 |      -0.0664 |     -0.0232 |
| EL_to_NBA   | + minutes                                     | fga_per_game     |         7.9526 |                 7.7208 |                6.3183 |       0.5878 |      0.0834 |
| EL_to_NBA   | + minutes                                     | efg_pct          |         0.5342 |                 0.5321 |                0.5311 |       0.0442 |      0.03   |
| EL_to_NBA   | + minutes                                     | three_pt_pct     |        35.6742 |                35.7844 |               36.3188 |      -0.0664 |     -0.0114 |
| EL_to_NBA   | + minutes                                     | minutes_per_game |        23.9912 |                24.0327 |               21.0249 |       0.4771 |     -0.0067 |
| EL_to_NBA   | + minutes + exact position                    | fga_per_game     |         7.9526 |                 7.7478 |                6.3183 |       0.5878 |      0.0737 |
| EL_to_NBA   | + minutes + exact position                    | efg_pct          |         0.5342 |                 0.5315 |                0.5311 |       0.0442 |      0.0377 |
| EL_to_NBA   | + minutes + exact position                    | three_pt_pct     |        35.6742 |                35.8451 |               36.3188 |      -0.0664 |     -0.0176 |
| EL_to_NBA   | + minutes + exact position                    | minutes_per_game |        23.9912 |                23.98   |               21.0249 |       0.4771 |      0.0018 |
| EL_to_NBA   | + minutes + age + experience                  | fga_per_game     |         7.9526 |                 7.603  |                6.3183 |       0.5878 |      0.1258 |
| EL_to_NBA   | + minutes + age + experience                  | efg_pct          |         0.5342 |                 0.5308 |                0.5311 |       0.0442 |      0.0487 |
| EL_to_NBA   | + minutes + age + experience                  | three_pt_pct     |        35.6742 |                35.9849 |               36.3188 |      -0.0664 |     -0.032  |
| EL_to_NBA   | + minutes + age + experience                  | minutes_per_game |        23.9912 |                23.8606 |               21.0249 |       0.4771 |      0.021  |
| EL_to_NBA   | + minutes + age + experience                  | age              |        24.1429 |                24.8586 |               27.3948 |      -0.8735 |     -0.1923 |
| EL_to_NBA   | + minutes + age + experience                  | experience       |         1.8722 |                 1.9008 |                3.0337 |      -0.3859 |     -0.0095 |
| EL_to_NBA   | + minutes + age + experience + exact position | fga_per_game     |         7.9526 |                 7.5432 |                6.3183 |       0.5878 |      0.1473 |
| EL_to_NBA   | + minutes + age + experience + exact position | efg_pct          |         0.5342 |                 0.528  |                0.5311 |       0.0442 |      0.088  |
| EL_to_NBA   | + minutes + age + experience + exact position | three_pt_pct     |        35.6742 |                36.1916 |               36.3188 |      -0.0664 |     -0.0533 |
| EL_to_NBA   | + minutes + age + experience + exact position | minutes_per_game |        23.9912 |                23.7795 |               21.0249 |       0.4771 |      0.034  |
| EL_to_NBA   | + minutes + age + experience + exact position | age              |        24.1429 |                25.1669 |               27.3948 |      -0.8735 |     -0.2751 |
| EL_to_NBA   | + minutes + age + experience + exact position | experience       |         1.8722 |                 1.9248 |                3.0337 |      -0.3859 |     -0.0175 |
| NBA_to_EL   | base (paper)                                  | fga_per_game     |         3.9856 |                 4.1377 |                7.8295 |      -0.8165 |     -0.0323 |
| NBA_to_EL   | base (paper)                                  | efg_pct          |         0.4563 |                 0.4572 |                0.508  |      -0.6623 |     -0.0112 |
| NBA_to_EL   | base (paper)                                  | three_pt_pct     |        23.7475 |                23.0274 |               28.3238 |      -0.2985 |      0.047  |
| NBA_to_EL   | + minutes                                     | fga_per_game     |         3.9856 |                 4.1377 |                7.8295 |      -0.8165 |     -0.0323 |
| NBA_to_EL   | + minutes                                     | efg_pct          |         0.4563 |                 0.4572 |                0.508  |      -0.6623 |     -0.0112 |
| NBA_to_EL   | + minutes                                     | three_pt_pct     |        23.7475 |                23.0274 |               28.3238 |      -0.2985 |      0.047  |
| NBA_to_EL   | + minutes + age + experience                  | fga_per_game     |         4.0201 |                 4.188  |                7.8295 |      -0.8091 |     -0.0357 |
| NBA_to_EL   | + minutes + age + experience                  | efg_pct          |         0.4545 |                 0.4607 |                0.508  |      -0.6861 |     -0.0794 |
| NBA_to_EL   | + minutes + age + experience                  | three_pt_pct     |        23.501  |                23.1238 |               28.3238 |      -0.3146 |      0.0246 |
| NBA_to_EL   | + minutes + age + experience                  | experience       |         2.0208 |                 1.9219 |                3.2745 |      -0.3969 |      0.0313 |

### `D4_control_reuse.csv`

Effect of allowing the same control player-season into more than one matched set.

| direction   | control_sampling         | outcome      |   n_episodes |   n_players |   migrant_delta |   control_delta |     DiD |    ci_lo |   ci_hi |   ci_lo_clustered |   ci_hi_clustered |   wilcoxon_p | covariates_used                   | covariates_dropped   |   control_pool_n |
|:------------|:-------------------------|:-------------|-------------:|------------:|----------------:|----------------:|--------:|---------:|--------:|------------------:|------------------:|-------------:|:----------------------------------|:---------------------|-----------------:|
| EL_to_NBA   | with replacement (paper) | efg_pct      |          128 |          87 |         -0.0675 |         -0.0052 | -0.0635 |  -0.0832 | -0.0455 |           -0.0863 |           -0.043  |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | with replacement (paper) | three_pt_pct |          110 |          79 |         -8.4862 |          0.4269 | -7.8111 | -10.3765 | -5.3287 |          -10.9086 |           -4.8067 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | with replacement (paper) | fga_per_game |           47 |          39 |         -2.9895 |         -0.8119 | -2.8749 |  -3.7711 | -2.03   |           -3.9382 |           -1.9004 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | without replacement      | efg_pct      |          129 |          87 |         -0.0675 |         -0.0054 | -0.0632 |  -0.0813 | -0.0463 |           -0.0843 |           -0.0436 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | without replacement      | three_pt_pct |          108 |          77 |         -8.4862 |         -0.2346 | -7.1725 |  -9.6154 | -4.8004 |          -10.2249 |           -4.3362 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | without replacement      | fga_per_game |           46 |          39 |         -2.9895 |         -0.6674 | -3.6065 |  -4.5422 | -2.6928 |           -4.6549 |           -2.5762 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| NBA_to_EL   | with replacement (paper) | efg_pct      |          216 |         146 |          0.0479 |          0.0247 |  0.024  |   0.0067 |  0.0405 |            0.0055 |            0.0416 |       0.0001 | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | with replacement (paper) | three_pt_pct |          170 |         113 |          7.4404 |          2.1509 |  6.0799 |   3.7112 |  8.6042 |            3.5107 |            8.8599 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | with replacement (paper) | fga_per_game |          101 |          66 |          2.9002 |          0.5454 |  2.4608 |   1.8954 |  3      |            1.8117 |            3.1268 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | without replacement      | efg_pct      |          216 |         146 |          0.0479 |          0.017  |  0.0311 |   0.0134 |  0.0477 |            0.0127 |            0.0484 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | without replacement      | three_pt_pct |          170 |         113 |          7.4404 |          1.8926 |  6.4472 |   4.0762 |  8.9305 |            3.9003 |            9.065  |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | without replacement      | fga_per_game |          101 |          66 |          2.9002 |          0.5004 |  2.4344 |   1.8718 |  2.9672 |            1.7945 |            3.094  |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |

## Reviewer 3.13 / 3.15 - Dependence robustness

### `E1_episodes_per_player.csv`

Episodes per player, box-score sample.

|   episodes_per_player |   n_players |   n_episodes |
|----------------------:|------------:|-------------:|
|                     1 |         108 |          108 |
|                     2 |          96 |          192 |
|                     3 |          34 |          102 |
|                     4 |          40 |          160 |
|                     5 |           3 |           15 |
|                     6 |           2 |           12 |

### `E2_primary_episodes_per_player.csv`

Episodes per player, primary sample.

|   episodes_per_player |   n_players |
|----------------------:|------------:|
|                     2 |           5 |
|                     3 |           3 |
|                     4 |           3 |

### `E3_dependence_primary.csv`

Primary results under iid bootstrap, player-clustered bootstrap and one-episode-per-player restrictions.

| spec            | group                                     | metric   |   n |   n_players |   mean_delta |   ci_lo |   ci_hi |   wilcoxon_p |
|:----------------|:------------------------------------------|:---------|----:|------------:|-------------:|--------:|--------:|-------------:|
| harmonised      | all episodes (iid bootstrap)              | efg      |  31 |          11 |      -0.0226 | -0.0489 |  0.0038 |       0.1757 |
| harmonised      | all episodes (iid bootstrap)              | pps      |  31 |          11 |      -0.0453 | -0.0978 |  0.0076 |       0.1757 |
| harmonised      | all episodes (iid bootstrap)              | sxsv     |  31 |          11 |      -0.0092 | -0.0312 |  0.0111 |       0.5294 |
| harmonised      | all episodes (iid bootstrap)              | smoe     |  31 |          11 |      -0.0151 | -0.0354 |  0.0045 |       0.3271 |
| harmonised      | all episodes (player-clustered bootstrap) | efg      |  31 |          11 |      -0.0226 | -0.0507 |  0.0058 |       0.1757 |
| harmonised      | all episodes (player-clustered bootstrap) | pps      |  31 |          11 |      -0.0453 | -0.1014 |  0.0116 |       0.1757 |
| harmonised      | all episodes (player-clustered bootstrap) | sxsv     |  31 |          11 |      -0.0092 | -0.0362 |  0.0171 |       0.5294 |
| harmonised      | all episodes (player-clustered bootstrap) | smoe     |  31 |          11 |      -0.0151 | -0.0352 |  0.0035 |       0.3271 |
| harmonised      | one episode per player (first)            | efg      |  11 |          11 |      -0.0588 | -0.0979 | -0.0144 |       0.0537 |
| harmonised      | one episode per player (first)            | pps      |  11 |          11 |      -0.1175 | -0.1958 | -0.0287 |       0.0537 |
| harmonised      | one episode per player (first)            | sxsv     |  11 |          11 |      -0.0269 | -0.0689 |  0.01   |       0.2783 |
| harmonised      | one episode per player (first)            | smoe     |  11 |          11 |      -0.0365 | -0.0659 | -0.0101 |       0.0322 |
| harmonised      | one episode per player (random)           | efg      |  11 |          11 |      -0.0346 | -0.0778 |  0.0095 |       0.2783 |
| harmonised      | one episode per player (random)           | pps      |  11 |          11 |      -0.0692 | -0.1555 |  0.019  |       0.2783 |
| harmonised      | one episode per player (random)           | sxsv     |  11 |          11 |      -0.0142 | -0.0412 |  0.0113 |       0.4131 |
| harmonised      | one episode per player (random)           | smoe     |  11 |          11 |      -0.0186 | -0.0562 |  0.0187 |       0.4648 |
| league_specific | all episodes (iid bootstrap)              | efg      |  31 |          11 |      -0.0226 | -0.0489 |  0.0038 |       0.1757 |
| league_specific | all episodes (iid bootstrap)              | pps      |  31 |          11 |      -0.0453 | -0.0978 |  0.0076 |       0.1757 |
| league_specific | all episodes (iid bootstrap)              | sxsv     |  31 |          11 |      -0.0102 | -0.0353 |  0.0157 |       0.3176 |
| league_specific | all episodes (iid bootstrap)              | smoe     |  31 |          11 |      -0.0148 | -0.0353 |  0.005  |       0.2639 |
| league_specific | all episodes (player-clustered bootstrap) | efg      |  31 |          11 |      -0.0226 | -0.0507 |  0.0058 |       0.1757 |
| league_specific | all episodes (player-clustered bootstrap) | pps      |  31 |          11 |      -0.0453 | -0.1014 |  0.0116 |       0.1757 |
| league_specific | all episodes (player-clustered bootstrap) | sxsv     |  31 |          11 |      -0.0102 | -0.0382 |  0.0204 |       0.3176 |
| league_specific | all episodes (player-clustered bootstrap) | smoe     |  31 |          11 |      -0.0148 | -0.0354 |  0.0047 |       0.2639 |
| league_specific | one episode per player (first)            | efg      |  11 |          11 |      -0.0588 | -0.0979 | -0.0144 |       0.0537 |
| league_specific | one episode per player (first)            | pps      |  11 |          11 |      -0.1175 | -0.1958 | -0.0287 |       0.0537 |
| league_specific | one episode per player (first)            | sxsv     |  11 |          11 |      -0.0322 | -0.0723 |  0.0151 |       0.1748 |
| league_specific | one episode per player (first)            | smoe     |  11 |          11 |      -0.0351 | -0.061  | -0.0114 |       0.0186 |
| league_specific | one episode per player (random)           | efg      |  11 |          11 |      -0.0346 | -0.0778 |  0.0095 |       0.2783 |
| league_specific | one episode per player (random)           | pps      |  11 |          11 |      -0.0692 | -0.1555 |  0.019  |       0.2783 |
| league_specific | one episode per player (random)           | sxsv     |  11 |          11 |      -0.038  | -0.0747 |  0      |       0.0674 |
| league_specific | one episode per player (random)           | smoe     |  11 |          11 |      -0.0093 | -0.0473 |  0.0289 |       0.5771 |

### `E4_did_dependence.csv`

Matched-control DiD, all episodes vs one per player.

| direction   | sample                 | outcome      |   n_episodes |   n_players |   migrant_delta |   control_delta |      DiD |    ci_lo |   ci_hi |   ci_lo_clustered |   ci_hi_clustered |   wilcoxon_p | covariates_used                   | covariates_dropped   |   control_pool_n |
|:------------|:-----------------------|:-------------|-------------:|------------:|----------------:|----------------:|---------:|---------:|--------:|------------------:|------------------:|-------------:|:----------------------------------|:---------------------|-----------------:|
| EL_to_NBA   | all episodes           | efg_pct      |          128 |          87 |         -0.0675 |         -0.0052 |  -0.0635 |  -0.0832 | -0.0455 |           -0.0863 |           -0.043  |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | all episodes           | three_pt_pct |          110 |          79 |         -8.4862 |          0.4269 |  -7.8111 | -10.3765 | -5.3287 |          -10.9086 |           -4.8067 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | all episodes           | fga_per_game |           47 |          39 |         -2.9895 |         -0.8119 |  -2.8749 |  -3.7711 | -2.03   |           -3.9382 |           -1.9004 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | one episode per player | efg_pct      |           69 |          69 |         -0.0745 |         -0.001  |  -0.0758 |  -0.1045 | -0.0493 |           -0.1045 |           -0.0493 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | one episode per player | three_pt_pct |           57 |          57 |        -10.4618 |          0.5826 | -10.8024 | -14.8337 | -7.0542 |          -14.8337 |           -7.0542 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | one episode per player | fga_per_game |           24 |          24 |         -2.9053 |         -0.6158 |  -3.3971 |  -4.66   | -2.2122 |           -4.66   |           -2.2122 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| NBA_to_EL   | all episodes           | efg_pct      |          216 |         146 |          0.0479 |          0.0247 |   0.024  |   0.0067 |  0.0405 |            0.0055 |            0.0416 |       0.0001 | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | all episodes           | three_pt_pct |          170 |         113 |          7.4404 |          2.1509 |   6.0799 |   3.7112 |  8.6042 |            3.5107 |            8.8599 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | all episodes           | fga_per_game |          101 |          66 |          2.9002 |          0.5454 |   2.4608 |   1.8954 |  3      |            1.8117 |            3.1268 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | one episode per player | efg_pct      |          133 |         133 |          0.0387 |          0.0268 |   0.0126 |  -0.0124 |  0.0345 |           -0.0124 |            0.0345 |       0.0267 | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | one episode per player | three_pt_pct |          103 |         103 |          6.0993 |          1.8806 |   4.4795 |   1.5924 |  7.3932 |            1.5924 |            7.3932 |       0.0029 | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | one episode per player | fga_per_game |           55 |          55 |          2.4695 |          0.5733 |   2.0434 |   1.321  |  2.7761 |            1.321  |            2.7761 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |

### `H1_distinct_moves.csv`

Episodes vs DISTINCT migration moves. Because both direct (gap 0) and one-season-gap (gap 1) transitions are retained, the same destination season can enter the data twice, paired with two different origin seasons. A distinct move is a unique player x direction x destination season.

| sample                              |   n_episodes |   n_distinct_moves |   n_players |   episodes_per_move |
|:------------------------------------|-------------:|-------------------:|------------:|--------------------:|
| box-score sample (all 589 episodes) |          589 |                418 |         283 |              1.4091 |
| shot-coordinate sample, >=50 FGA    |           46 |                 26 |          16 |              1.7692 |
| shot-coordinate sample, >=100 FGA   |           31 |                 19 |          11 |              1.6316 |
| shot-coordinate sample, >=150 FGA   |           19 |                 12 |           9 |              1.5833 |
| shot-coordinate sample, >=200 FGA   |           12 |                  7 |           6 |              1.7143 |

### `H2_distinct_moves_direction.csv`

Distinct moves by direction in the primary sample.

| direction   |   n_distinct_moves |
|:------------|-------------------:|
| EL_to_NBA   |                 11 |
| NBA_to_EL   |                  8 |

### `H3_primary_distinct_moves.csv`

Primary pre-post results on all 31 episodes vs one episode per distinct move.

| spec            | sample                        | group     | metric   |   n |   n_players |   mean_pre |   mean_post |   mean_delta |   ci_lo |   ci_hi |   wilcoxon_p |
|:----------------|:------------------------------|:----------|:---------|----:|------------:|-----------:|------------:|-------------:|--------:|--------:|-------------:|
| harmonised      | all 31 episodes               | ALL       | efg      |  31 |          11 |     0.5157 |      0.493  |      -0.0226 | -0.0489 |  0.0038 |       0.1757 |
| harmonised      | all 31 episodes               | ALL       | pps      |  31 |          11 |     1.0313 |      0.986  |      -0.0453 | -0.0978 |  0.0076 |       0.1757 |
| harmonised      | all 31 episodes               | ALL       | sxsv     |  31 |          11 |     1.0345 |      1.0253 |      -0.0092 | -0.0312 |  0.0111 |       0.5294 |
| harmonised      | all 31 episodes               | ALL       | smoe     |  31 |          11 |     0.0008 |     -0.0143 |      -0.0151 | -0.0354 |  0.0045 |       0.3271 |
| harmonised      | all 31 episodes               | EL_to_NBA | efg      |  19 |          11 |     0.5404 |      0.489  |      -0.0513 | -0.0845 | -0.0164 |       0.0124 |
| harmonised      | all 31 episodes               | EL_to_NBA | pps      |  19 |          11 |     1.0807 |      0.9781 |      -0.1026 | -0.1689 | -0.0329 |       0.0124 |
| harmonised      | all 31 episodes               | EL_to_NBA | sxsv     |  19 |          11 |     1.0371 |      1.0255 |      -0.0115 | -0.0418 |  0.0158 |       0.6226 |
| harmonised      | all 31 episodes               | EL_to_NBA | smoe     |  19 |          11 |     0.0197 |     -0.0158 |      -0.0355 | -0.0615 | -0.0092 |       0.0204 |
| harmonised      | all 31 episodes               | NBA_to_EL | efg      |  12 |           8 |     0.4766 |      0.4993 |       0.0228 | -0.0039 |  0.05   |       0.1763 |
| harmonised      | all 31 episodes               | NBA_to_EL | pps      |  12 |           8 |     0.9531 |      0.9987 |       0.0456 | -0.0079 |  0.1    |       0.1763 |
| harmonised      | all 31 episodes               | NBA_to_EL | sxsv     |  12 |           8 |     1.0305 |      1.025  |      -0.0054 | -0.0351 |  0.0232 |       0.791  |
| harmonised      | all 31 episodes               | NBA_to_EL | smoe     |  12 |           8 |    -0.029  |     -0.012  |       0.017  | -0.0044 |  0.0368 |       0.1294 |
| harmonised      | one episode per distinct move | ALL       | efg      |  19 |          11 |     0.5005 |      0.4941 |      -0.0064 | -0.0451 |  0.0281 |       0.953  |
| harmonised      | one episode per distinct move | ALL       | pps      |  19 |          11 |     1.001  |      0.9882 |      -0.0128 | -0.0902 |  0.0562 |       0.953  |
| harmonised      | one episode per distinct move | ALL       | sxsv     |  19 |          11 |     1.0237 |      1.0277 |       0.0039 | -0.0179 |  0.0258 |       0.8596 |
| harmonised      | one episode per distinct move | ALL       | smoe     |  19 |          11 |    -0.0065 |     -0.0151 |      -0.0086 | -0.0375 |  0.0177 |       0.8906 |
| harmonised      | one episode per distinct move | EL_to_NBA | efg      |  11 |          11 |     0.5269 |      0.4905 |      -0.0364 | -0.0854 |  0.0126 |       0.2402 |
| harmonised      | one episode per distinct move | EL_to_NBA | pps      |  11 |          11 |     1.0537 |      0.981  |      -0.0727 | -0.1707 |  0.0253 |       0.2402 |
| harmonised      | one episode per distinct move | EL_to_NBA | sxsv     |  11 |          11 |     1.0195 |      1.0275 |       0.0081 | -0.0201 |  0.0368 |       0.6377 |
| harmonised      | one episode per distinct move | EL_to_NBA | smoe     |  11 |          11 |     0.0181 |     -0.0154 |      -0.0334 | -0.0716 |  0.0058 |       0.1748 |
| harmonised      | one episode per distinct move | NBA_to_EL | efg      |   8 |           8 |     0.4642 |      0.4991 |       0.0348 | -0.0045 |  0.0702 |       0.1484 |
| harmonised      | one episode per distinct move | NBA_to_EL | pps      |   8 |           8 |     0.9285 |      0.9981 |       0.0696 | -0.0089 |  0.1404 |       0.1484 |
| harmonised      | one episode per distinct move | NBA_to_EL | sxsv     |   8 |           8 |     1.0296 |      1.0278 |      -0.0018 | -0.0365 |  0.0327 |       1      |
| harmonised      | one episode per distinct move | NBA_to_EL | smoe     |   8 |           8 |    -0.0403 |     -0.0149 |       0.0254 |  0.0007 |  0.0481 |       0.0781 |
| league_specific | all 31 episodes               | ALL       | efg      |  31 |          11 |     0.5157 |      0.493  |      -0.0226 | -0.0489 |  0.0038 |       0.1757 |
| league_specific | all 31 episodes               | ALL       | pps      |  31 |          11 |     1.0313 |      0.986  |      -0.0453 | -0.0978 |  0.0076 |       0.1757 |
| league_specific | all 31 episodes               | ALL       | sxsv     |  31 |          11 |     1.0294 |      1.0192 |      -0.0102 | -0.0353 |  0.0157 |       0.3176 |
| league_specific | all 31 episodes               | ALL       | smoe     |  31 |          11 |     0.0031 |     -0.0117 |      -0.0148 | -0.0353 |  0.005  |       0.2639 |
| league_specific | all 31 episodes               | EL_to_NBA | efg      |  19 |          11 |     0.5404 |      0.489  |      -0.0513 | -0.0845 | -0.0164 |       0.0124 |
| league_specific | all 31 episodes               | EL_to_NBA | pps      |  19 |          11 |     1.0807 |      0.9781 |      -0.1026 | -0.1689 | -0.0329 |       0.0124 |
| league_specific | all 31 episodes               | EL_to_NBA | sxsv     |  19 |          11 |     1.0306 |      1.0227 |      -0.0079 | -0.0379 |  0.0239 |       0.3955 |
| league_specific | all 31 episodes               | EL_to_NBA | smoe     |  19 |          11 |     0.0227 |     -0.0147 |      -0.0373 | -0.0619 | -0.0129 |       0.0108 |
| league_specific | all 31 episodes               | NBA_to_EL | efg      |  12 |           8 |     0.4766 |      0.4993 |       0.0228 | -0.0039 |  0.05   |       0.1763 |
| league_specific | all 31 episodes               | NBA_to_EL | pps      |  12 |           8 |     0.9531 |      0.9987 |       0.0456 | -0.0079 |  0.1    |       0.1763 |
| league_specific | all 31 episodes               | NBA_to_EL | sxsv     |  12 |           8 |     1.0275 |      1.0137 |      -0.0139 | -0.0565 |  0.0291 |       0.6221 |
| league_specific | all 31 episodes               | NBA_to_EL | smoe     |  12 |           8 |    -0.0279 |     -0.007  |       0.0209 | -0.0035 |  0.0433 |       0.1294 |
| league_specific | one episode per distinct move | ALL       | efg      |  19 |          11 |     0.5005 |      0.4941 |      -0.0064 | -0.0451 |  0.0281 |       0.953  |
| league_specific | one episode per distinct move | ALL       | pps      |  19 |          11 |     1.001  |      0.9882 |      -0.0128 | -0.0902 |  0.0562 |       0.953  |
| league_specific | one episode per distinct move | ALL       | sxsv     |  19 |          11 |     1.0164 |      1.0232 |       0.0069 | -0.0225 |  0.0372 |       0.8906 |
| league_specific | one episode per distinct move | ALL       | smoe     |  19 |          11 |    -0.0037 |     -0.0132 |      -0.0095 | -0.0387 |  0.0169 |       0.8906 |
| league_specific | one episode per distinct move | EL_to_NBA | efg      |  11 |          11 |     0.5269 |      0.4905 |      -0.0364 | -0.0854 |  0.0126 |       0.2402 |
| league_specific | one episode per distinct move | EL_to_NBA | pps      |  11 |          11 |     1.0537 |      0.981  |      -0.0727 | -0.1707 |  0.0253 |       0.2402 |
| league_specific | one episode per distinct move | EL_to_NBA | sxsv     |  11 |          11 |     1.0094 |      1.0248 |       0.0153 | -0.0164 |  0.0531 |       0.8311 |
| league_specific | one episode per distinct move | EL_to_NBA | smoe     |  11 |          11 |     0.0219 |     -0.0143 |      -0.0361 | -0.0748 |  0.0011 |       0.1748 |
| league_specific | one episode per distinct move | NBA_to_EL | efg      |   8 |           8 |     0.4642 |      0.4991 |       0.0348 | -0.0045 |  0.0702 |       0.1484 |
| league_specific | one episode per distinct move | NBA_to_EL | pps      |   8 |           8 |     0.9285 |      0.9981 |       0.0696 | -0.0089 |  0.1404 |       0.1484 |
| league_specific | one episode per distinct move | NBA_to_EL | sxsv     |   8 |           8 |     1.026  |      1.0212 |      -0.0048 | -0.0536 |  0.0465 |       0.8438 |
| league_specific | one episode per distinct move | NBA_to_EL | smoe     |   8 |           8 |    -0.0389 |     -0.0118 |       0.0271 |  0.0025 |  0.053  |       0.1094 |

### `H6_did_distinct_moves.csv`

Matched-control DiD on all episodes, distinct moves and one episode per player.

| direction   | sample                        | outcome      |   n |   n_players |   migrant_delta |   control_delta |     DiD |    ci_lo |   ci_hi |   ci_lo_clustered |   ci_hi_clustered |   wilcoxon_p |
|:------------|:------------------------------|:-------------|----:|------------:|----------------:|----------------:|--------:|---------:|--------:|------------------:|------------------:|-------------:|
| EL_to_NBA   | all episodes                  | efg_pct      | 128 |          87 |         -0.0624 |         -0.0052 | -0.0581 |  -0.0765 | -0.0408 |           -0.0789 |           -0.0393 |       0      |
| EL_to_NBA   | all episodes                  | three_pt_pct | 110 |          79 |         -7.6208 |          0.4269 | -7.0829 |  -9.555  | -4.6683 |          -10.055  |           -4.2645 |       0      |
| EL_to_NBA   | all episodes                  | fga_per_game |  47 |          39 |         -2.9115 |         -0.8119 | -2.7123 |  -3.5345 | -1.9336 |           -3.6969 |           -1.8065 |       0      |
| EL_to_NBA   | one episode per distinct move | efg_pct      |  82 |          82 |         -0.0764 |         -0.0076 | -0.0703 |  -0.095  | -0.0469 |           -0.0949 |           -0.0472 |       0      |
| EL_to_NBA   | one episode per distinct move | three_pt_pct |  73 |          73 |         -8.3252 |          0.4906 | -8.2073 | -11.5343 | -5.0082 |          -11.6427 |           -4.8924 |       0      |
| EL_to_NBA   | one episode per distinct move | fga_per_game |  31 |          31 |         -3.2717 |         -0.969  | -2.3813 |  -3.4156 | -1.391  |           -3.4228 |           -1.3676 |       0.0001 |
| EL_to_NBA   | one episode per player        | efg_pct      |  69 |          69 |         -0.0714 |         -0.001  | -0.0726 |  -0.101  | -0.0474 |           -0.101  |           -0.0474 |       0      |
| EL_to_NBA   | one episode per player        | three_pt_pct |  57 |          57 |         -9.6878 |          0.5826 | -9.8112 | -13.7218 | -6.1547 |          -13.7218 |           -6.1547 |       0      |
| EL_to_NBA   | one episode per player        | fga_per_game |  24 |          24 |         -2.8364 |         -0.6158 | -3.2096 |  -4.4009 | -2.1116 |           -4.4009 |           -2.1116 |       0      |
| NBA_to_EL   | all episodes                  | efg_pct      | 216 |         146 |          0.0388 |          0.0169 |  0.0229 |   0.0051 |  0.039  |            0.0043 |            0.0409 |       0.0001 |
| NBA_to_EL   | all episodes                  | three_pt_pct | 170 |         113 |          6.1286 |          1.1584 |  6.0408 |   3.7205 |  8.5423 |            3.5006 |            8.8153 |       0      |
| NBA_to_EL   | all episodes                  | fga_per_game | 101 |          66 |          2.7374 |          0.4622 |  2.4101 |   1.8599 |  2.929  |            1.775  |            3.0554 |       0      |
| NBA_to_EL   | one episode per distinct move | efg_pct      | 156 |         146 |          0.0482 |          0.0211 |  0.0276 |   0.0056 |  0.0486 |            0.0055 |            0.0484 |       0.0002 |
| NBA_to_EL   | one episode per distinct move | three_pt_pct | 123 |         113 |          7.6253 |          1.7062 |  7.1643 |   4.3235 | 10.2985 |            4.2308 |           10.3191 |       0      |
| NBA_to_EL   | one episode per distinct move | fga_per_game |  67 |          66 |          3.173  |          0.5628 |  2.7671 |   2.1256 |  3.4099 |            2.1272 |            3.4118 |       0      |
| NBA_to_EL   | one episode per player        | efg_pct      | 133 |         133 |          0.0296 |          0.017  |  0.0137 |  -0.0112 |  0.0354 |           -0.0112 |            0.0354 |       0.0089 |
| NBA_to_EL   | one episode per player        | three_pt_pct | 103 |         103 |          4.5741 |          0.6962 |  4.5051 |   1.7658 |  7.3006 |            1.7658 |            7.3006 |       0.0033 |
| NBA_to_EL   | one episode per player        | fga_per_game |  55 |          55 |          2.2538 |          0.4779 |  1.9668 |   1.2762 |  2.6605 |            1.2762 |            2.6605 |       0      |

## Reviewer 3.17 - Direct vs one-season-gap transitions

### `F1_gap_counts.csv`

Episode counts by season gap, box-score sample.

| seasons_gap    |   EL_to_NBA |   NBA_to_EL |   total |
|:---------------|------------:|------------:|--------:|
| 0              |         149 |         182 |     331 |
| 1              |          94 |         164 |     258 |
| unique players |         156 |         229 |     283 |

### `F2_gap_counts_primary.csv`

Episode counts by season gap, primary sample.

|   gap |   EL_to_NBA |   NBA_to_EL |   total |
|------:|------------:|------------:|--------:|
|     0 |          11 |           7 |      18 |
|     1 |           8 |           5 |      13 |

### `F3_gap_primary_results.csv`

Primary pre-post results split by transition type.

| spec            | group                    | metric        |   n |   n_players |   mean_delta |   ci_lo |   ci_hi |   wilcoxon_p |
|:----------------|:-------------------------|:--------------|----:|------------:|-------------:|--------:|--------:|-------------:|
| harmonised      | direct (gap = 0)         | efg           |  18 |          11 |      -0.0081 | -0.0475 |  0.0293 |       0.8986 |
| harmonised      | direct (gap = 0)         | pps           |  18 |          11 |      -0.0161 | -0.0951 |  0.0585 |       0.8986 |
| harmonised      | direct (gap = 0)         | sxsv          |  18 |          11 |       0.0019 | -0.0215 |  0.0249 |       1      |
| harmonised      | direct (gap = 0)         | smoe          |  18 |          11 |      -0.0081 | -0.0384 |  0.0203 |       0.9323 |
| harmonised      | direct (gap = 0)         | three_rate    |  18 |          11 |      -0.0455 | -0.1338 |  0.0382 |       0.4423 |
| harmonised      | direct (gap = 0)         | mean_dist     |  18 |          11 |      -0.2915 | -0.7194 |  0.1311 |       0.2645 |
| harmonised      | direct (gap = 0)         | pps_over_sxsv |  18 |          11 |      -0.018  | -0.0946 |  0.0532 |       1      |
| harmonised      | one-season gap (gap = 1) | efg           |  13 |           9 |      -0.0428 | -0.076  | -0.0121 |       0.0327 |
| harmonised      | one-season gap (gap = 1) | pps           |  13 |           9 |      -0.0856 | -0.152  | -0.0242 |       0.0327 |
| harmonised      | one-season gap (gap = 1) | sxsv          |  13 |           9 |      -0.0245 | -0.062  |  0.01   |       0.3054 |
| harmonised      | one-season gap (gap = 1) | smoe          |  13 |           9 |      -0.0249 | -0.051  | -0.003  |       0.0803 |
| harmonised      | one-season gap (gap = 1) | three_rate    |  13 |           9 |       0.0062 | -0.0976 |  0.097  |       0.5879 |
| harmonised      | one-season gap (gap = 1) | mean_dist     |  13 |           9 |       0.1811 | -0.4417 |  0.7215 |       0.3757 |
| harmonised      | one-season gap (gap = 1) | pps_over_sxsv |  13 |           9 |      -0.0611 | -0.1258 | -0.0086 |       0.0803 |
| league_specific | direct (gap = 0)         | efg           |  18 |          11 |      -0.0081 | -0.0475 |  0.0293 |       0.8986 |
| league_specific | direct (gap = 0)         | pps           |  18 |          11 |      -0.0161 | -0.0951 |  0.0585 |       0.8986 |
| league_specific | direct (gap = 0)         | sxsv          |  18 |          11 |       0.0036 | -0.0273 |  0.0362 |       0.6397 |
| league_specific | direct (gap = 0)         | smoe          |  18 |          11 |      -0.0086 | -0.0392 |  0.02   |       1      |
| league_specific | direct (gap = 0)         | three_rate    |  18 |          11 |      -0.0455 | -0.1338 |  0.0382 |       0.4423 |
| league_specific | direct (gap = 0)         | mean_dist     |  18 |          11 |      -0.2915 | -0.7194 |  0.1311 |       0.2645 |
| league_specific | direct (gap = 0)         | pps_over_sxsv |  18 |          11 |      -0.0197 | -0.0956 |  0.0499 |       0.8986 |
| league_specific | one-season gap (gap = 1) | efg           |  13 |           9 |      -0.0428 | -0.076  | -0.0121 |       0.0327 |
| league_specific | one-season gap (gap = 1) | pps           |  13 |           9 |      -0.0856 | -0.152  | -0.0242 |       0.0327 |
| league_specific | one-season gap (gap = 1) | sxsv          |  13 |           9 |      -0.0293 | -0.0681 |  0.0112 |       0.2163 |
| league_specific | one-season gap (gap = 1) | smoe          |  13 |           9 |      -0.0233 | -0.049  |  0.0011 |       0.0803 |
| league_specific | one-season gap (gap = 1) | three_rate    |  13 |           9 |       0.0062 | -0.0976 |  0.097  |       0.5879 |
| league_specific | one-season gap (gap = 1) | mean_dist     |  13 |           9 |       0.1811 | -0.4417 |  0.7215 |       0.3757 |
| league_specific | one-season gap (gap = 1) | pps_over_sxsv |  13 |           9 |      -0.0563 | -0.1171 |  0.0017 |       0.1099 |

### `F4_gap_boxscore_results.csv`

Box-score pre-post results split by transition type.

| sample                              | variable            |   n |   n_players |   mean_pre |   mean_post |   mean_delta |   ci_lo |   ci_hi |   ci_lo_clustered |   ci_hi_clustered |   wilcoxon_p |
|:------------------------------------|:--------------------|----:|------------:|-----------:|------------:|-------------:|--------:|--------:|------------------:|------------------:|-------------:|
| box-score, direct (gap = 0)         | minutes_per_game    | 179 |         136 |    15.9565 |     17.8902 |       0.5703 | -1.2982 |  2.4492 |           -0.9313 |            2.113  |       0.4993 |
| box-score, direct (gap = 0)         | fga_per_game        | 179 |         136 |     5.0525 |      5.7173 |       0.1988 | -0.5177 |  0.9205 |           -0.3958 |            0.7878 |       0.5573 |
| box-score, direct (gap = 0)         | fga_per_min         | 179 |         136 |     0.3122 |      0.3149 |       0.0045 | -0.0108 |  0.0192 |           -0.0095 |            0.0183 |       0.7766 |
| box-score, direct (gap = 0)         | usage_proxy_per_min | 179 |         136 |     0.414  |      0.4188 |       0.0084 | -0.0103 |  0.027  |           -0.0086 |            0.0255 |       0.5684 |
| box-score, direct (gap = 0)         | points_per_game     | 179 |         136 |     6.1981 |      7.1117 |       0.2482 | -0.8355 |  1.3347 |           -0.6295 |            1.1381 |       0.6213 |
| box-score, direct (gap = 0)         | efg_pct             | 323 |         217 |     0.4701 |      0.4877 |       0.018  | -0.0007 |  0.0365 |            0.0014 |            0.0341 |       0.0535 |
| box-score, one-season gap (gap = 1) | minutes_per_game    | 148 |         124 |    15.4503 |     19.059  |       2.4138 |  0.5532 |  4.2864 |            0.5309 |            4.2892 |       0.0192 |
| box-score, one-season gap (gap = 1) | fga_per_game        | 148 |         124 |     4.8279 |      6.1078 |       0.8849 |  0.1419 |  1.6417 |            0.1725 |            1.6183 |       0.0252 |
| box-score, one-season gap (gap = 1) | fga_per_min         | 148 |         124 |     0.3097 |      0.3171 |       0.0079 | -0.0063 |  0.0228 |           -0.0057 |            0.0221 |       0.7521 |
| box-score, one-season gap (gap = 1) | usage_proxy_per_min | 148 |         124 |     0.4168 |      0.4268 |       0.0104 | -0.0059 |  0.0282 |           -0.0056 |            0.0268 |       0.3395 |
| box-score, one-season gap (gap = 1) | points_per_game     | 148 |         124 |     5.9248 |      7.7724 |       1.2168 |  0.1417 |  2.2926 |            0.1938 |            2.2544 |       0.0294 |
| box-score, one-season gap (gap = 1) | efg_pct             | 252 |         211 |     0.4716 |      0.5061 |       0.0333 |  0.0155 |  0.0513 |            0.0159 |            0.0514 |       0.0018 |

### `F5_gap_did.csv`

Matched-control DiD split by transition type.

| direction   | transition               | outcome      |   n_episodes |   n_players |   migrant_delta |   control_delta |     DiD |    ci_lo |   ci_hi |   ci_lo_clustered |   ci_hi_clustered |   wilcoxon_p | covariates_used                   | covariates_dropped   |   control_pool_n |
|:------------|:-------------------------|:-------------|-------------:|------------:|----------------:|----------------:|--------:|---------:|--------:|------------------:|------------------:|-------------:|:----------------------------------|:---------------------|-----------------:|
| EL_to_NBA   | direct (gap = 0)         | efg_pct      |           80 |          80 |         -0.0812 |         -0.0074 | -0.0742 |  -0.1013 | -0.0496 |           -0.1013 |           -0.0496 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | direct (gap = 0)         | three_pt_pct |           71 |          71 |         -9.114  |          0.5252 | -8.3188 | -11.8081 | -4.9354 |          -11.8081 |           -4.9354 |       0.0001 | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | direct (gap = 0)         | fga_per_game |           30 |          30 |         -3.3089 |         -0.9953 | -2.4333 |  -3.574  | -1.344  |           -3.574  |           -1.344  |       0.0001 | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | one-season gap (gap = 1) | efg_pct      |           48 |          48 |         -0.0463 |         -0.0016 | -0.0456 |  -0.069  | -0.0231 |           -0.069  |           -0.0231 |       0.0004 | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | one-season gap (gap = 1) | three_pt_pct |           39 |          39 |         -7.5085 |          0.248  | -6.8867 | -10.6311 | -3.3085 |          -10.6311 |           -3.3085 |       0.0001 | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| EL_to_NBA   | one-season gap (gap = 1) | fga_per_game |           17 |          17 |         -2.4921 |         -0.4882 | -3.6541 |  -5.0382 | -2.417  |           -5.0382 |           -2.417  |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             2224 |
| NBA_to_EL   | direct (gap = 0)         | efg_pct      |          124 |         115 |          0.0524 |          0.027  |  0.025  |   0.0008 |  0.0469 |            0.0004 |            0.0461 |       0.0004 | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | direct (gap = 0)         | three_pt_pct |          100 |          91 |          7.8478 |          2.8014 |  6.2166 |   3.136  |  9.5308 |            3.1476 |            9.7682 |       0.0001 | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | direct (gap = 0)         | fga_per_game |           55 |          54 |          3.3004 |          0.6189 |  2.7548 |   2.1015 |  3.435  |            2.1041 |            3.4327 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | one-season gap (gap = 1) | efg_pct      |           92 |          91 |          0.0419 |          0.0215 |  0.0226 |  -0.001  |  0.0452 |           -0.0007 |            0.0464 |       0.0387 | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | one-season gap (gap = 1) | three_pt_pct |           70 |          69 |          6.8583 |          1.2745 |  5.8846 |   2.2969 |  9.5244 |            2.3307 |            9.6694 |       0.0034 | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |
| NBA_to_EL   | one-season gap (gap = 1) | fga_per_game |           46 |          45 |          2.4217 |          0.4463 |  2.1092 |   1.2382 |  2.9613 |            1.2787 |            2.9468 |       0      | fga_per_game+efg_pct+three_pt_pct | -                    |             6183 |

## Reviewer 3.16 - Minutes, attempts per minute and usage

### `G1_usage_availability.csv`

Availability of playing-time and usage variables.

| source                                          |   n_rows |   minutes_per_game_% |   fga_per_game_% |   turnovers_per_game_% |   ft_attempts_% |   fga_per_min_% |   usage_proxy_% |
|:------------------------------------------------|---------:|---------------------:|-----------------:|-----------------------:|----------------:|----------------:|----------------:|
| EuroLeague season table (migrant + all players) |     8378 |              56.9706 |          56.9706 |                56.9706 |             100 |         56.9706 |         56.9706 |
| NBA season table (migrant + all players)        |     1677 |             100      |         100      |                99.7615 |             100 |        100      |         99.7615 |
| NBANonMigrantSeasons (NBA control pool)         |     8180 |               0      |         100      |                 0      |               0 |          0      |          0      |

### `G2_usage_prepost.csv`

Minutes per game, FGA per game, FGA per minute and a usage proxy before and after migration.

| sample                     | variable            |   n |   n_players |   mean_pre |   mean_post |   mean_delta |   ci_lo |   ci_hi |   ci_lo_clustered |   ci_hi_clustered |   wilcoxon_p |
|:---------------------------|:--------------------|----:|------------:|-----------:|------------:|-------------:|--------:|--------:|------------------:|------------------:|-------------:|
| all episodes (box-score)   | minutes_per_game    | 327 |         162 |    15.7277 |     18.396  |       1.4047 |  0.0487 |  2.7153 |            0.1025 |            2.7175 |       0.0388 |
| all episodes (box-score)   | fga_per_game        | 327 |         162 |     4.951  |      5.8863 |       0.5093 | -0.013  |  1.0081 |           -0.0035 |            1.0205 |       0.0531 |
| all episodes (box-score)   | fga_per_min         | 327 |         162 |     0.3111 |      0.3159 |       0.0061 | -0.0045 |  0.0163 |           -0.0051 |            0.0169 |       0.6799 |
| all episodes (box-score)   | usage_proxy_per_min | 327 |         162 |     0.4152 |      0.4223 |       0.0093 | -0.0032 |  0.0218 |           -0.0041 |            0.0229 |       0.292  |
| all episodes (box-score)   | points_per_game     | 327 |         162 |     6.0746 |      7.3976 |       0.6866 | -0.0964 |  1.4288 |           -0.085  |            1.4675 |       0.0669 |
| all episodes (box-score)   | efg_pct             | 575 |         276 |     0.4707 |      0.4958 |       0.0247 |  0.012  |  0.0375 |            0.012  |            0.0373 |       0.0005 |
| box-score EL_to_NBA        | minutes_per_game    | 154 |         102 |    23.4179 |     15.3437 |      -8.1611 | -9.518  | -6.8316 |           -9.7631 |           -6.5386 |       0      |
| box-score EL_to_NBA        | fga_per_game        | 154 |         102 |     7.7078 |      4.7284 |      -3.0762 | -3.6391 | -2.5018 |           -3.729  |           -2.3756 |       0      |
| box-score EL_to_NBA        | fga_per_min         | 154 |         102 |     0.3226 |      0.3091 |      -0.0148 | -0.0289 |  0.0005 |           -0.0316 |            0.0031 |       0.0004 |
| box-score EL_to_NBA        | usage_proxy_per_min | 154 |         102 |     0.4413 |      0.4053 |      -0.039  | -0.0563 | -0.0202 |           -0.0596 |           -0.0171 |       0      |
| box-score EL_to_NBA        | points_per_game     | 154 |         102 |    10.4682 |      5.5103 |      -5.0564 | -5.8129 | -4.2969 |           -5.9363 |           -4.1486 |       0      |
| box-score EL_to_NBA        | efg_pct             | 238 |         154 |     0.5252 |      0.4708 |      -0.0533 | -0.0682 | -0.0391 |           -0.0696 |           -0.037  |       0      |
| box-score NBA_to_EL        | minutes_per_game    | 173 |         112 |    12.3048 |     22.6833 |       9.9199 |  8.6762 | 11.2004 |            8.552  |           11.3647 |       0      |
| box-score NBA_to_EL        | fga_per_game        | 173 |         112 |     3.724  |      7.5127 |       3.7011 |  3.2099 |  4.2064 |            3.1505 |            4.2693 |       0      |
| box-score NBA_to_EL        | fga_per_min         | 173 |         112 |     0.306  |      0.3253 |       0.0247 |  0.009  |  0.0389 |            0.0073 |            0.0408 |       0.0001 |
| box-score NBA_to_EL        | usage_proxy_per_min | 173 |         112 |     0.4036 |      0.4461 |       0.0523 |  0.0363 |  0.0678 |            0.0341 |            0.0696 |       0      |
| box-score NBA_to_EL        | points_per_game     | 173 |         112 |     4.1191 |     10.0486 |       5.7988 |  5.1482 |  6.4757 |            5.0543 |            6.5644 |       0      |
| box-score NBA_to_EL        | efg_pct             | 337 |         223 |     0.4332 |      0.5138 |       0.0798 |  0.0623 |  0.0967 |            0.061  |            0.0994 |       0      |
| primary ≥100 FGA subsample | minutes_per_game    |  30 |          11 |    20.8078 |     20.0879 |      -0.9154 | -4.3305 |  2.5002 |           -3.6711 |            1.6737 |       0.7922 |
| primary ≥100 FGA subsample | fga_per_game        |  30 |          11 |     6.8539 |      6.81   |      -0.0913 | -1.7354 |  1.6137 |           -1.5582 |            1.5943 |       0.7421 |
| primary ≥100 FGA subsample | fga_per_min         |  30 |          11 |     0.3236 |      0.33   |       0.0077 | -0.0232 |  0.038  |           -0.0218 |            0.0399 |       0.5838 |
| primary ≥100 FGA subsample | usage_proxy_per_min |  30 |          11 |     0.4281 |      0.4338 |       0.0062 | -0.0348 |  0.0459 |           -0.0358 |            0.0469 |       0.5838 |
| primary ≥100 FGA subsample | points_per_game     |  30 |          11 |     8.6226 |      8.203  |      -0.4987 | -2.7811 |  1.7568 |           -2.326  |            1.5502 |       0.7611 |
| primary ≥100 FGA subsample | efg_pct             |  31 |          11 |     0.5108 |      0.4895 |      -0.0213 | -0.0484 |  0.0067 |           -0.0484 |            0.0046 |       0.0958 |

### `G3_fga_on_minutes.csv`

Change in FGA per game regressed on change in minutes per game.

| term                      |    beta |   se_clustered |      p |   ci_lo |   ci_hi |
|:--------------------------|--------:|---------------:|-------:|--------:|--------:|
| Intercept                 | -0.0763 |         0.1974 | 0.6993 | -0.4633 |  0.3107 |
| C(direction)[T.NBA_to_EL] |  0.1309 |         0.3281 | 0.6899 | -0.5122 |  0.774  |
| d_minutes_per_game        |  0.3676 |         0.0145 | 0      |  0.3391 |  0.3961 |

## Additional files (CSV only, not tabulated here)

- `calibration_bins.csv`
- `C_threshold_sensitivity_full.csv`
- `B0_episode_covariates.csv`
- `G0_usage_episode_level.csv`
- `C5_primary_episode_level_harmonised.csv`
- `C5_primary_episode_level_leaguespecific.csv`