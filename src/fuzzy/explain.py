from __future__ import annotations


def build_explanation(
    *,
    battery_pct: float,
    temperature_level: str,
    ac_level: str,
    speed_level: str,
    driving_mode: str,
    traffic_level: str,
    dataset_multiplier: float,
    fuzzy_adjustment_factor: float,
    dataset_fallback_level: str,
    proxy_speed_level: str,
    sample_count: int,
) -> dict[str, str | list[str]]:
    drivers: list[str] = []

    if battery_pct <= 25:
        drivers.append("Low battery state is already limiting the claimed remaining range.")

    if dataset_multiplier >= 1.04:
        dataset_summary_driver = (
            f"The dataset-backed shown range is above the claimed battery-scaled range because "
            f"{driving_mode} driving with {traffic_level.lower()} traffic is relatively efficient for the selected speed."
        )
    elif dataset_multiplier >= 0.98:
        dataset_summary_driver = (
            "The dataset-backed shown range stays close to the claimed battery-scaled range under the selected road conditions."
        )
    else:
        dataset_summary_driver = (
            f"The dataset-backed shown range is lower than the claimed battery-scaled range because "
            f"{speed_level.lower()} driving, {driving_mode.lower()} mode, or traffic conditions increase expected energy use."
        )

    if proxy_speed_level != speed_level:
        drivers.append(
            f"The dataset does not contain enough direct samples for {speed_level.lower()} speeds, so the shown-range stage uses the nearest {proxy_speed_level.lower()} dataset bucket with an extra high-speed penalty."
        )
    elif dataset_fallback_level != "exact":
        drivers.append(
            f"The shown-range estimate uses a {dataset_fallback_level.replace('_', ' ')} fallback bucket with {sample_count} supporting rows."
        )
    else:
        drivers.append(
            f"The shown-range estimate uses an exact dataset bucket with {sample_count} matching rows."
        )

    if temperature_level == "Extremely Hot":
        fuzzy_summary_driver = "Extremely hot UAE weather adds the strongest thermal penalty to the shown range."
        drivers.append("Extremely hot UAE weather is creating the harshest thermal penalty.")
    elif temperature_level == "Very Hot":
        fuzzy_summary_driver = "Very hot weather applies a clear UAE heat penalty on top of the shown range."
        drivers.append("Very hot weather is adding a strong heat penalty.")
    elif temperature_level == "Hot":
        fuzzy_summary_driver = "Hot weather trims the shown range slightly because the battery and cabin cooling load stay elevated."
        drivers.append("Hot weather is slightly reducing the expected range.")
    else:
        fuzzy_summary_driver = "Pleasant UAE weather allows a small thermal recovery over the shown range."
        drivers.append("Pleasant weather keeps thermal stress on the vehicle lower.")

    if ac_level == "High":
        drivers.append("High AC demand is reducing range to maintain cabin comfort.")
    elif ac_level == "Medium":
        drivers.append("Medium AC usage adds a moderate auxiliary load.")
    else:
        drivers.append("Low AC usage helps preserve battery range.")

    if driving_mode == "Sport":
        drivers.append("Sport driving mode increases power demand and lowers the dataset-backed shown range.")
    elif driving_mode == "Comfort":
        drivers.append("Comfort mode balances performance and efficiency in the dataset-backed stage.")
    elif driving_mode == "Eco":
        drivers.append("Eco driving mode helps preserve range under the same dataset conditions.")

    if fuzzy_adjustment_factor >= 1.03:
        summary = "Favorable UAE weather is slightly increasing the final range above the dataset-backed shown estimate."
    elif fuzzy_adjustment_factor >= 0.98:
        summary = "Dataset conditions dominate this case, while UAE temperature and AC keep the final range near the shown estimate."
    else:
        summary = "UAE temperature and AC are reducing the final range below the dataset-backed shown estimate."

    return {
        "summary": summary,
        "dataset_summary_driver": dataset_summary_driver,
        "fuzzy_summary_driver": fuzzy_summary_driver,
        "drivers": drivers,
    }
