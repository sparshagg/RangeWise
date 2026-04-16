from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _build_rows(
    *,
    speed: float,
    driving_mode: int,
    traffic_level: int,
    km_per_kwh: float,
    count: int,
) -> list[dict[str, float | int]]:
    return [
        {
            "speed": speed,
            "driving_mode": driving_mode,
            "traffic_level": traffic_level,
            "distance_travelled_km": km_per_kwh * 10,
            "energy_consumption_kwh": 10.0,
        }
        for _ in range(count)
    ]


@pytest.fixture
def range_model_dataset() -> pd.DataFrame:
    rows: list[dict[str, float | int]] = []
    rows.extend(_build_rows(speed=65, driving_mode=2, traffic_level=2, km_per_kwh=3.0, count=120))
    rows.extend(_build_rows(speed=65, driving_mode=1, traffic_level=1, km_per_kwh=3.5, count=80))
    rows.extend(_build_rows(speed=65, driving_mode=2, traffic_level=1, km_per_kwh=3.2, count=40))
    rows.extend(_build_rows(speed=65, driving_mode=2, traffic_level=3, km_per_kwh=2.6, count=40))
    rows.extend(_build_rows(speed=65, driving_mode=3, traffic_level=3, km_per_kwh=2.3, count=70))
    rows.extend(_build_rows(speed=110, driving_mode=2, traffic_level=2, km_per_kwh=2.6, count=90))
    rows.extend(_build_rows(speed=110, driving_mode=1, traffic_level=1, km_per_kwh=2.9, count=40))
    rows.extend(_build_rows(speed=110, driving_mode=1, traffic_level=2, km_per_kwh=2.8, count=40))
    rows.extend(_build_rows(speed=110, driving_mode=3, traffic_level=2, km_per_kwh=2.2, count=40))
    rows.extend(_build_rows(speed=110, driving_mode=3, traffic_level=3, km_per_kwh=2.1, count=10))
    rows.extend(_build_rows(speed=45, driving_mode=2, traffic_level=1, km_per_kwh=3.8, count=30))
    rows.extend(_build_rows(speed=45, driving_mode=1, traffic_level=1, km_per_kwh=4.1, count=25))
    rows.extend(_build_rows(speed=45, driving_mode=3, traffic_level=2, km_per_kwh=3.1, count=25))
    return pd.DataFrame(rows)
