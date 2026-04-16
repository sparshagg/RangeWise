from src.fuzzy.inference import predict_adjusted_range


def test_harsh_conditions_reduce_range_more_than_mild_conditions() -> None:
    mild = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_c=24,
        ac_intensity=2,
        driving_style=2,
        traffic_level=2,
    )
    harsh = predict_adjusted_range(
        manufacturer_range_km=450,
        battery_pct=80,
        temperature_c=46,
        ac_intensity=9,
        driving_style=8,
        traffic_level=8,
    )

    assert harsh["adjusted_range_km"] < mild["adjusted_range_km"]
    assert harsh["adjustment_factor"] < mild["adjustment_factor"]


def test_adjusted_range_never_goes_negative() -> None:
    result = predict_adjusted_range(
        manufacturer_range_km=500,
        battery_pct=0,
        temperature_c=50,
        ac_intensity=10,
        driving_style=10,
        traffic_level=10,
    )

    assert result["baseline_remaining_km"] == 0
    assert result["adjusted_range_km"] == 0

