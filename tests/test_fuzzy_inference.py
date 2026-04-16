from itertools import product

from src.config import (
    AC_LEVEL_VALUES,
    DRIVING_MODE_LEVEL_VALUES,
    SPEED_LEVEL_VALUES,
    TEMPERATURE_LEVEL_VALUES,
    TRAFFIC_LEVEL_VALUES,
)
from src.fuzzy.inference import predict_adjusted_range


def test_harsh_conditions_reduce_range_more_than_mild_conditions() -> None:
    mild = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Pleasant",
        ac_level="Low",
        speed_level="Local",
        driving_mode="Eco",
        traffic_level="No Traffic",
    )
    harsh = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Extremely Hot",
        ac_level="High",
        speed_level="Extreme Highway",
        driving_mode="Sport",
        traffic_level="High",
    )

    assert harsh["adjusted_range_km"] < mild["adjusted_range_km"]
    assert harsh["adjustment_factor"] < mild["adjustment_factor"]


def test_adjusted_range_never_goes_negative() -> None:
    result = predict_adjusted_range(
        manufacturer_range_km=500,
        battery_pct=0,
        temperature_level="Extremely Hot",
        ac_level="High",
        speed_level="Extreme Highway",
        driving_mode="Sport",
        traffic_level="High",
    )

    assert result["baseline_remaining_km"] == 0
    assert result["adjusted_range_km"] == 0

def test_speed_levels_reduce_range_progressively() -> None:
    city = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )
    highway = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Highway",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )
    extreme = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Extreme Highway",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )

    assert city["adjusted_range_km"] > highway["adjusted_range_km"] > extreme["adjusted_range_km"]


def test_driving_mode_reduces_range_progressively() -> None:
    eco = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Highway",
        driving_mode="Eco",
        traffic_level="Moderate",
    )
    comfort = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Highway",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )
    sport = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Highway",
        driving_mode="Sport",
        traffic_level="Moderate",
    )

    assert eco["adjusted_range_km"] > comfort["adjusted_range_km"] > sport["adjusted_range_km"]


def test_ac_levels_reduce_range_progressively() -> None:
    low = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Very Hot",
        ac_level="Low",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )
    medium = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Very Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )
    high = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Very Hot",
        ac_level="High",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )

    assert low["adjusted_range_km"] > medium["adjusted_range_km"] > high["adjusted_range_km"]


def test_temperature_levels_reduce_range_progressively() -> None:
    pleasant = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Pleasant",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )
    hot = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )
    very_hot = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Very Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )
    extreme = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Extremely Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )

    assert pleasant["adjusted_range_km"] > hot["adjusted_range_km"] > very_hot["adjusted_range_km"] > extreme["adjusted_range_km"]


def test_traffic_levels_reduce_range_progressively() -> None:
    no_traffic = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="No Traffic",
    )
    moderate = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )
    high = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="High",
    )

    assert no_traffic["adjusted_range_km"] > moderate["adjusted_range_km"] > high["adjusted_range_km"]


def test_all_linguistic_ui_combinations_return_adjustment_factor() -> None:
    for temperature_level, ac_level, speed_level, driving_mode, traffic_level in product(
        TEMPERATURE_LEVEL_VALUES.keys(),
        AC_LEVEL_VALUES.keys(),
        SPEED_LEVEL_VALUES.keys(),
        DRIVING_MODE_LEVEL_VALUES.keys(),
        TRAFFIC_LEVEL_VALUES.keys(),
    ):
        result = predict_adjusted_range(
            manufacturer_range_km=450,
            battery_pct=80,
            temperature_level=temperature_level,
            ac_level=ac_level,
            speed_level=speed_level,
            driving_mode=driving_mode,
            traffic_level=traffic_level,
        )

        assert "adjustment_factor" in result
