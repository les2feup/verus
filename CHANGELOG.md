# Changelog

All notable changes to the VERUS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added (Unreleased)

-   Initial documentation for core concepts
-   Support for time-based vulnerability assessment

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
