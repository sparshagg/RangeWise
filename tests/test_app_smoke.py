from src.app import build_dashboard_payload, load_dashboard_dataset
from src.ui.controls import UserInputs


def test_build_dashboard_payload_returns_expected_keys() -> None:
    payload = build_dashboard_payload(
        UserInputs(
            manufacturer_range_km=450,
            battery_pct=85,
            temperature_level="Hot",
            ac_level="Medium",
            speed_level="City",
            driving_mode="Comfort",
            traffic_level="Moderate",
        )
    )

    assert "adjusted_range_km" in payload
    assert "summary" in payload
    assert isinstance(payload["drivers"], list)


def test_load_dashboard_dataset_surfaces_missing_dataset() -> None:
    dataset, error_message = load_dashboard_dataset("missing.csv")
    assert dataset is None
    assert error_message is not None
