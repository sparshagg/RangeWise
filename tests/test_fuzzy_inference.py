from src.fuzzy.inference import predict_adjusted_range


def test_harsh_conditions_reduce_range_more_than_mild_conditions() -> None:
    mild = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_c=24,
        ac_intensity=2,
        speed_kmh=45,
        driving_mode=1,
        traffic_condition=1,
    )
    harsh = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_c=46,
        ac_intensity=9,
        speed_kmh=110,
        driving_mode=3,
        traffic_condition=3,
    )

    assert harsh["adjusted_range_km"] < mild["adjusted_range_km"]
    assert harsh["adjustment_factor"] < mild["adjustment_factor"]


def test_adjusted_range_never_goes_negative() -> None:
    result = predict_adjusted_range(
        manufacturer_range_km=500,
        battery_pct=0,
        temperature_c=50,
        ac_intensity=10,
        speed_kmh=120,
        driving_mode=3,
        traffic_condition=3,
    )

    assert result["baseline_remaining_km"] == 0
    assert result["adjusted_range_km"] == 0


def test_high_speed_reduces_range_more_than_moderate_speed() -> None:
    moderate_speed = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_c=34,
        ac_intensity=5,
        speed_kmh=55,
        driving_mode=2,
        traffic_condition=2,
    )
    high_speed = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_c=34,
        ac_intensity=5,
        speed_kmh=105,
        driving_mode=2,
        traffic_condition=2,
    )

    assert high_speed["adjusted_range_km"] < moderate_speed["adjusted_range_km"]
