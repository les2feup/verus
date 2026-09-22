# Experiment inputs

Inputs read by the notebooks in `notebooks/experiments/` (paths `../../data/...`).

| File | Content | Source |
|---|---|---|
| `poti/porto_dataset_buffered.csv` | 430 POTIs, Porto | IJDRR article; same file as `md-contextual-risk-index/data/poti/` (commit `495ebf2`) |
| `poti/lisbon_dataset_buffered.csv` | 776 POTIs, Lisbon | IJDRR article; same file as `md-contextual-risk-index/data/poti/` (commit `495ebf2`) |
| `poti/paris_dataset_buffered.csv` | 2066 POTIs, Paris | IJDRR article (<https://doi.org/10.5281/zenodo.19113788>) |
| `time_windows/default_time_windows.csv` | Time-window table of the IJDRR article | Built from the per-category files below |
| `time_windows/{category}.csv` | Per-category schedules of the article's table | `md-contextual-risk-index/data/time_windows/` (commit `495ebf2`) |

Time windows store `ts`/`te` as Unix epochs of local wall-clock time, read as UTC, the same convention as
`TimeWindowGenerator.to_unix_epoch`. The files used in the IJDRR article are tagged `ijdrr-article`.
