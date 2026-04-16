from src.config import (
    AC_LEVEL_VALUES,
    FUZZY_FACTOR_MAX,
    FUZZY_FACTOR_MIN,
    TEMPERATURE_LEVEL_VALUES,
)
from src.fuzzy.inference import predict_adjusted_range


def test_harsh_conditions_reduce_range_more_than_mild_conditions(range_model_dataset) -> None:
    mild = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Pleasant",
        ac_level="Low",
        speed_level="City",
        driving_mode="Eco",
        traffic_level="No Traffic",
        dataset=range_model_dataset,
    )
    harsh = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Extremely Hot",
        ac_level="High",
        speed_level="Extreme Highway",
        driving_mode="Sport",
        traffic_level="High",
        dataset=range_model_dataset,
    )

    assert harsh["adjusted_range_km"] < mild["adjusted_range_km"]
    assert harsh["fuzzy_adjustment_factor"] < mild["fuzzy_adjustment_factor"]
    assert harsh["dataset_multiplier"] < mild["dataset_multiplier"]


def test_adjusted_range_never_goes_negative(range_model_dataset) -> None:
    result = predict_adjusted_range(
        manufacturer_range_km=500,
        battery_pct=0,
        temperature_level="Extremely Hot",
        ac_level="High",
        speed_level="Extreme Highway",
        driving_mode="Sport",
        traffic_level="High",
        dataset=range_model_dataset,
    )

    assert result["claimed_remaining_km"] == 0
    assert result["shown_range_km"] == 0
    assert result["adjusted_range_km"] == 0


def test_dataset_speed_levels_reduce_shown_range_progressively(range_model_dataset) -> None:
    city = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    highway = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Highway",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    extreme = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Extreme Highway",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )

    assert city["shown_range_km"] > highway["shown_range_km"] > extreme["shown_range_km"]


def test_dataset_driving_mode_reduces_shown_range_progressively(range_model_dataset) -> None:
    eco = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Highway",
        driving_mode="Eco",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    comfort = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Highway",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    sport = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="Highway",
        driving_mode="Sport",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )

    assert eco["shown_range_km"] > comfort["shown_range_km"] > sport["shown_range_km"]


def test_fuzzy_ac_levels_adjust_final_range_progressively(range_model_dataset) -> None:
    low = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Very Hot",
        ac_level="Low",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    medium = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Very Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    high = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Very Hot",
        ac_level="High",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )

    assert low["fuzzy_adjustment_factor"] > medium["fuzzy_adjustment_factor"] > high["fuzzy_adjustment_factor"]
    assert low["adjusted_range_km"] > medium["adjusted_range_km"] > high["adjusted_range_km"]


def test_fuzzy_temperature_levels_reduce_range_progressively(range_model_dataset) -> None:
    pleasant = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Pleasant",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    hot = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    very_hot = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Very Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    extreme = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Extremely Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )

    assert pleasant["fuzzy_adjustment_factor"] > hot["fuzzy_adjustment_factor"] > very_hot["fuzzy_adjustment_factor"] > extreme["fuzzy_adjustment_factor"]


def test_traffic_levels_reduce_shown_range_progressively(range_model_dataset) -> None:
    no_traffic = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="No Traffic",
        dataset=range_model_dataset,
    )
    moderate = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )
    high = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_level="Hot",
        ac_level="Medium",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="High",
        dataset=range_model_dataset,
    )

    assert no_traffic["shown_range_km"] > moderate["shown_range_km"] > high["shown_range_km"]


def test_all_linguistic_ui_combinations_return_fuzzy_output(range_model_dataset) -> None:
    for temperature_level in TEMPERATURE_LEVEL_VALUES.keys():
        for ac_level in AC_LEVEL_VALUES.keys():
            result = predict_adjusted_range(
                manufacturer_range_km=450,
                battery_pct=80,
                temperature_level=temperature_level,
                ac_level=ac_level,
                speed_level="City",
                driving_mode="Comfort",
                traffic_level="Moderate",
                dataset=range_model_dataset,
            )

            assert FUZZY_FACTOR_MIN <= result["fuzzy_adjustment_factor"] <= FUZZY_FACTOR_MAX


def test_favorable_conditions_can_raise_adjusted_range_above_shown(range_model_dataset) -> None:
    result = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=100,
        temperature_level="Pleasant",
        ac_level="Low",
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
        dataset=range_model_dataset,
    )

    assert result["adjusted_range_km"] > result["shown_range_km"]


def test_adjusted_range_is_capped_against_claimed_remaining(range_model_dataset) -> None:
    result = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=100,
        temperature_level="Pleasant",
        ac_level="Low",
        speed_level="Local",
        driving_mode="Eco",
        traffic_level="No Traffic",
        dataset=range_model_dataset,
    )

    assert result["adjusted_range_km"] <= result["claimed_remaining_km"] * 1.15
