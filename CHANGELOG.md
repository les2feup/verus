# Changelog

All notable changes to the VERUS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added (Unreleased)

### Fixed (Unreleased)

## [1.1.0] - 2026-04-14

### Added

-   **H3-based hexagonal grid generation** (`use_h3=True` parameter on `HexagonGridGenerator`): generates geodesic, pointy-topped hexagonal grids using Uber's H3 library instead of the manual flat-topped tessellation. Produces a `GeoDataFrame` with a `hex_id` column containing native H3 cell indices.
-   `_choose_h3_resolution(edge_length)` helper method: automatically selects the H3 resolution (0–15) whose average edge length is closest to the requested `edge_length` in metres using `h3.average_hexagon_edge_length`.
-   `generate_hex_grid_h3(area_gdf, resolution=None)` method: fills the bounding box of the AoI with H3 cells via `h3.polygon_to_cells`, filters by geometric intersection with the true boundary, and clips to the exact AoI outline so edge cells are cropped rather than dropped.
-   `h3_resolution` parameter on `HexagonGridGenerator.__init__()`: allows overriding the automatically chosen resolution.
-   `h3>=4.0.0` added as a project dependency in `pyproject.toml` and `src/requirements.txt`.
-   New pytest test file `test/test_hexagon_h3.py` with 17 tests covering resolution selection, GeoDataFrame structure, CRS, polygon validity, coverage, uniqueness and parameter validation. Tests skip gracefully when `h3` is not installed.
-   `VERUS.load()` now accepts a CSV file path string for `potis_df` and `centroids_df` in addition to a `DataFrame`, reading the file automatically with `pd.read_csv`.

### Fixed

-   **H3 grid boundary clipping**: replaced `polygon_to_cells` on a buffered polygon (centroid-containment misses concave boundary sections) with a bounding-box fill + `intersects` filter + `gpd.clip`. This ensures complete, gap-free coverage along the entire AoI outline including inlets and river bends.
-   `clip_to_region` was silently returning an unclipped grid for H3 grids because `set_crs` raises a `ValueError` when a CRS is already assigned. Changed to `to_crs` which reprojects correctly and never errors on a matching CRS.
-   **OSM cache disabled on every `DataExtractor.run()` call**: removed the unconditional `clear_osm_cache()` call that was toggling `ox.settings.use_cache` off/on, defeating osmnx's HTTP disk cache and forcing live Overpass API round-trips for every execution.
-   `adjusted_timeout` in `DataExtractor._extract_category_pois` was computed but never forwarded to `_fetch_features_with_timeout`, which always used the default 60-second hard limit regardless of polygon size. The timeout is now passed through and `ox.settings.requests_timeout` is kept in sync so the osmnx HTTP layer and the wrapper agree.
-   `_fetch_features_with_timeout` now accepts an explicit `timeout` parameter (falls back to `self.fetch_timeout` when omitted).

### Changed

-   `HexagonGridGenerator.__init__()` signature extended with `use_h3=False` and `h3_resolution=None`; backward compatible — existing callers require no changes.
-   `HexagonGridGenerator.run()` dispatches to `generate_hex_grid_h3()` when `use_h3=True`, otherwise preserves the existing manual tessellation path.

## [0.1.1] - 2025-06-10

### Added

-   Support for loading custom region boundaries from GeoJSON files in HexagonGridGenerator

### Improved

-   Updated documentation with examples of GeoJSON file usage
-   Enhanced hexagon grid generator with file validation and error handling

## [1.0.1] - 2025-11-03

### Fixed

-   KMeans predefined centers flow: `predefined_centers` no longer mandatory in constructor; now validated only when `init="predefined"` is used and centers are actually needed (constructor or `run()` may supply them).
-   Resolved indentation issue in `_init_centroids_predefined` leading to a syntax error.
-   GeoPandas centroid warning fixed in POI extraction by computing centroids in a projected CRS (EPSG:3857) and converting back to EPSG:4326.

### Changed

-   Time windows: `TimeWindowGenerator.generate_from_schedule(as_dataframe=True)` now returns a single combined DataFrame with `category, vi, ts, te, start_time, end_time` while keeping dict-of-DataFrames for backward compatibility. Test updated to validate consistency between both outputs.

### Documentation

-   Notebooks updated to use the DataFrame-first time windows API where applicable.

## [1.0.0] - 2025-03-13

### Added (1.0.0)

-   Initial release of VERUS framework
-   Core functionality for Points of Temporal Influence (PoTIs)
-   Vulnerability zone calculation with hexagonal grid support
-   Time window-based analysis
-   Data extraction from OpenStreetMap
-   Basic visualization tools
-   Gaussian and inverse weighted distance methods for vulnerability calculation
-   Clustering pipeline using OPTICS and KMeans algorithms

### Known Issues

-   Limited support for time windows
-   Main function can expose more parameters for experimentation

### Future Improvements

-   Implement a CLI for easier usage of the framework
