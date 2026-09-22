# Experiment inputs

Inputs read by the notebooks in `notebooks/experiments/` (paths `../../data/...`).

| File | Content | Source |
|---|---|---|
| `poti/porto_dataset_buffered.csv` | 430 POTIs, Porto | IJDRR article; same file as `md-contextual-risk-index/data/poti/` (commit `495ebf2`) |
| `poti/lisbon_dataset_buffered.csv` | 776 POTIs, Lisbon | IJDRR article; same file as `md-contextual-risk-index/data/poti/` (commit `495ebf2`) |
| `poti/paris_dataset_buffered.csv` | 2066 POTIs, Paris | IJDRR article (<https://doi.org/10.5281/zenodo.19113788>) |
| `time_windows/default_time_windows.csv` | Time-window table of the IJDRR article | Built from the per-category files below |
| `time_windows/{category}.csv` | Per-category schedules of the article's table | `md-contextual-risk-index/data/time_windows/` (commit `495ebf2`) |
| `time_windows/time_windows_continuous_occupancy.csv` | Continuous-occupancy time-window table: exclusive window ends, every category active between its peaks, hospitals and stations at a low level at night | `time_windows_T1g.csv` in `md-contextual-risk-index/data/time_windows/` (commit `495ebf2`); documented in its `docs/thesis/README.md` |
| `time_windows/scenarios_activity_regimes.csv` | Scenarios s1–s4, one per activity regime: Mon 08:30, Mon 11:00, Mon 21:00, Sat 11:00 | `scenarios_T1g.csv` in the same folder |
| `cities/porto.geojson`, `cities/lisbon.geojson` | City boundaries for the 100 m grid | `md-contextual-risk-index/data/cities/` (commit `495ebf2`) |
| `cities/paris.geojson` | Boundary of the commune of Paris (OSM relation 71525) | Geocoded with osmnx (`geocode_to_gdf("Paris, France")`) on 2026-09-22 |

Time windows store `ts`/`te` as Unix epochs of local wall-clock time, read as UTC, the same convention as
`TimeWindowGenerator.to_unix_epoch`. The article's notebooks and inputs are tagged `ijdrr-article`. That
tag has neither the continuous-occupancy table nor the scenario file.
