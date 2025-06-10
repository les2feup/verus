# Changelog

All notable changes to the VERUS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

## [0.1.1] - 2025-06-10

### Added

- Support for loading custom region boundaries from GeoJSON files in HexagonGridGenerator

### Improved

- Updated documentation with examples of GeoJSON file usage
- Enhanced hexagon grid generator with file validation and error handling

## [0.1.0] - 2025-03-13

### Added

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
-   PoI filtering to select really influential points is not yet implemented

### Future Improvements

-   Implement a CLI for easier usage of the framework
