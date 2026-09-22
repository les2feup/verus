"""Regression tests: only POTIs active at the evaluation time are clustered.

With time windows loaded, POTIs of inactive categories (vi = 0) must not enter
OPTICS or K-means, and must not dilute the vulnerability kernel of a cluster.
The result must equal an assessment of the active POTIs alone.
"""

import os
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from shapely.geometry import box

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from verus import VERUS  # noqa: E402

T1 = 1_700_000_000  # only category "a" active
T_NONE = T1 + 86_400  # no category active

CONFIG = {
    "max_vulnerability": {"Synthetic": 1.0},
    "clustering": {
        "optics": {"min_samples": 5, "xi": 0.05, "min_cluster_size": 5},
        "kmeans": {"init": "predefined", "random_state": 42},
    },
}


@pytest.fixture(scope="module")
def data():
    rng = np.random.default_rng(1)
    rows = []
    # Category "a" in three groups; category "b" in two other groups
    for category, centers in [
        ("a", [(38.72, -9.15), (38.74, -9.13), (38.73, -9.17)]),
        ("b", [(38.715, -9.125), (38.745, -9.165)]),
    ]:
        for lat, lon in centers:
            for _ in range(10):
                rows.append(
                    {
                        "latitude": lat + rng.normal(0, 0.002),
                        "longitude": lon + rng.normal(0, 0.002),
                        "category": category,
                    }
                )
    potis = pd.DataFrame(rows)

    time_windows = pd.DataFrame([{"category": "a", "vi": 0.9, "ts": T1 - 600, "te": T1 + 600}])

    step = 0.005
    cells = [
        box(lon, lat, lon + step, lat + step)
        for lat in np.arange(38.71, 38.75, step)
        for lon in np.arange(-9.18, -9.12, step)
    ]
    zones = gpd.GeoDataFrame(
        {"hex_id": [f"h_{i}" for i in range(len(cells))]}, geometry=cells, crs="EPSG:4326"
    )
    return potis, time_windows, zones


def _run(potis, zones, evaluation_time=None, time_windows=None):
    assessor = VERUS(place_name="Synthetic", config=CONFIG, verbose=False)
    assessor.load(potis_df=potis, time_windows_df=time_windows, zones_gdf=zones)
    return assessor.run(evaluation_time=evaluation_time)


def test_only_active_potis_are_clustered(data):
    potis, time_windows, zones = data
    result = _run(potis, zones, T1, time_windows)

    used = result["input_data"]
    assert set(used["category"]) == {"a"}
    assert len(used) == (potis["category"] == "a").sum()
    assert set(result["clusters"]["category"]) == {"a"}


def test_inactive_potis_do_not_change_vulnerability(data):
    potis, time_windows, zones = data
    with_inactive = _run(potis, zones, T1, time_windows)["vulnerability_zones"]

    active = potis[potis["category"] == "a"].assign(vi=0.9)
    active_only = _run(active, zones)["vulnerability_zones"]

    merged = with_inactive[["hex_id", "value"]].merge(active_only[["hex_id", "value"]], on="hex_id")
    assert len(merged) == len(zones)
    np.testing.assert_allclose(merged["value_x"], merged["value_y"])


def test_no_active_potis_reports_error(data):
    potis, time_windows, zones = data
    result = _run(potis, zones, T_NONE, time_windows)

    assert "No POTIs active" in result["error"]
    assert result["vulnerability_zones"] is None


def test_without_time_windows_all_potis_are_clustered(data):
    potis, _, zones = data
    result = _run(potis.assign(vi=1.0), zones)

    assert len(result["input_data"]) == len(potis)
