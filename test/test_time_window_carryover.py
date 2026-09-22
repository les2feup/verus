"""Regression tests: vi values must not carry over between run() calls.

run() overwrites poti_df with the POTIs of the evaluated time. Time windows
must still be applied to the POTIs as loaded, so a category that is inactive
at the second evaluation time does not keep the vi of the first one.
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
T2 = T1 + 7_200  # only category "b" active

CONFIG = {
    "max_vulnerability": {"Synthetic": 1.0},
    "clustering": {
        "optics": {"min_samples": 5, "xi": 0.05, "min_cluster_size": 5},
        "kmeans": {"init": "predefined", "random_state": 42},
    },
}


@pytest.fixture(scope="module")
def data():
    rng = np.random.default_rng(0)
    centers = [(38.72, -9.15), (38.74, -9.13), (38.73, -9.17)]
    rows = []
    for lat, lon in centers:
        for category in ["a", "b", "c"]:
            for _ in range(8):
                rows.append(
                    {
                        "latitude": lat + rng.normal(0, 0.002),
                        "longitude": lon + rng.normal(0, 0.002),
                        "category": category,
                    }
                )
    potis = pd.DataFrame(rows)

    time_windows = pd.DataFrame(
        [
            {"category": "a", "vi": 0.9, "ts": T1 - 600, "te": T1 + 600},
            {"category": "b", "vi": 0.5, "ts": T2 - 600, "te": T2 + 600},
        ]
    )

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


def _assessor(data):
    potis, time_windows, zones = data
    assessor = VERUS(place_name="Synthetic", config=CONFIG, verbose=False)
    assessor.load(potis_df=potis, time_windows_df=time_windows, zones_gdf=zones)
    return assessor


def test_inactive_category_does_not_keep_previous_vi(data):
    assessor = _assessor(data)
    assessor.run(evaluation_time=T1)
    result = assessor.run(evaluation_time=T2)

    used = result["input_data"]
    assert set(used["category"]) == {"b"}
    assert list(used["vi"].unique()) == [0.5]


def test_sequential_runs_match_fresh_runs(data):
    sequential = _assessor(data)
    sequential.run(evaluation_time=T1)
    seq = sequential.run(evaluation_time=T2)["vulnerability_zones"]

    fresh = _assessor(data).run(evaluation_time=T2)["vulnerability_zones"]

    merged = seq[["hex_id", "value", "VL_normalized_smoothed"]].merge(
        fresh[["hex_id", "value", "VL_normalized_smoothed"]], on="hex_id"
    )
    assert len(merged) == len(fresh)
    np.testing.assert_allclose(merged["value_x"], merged["value_y"])
    np.testing.assert_allclose(
        merged["VL_normalized_smoothed_x"], merged["VL_normalized_smoothed_y"]
    )


def test_time_windows_apply_to_passed_data_source(data):
    potis, _, _ = data
    assessor = _assessor(data)
    subset = potis[potis["category"] != "c"].iloc[::2].assign(vi=0.0)

    result = assessor.run(data_source=subset, evaluation_time=T2)

    used = result["input_data"]
    assert set(used["category"]) == {"b"}
    assert len(used) == (subset["category"] == "b").sum()
    assert list(used["vi"].unique()) == [0.5]
