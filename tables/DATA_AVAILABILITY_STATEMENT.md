# Data availability and reproducibility - text for the manuscript

Reviewer #1 comment R1.20 ("Reproducibility is limited because processed data/code are
only available upon request"). The statement below replaces the current
availability-on-request wording.

**Repository URL (to be inserted once the repository is public):**
`https://github.com/simonator420/shooting-profiles-nba-euroleague`

---

## Data Availability Statement

The processed data and analysis code that support the findings of this study are
openly available at https://github.com/simonator420/shooting-profiles-nba-euroleague.
The repository contains the analysis-ready shot-level file with out-of-fold spatial
expected shot value estimates, the player-season box-score panel for both
competitions, the migration-episode table, the non-migrant control pool, and a
reproducibility notebook that regenerates every statistic reported in this article
without requiring any further data access. Code is released under the MIT licence.

Raw data were collected from publicly accessible sources: EuroLeague player, box-score
and shot-location data from the official EuroLeague API (api-live.euroleague.net), and
NBA player, box-score and shot-location data from stats.nba.com through the `nba_api`
Python package. The full-population shot files used to fit the expected shot value
models (approximately 4.0 million NBA and 0.54 million EuroLeague field-goal attempts)
are not redistributed because of their size; the fitted out-of-fold predictions for
every attempt used in the analyses are included in the repository, together with the
model performance and calibration output, and the collection scripts allow the
population files to be rebuilt from the original public sources.

---

## Shorter variant, if the journal caps the statement length

The processed data and analysis code supporting this study are openly available at
https://github.com/simonator420/shooting-profiles-nba-euroleague, together with a
notebook that reproduces all reported statistics without further data access. Raw data
were collected from the public EuroLeague API (api-live.euroleague.net) and from
stats.nba.com via the `nba_api` package. Code is released under the MIT licence.

---

## Suggested revision-letter response to R1.20

> **R1.20. Reproducibility is limited because processed data/code are only available
> upon request.**
>
> We agree. The processed data and the full analysis code are now openly available in
> a public repository rather than on request. The repository contains the
> analysis-ready shot-level file with out-of-fold spatial expected shot value
> estimates under both the harmonised and the league-specific specification, the
> player-season box-score panel for both competitions, the migration-episode table,
> the non-migrant control pool used for the matched-control comparison, and a
> reproducibility notebook whose final cell prints every number reported in the
> article. The Data Availability Statement has been updated accordingly, and the
> repository is released under the MIT licence.
