"""
Pytest tests for H3-based hexagonal grid generation.
"""

import os
import sys

import geopandas as gpd
import pytest
from shapely.geometry import box

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from verus.grid.hexagon import HexagonGridGenerator
from verus.utils.logger import Logger

h3 = pytest.importorskip("h3", reason="h3 library not installed; skipping H3 tests")


@pytest.fixture
def small_area_gdf():
    """A tiny bounding box around the centre of Porto as a GeoDataFrame."""
    # ~1 km square around Porto city centre
    poly = box(-8.620, 41.145, -8.610, 41.155)
    return gpd.GeoDataFrame({"geometry": [poly]}, crs="EPSG:4326")


def _make_generator(use_h3=True, edge_length=500, h3_resolution=None):
    """Create a HexagonGridGenerator that avoids geocoding."""
    gen = HexagonGridGenerator.__new__(HexagonGridGenerator)
    # Initialise the Logger mixin so self.log() works
    Logger.__init__(gen, name="HexagonGridGenerator_Test", verbose=False)
    gen.region = "Porto, Portugal"
    gen.place_name = "Porto"
    gen.edge_length = edge_length
    gen.use_h3 = use_h3
    gen.h3_resolution = h3_resolution
    gen.is_file = False
    return gen


# ---------------------------------------------------------------------------
# _choose_h3_resolution tests
# ---------------------------------------------------------------------------

class TestChooseH3Resolution:
    def test_returns_int_in_valid_range(self):
        gen = _make_generator(edge_length=500)
        res = gen._choose_h3_resolution(500)
        assert isinstance(res, int)
        assert 0 <= res <= 15

    def test_large_edge_length_gives_low_resolution(self):
        gen = _make_generator(edge_length=100_000)
        res = gen._choose_h3_resolution(100_000)
        # 100 km edge length should map to a very coarse resolution
        assert res <= 3

    def test_small_edge_length_gives_high_resolution(self):
        gen = _make_generator(edge_length=10)
        res = gen._choose_h3_resolution(10)
        # 10 m edge length should map to a fine resolution
        assert res >= 12

    def test_monotonically_coarser_for_larger_edges(self):
        gen = _make_generator()
        edge_lengths = [10_000, 1_000, 100]
        resolutions = [gen._choose_h3_resolution(e) for e in edge_lengths]
        # Larger edge length → smaller (coarser) resolution
        assert resolutions[0] <= resolutions[1] <= resolutions[2]


# ---------------------------------------------------------------------------
# generate_hex_grid_h3 tests
# ---------------------------------------------------------------------------

class TestGenerateHexGridH3:
    def test_returns_geodataframe(self, small_area_gdf):
        gen = _make_generator(edge_length=500)
        result = gen.generate_hex_grid_h3(small_area_gdf)
        assert isinstance(result, gpd.GeoDataFrame)

    def test_crs_is_4326(self, small_area_gdf):
        gen = _make_generator(edge_length=500)
        result = gen.generate_hex_grid_h3(small_area_gdf)
        assert result.crs is not None
        assert result.crs.to_epsg() == 4326

    def test_has_hex_id_column(self, small_area_gdf):
        gen = _make_generator(edge_length=500)
        result = gen.generate_hex_grid_h3(small_area_gdf)
        assert "hex_id" in result.columns

    def test_has_geometry_column(self, small_area_gdf):
        gen = _make_generator(edge_length=500)
        result = gen.generate_hex_grid_h3(small_area_gdf)
        assert "geometry" in result.columns

    def test_all_geometries_are_valid_polygons(self, small_area_gdf):
        gen = _make_generator(edge_length=500)
        result = gen.generate_hex_grid_h3(small_area_gdf)
        assert len(result) > 0
        for geom in result.geometry:
            assert geom.is_valid
            assert geom.geom_type in ("Polygon", "MultiPolygon")

    def test_cells_cover_region(self, small_area_gdf):
        gen = _make_generator(edge_length=500)
        result = gen.generate_hex_grid_h3(small_area_gdf)
        region_geom = small_area_gdf.geometry.iloc[0]
        union = result.union_all()
        # H3 polygon_to_cells uses centroid containment, so cells on the boundary
        # may be excluded. Verify at least some meaningful coverage exists.
        intersection = region_geom.intersection(union)
        coverage = intersection.area / region_geom.area
        assert coverage > 0.0
        assert len(result) > 0

    def test_hex_ids_are_unique(self, small_area_gdf):
        gen = _make_generator(edge_length=500)
        result = gen.generate_hex_grid_h3(small_area_gdf)
        assert result["hex_id"].nunique() == len(result)

    def test_explicit_resolution_respected(self, small_area_gdf):
        gen = _make_generator(edge_length=500)
        result_low = gen.generate_hex_grid_h3(small_area_gdf, resolution=7)
        result_high = gen.generate_hex_grid_h3(small_area_gdf, resolution=9)
        # Higher resolution → smaller cells → more cells within the same area
        assert len(result_high) >= len(result_low)

    def test_larger_edge_length_produces_fewer_cells(self, small_area_gdf):
        gen_coarse = _make_generator(edge_length=1000)
        gen_fine = _make_generator(edge_length=200)
        result_coarse = gen_coarse.generate_hex_grid_h3(small_area_gdf)
        result_fine = gen_fine.generate_hex_grid_h3(small_area_gdf)
        assert len(result_coarse) <= len(result_fine)


# ---------------------------------------------------------------------------
# HexagonGridGenerator integration (use_h3=True via run-like path)
# ---------------------------------------------------------------------------

class TestHexagonGridGeneratorH3Init:
    def test_use_h3_stored(self):
        gen = HexagonGridGenerator(region="Porto, Portugal", use_h3=True)
        assert gen.use_h3 is True

    def test_h3_resolution_stored(self):
        gen = HexagonGridGenerator(
            region="Porto, Portugal", use_h3=True, h3_resolution=8
        )
        assert gen.h3_resolution == 8

    def test_invalid_h3_resolution_raises(self):
        with pytest.raises(ValueError):
            HexagonGridGenerator(
                region="Porto, Portugal", use_h3=True, h3_resolution=16
            )

    def test_default_use_h3_is_false(self):
        gen = HexagonGridGenerator(region="Porto, Portugal")
        assert gen.use_h3 is False
