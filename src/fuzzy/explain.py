from __future__ import annotations


from src.config import DRIVING_MODE_LABELS, TRAFFIC_CONDITION_LABELS


def build_explanation(
    *,
    battery_pct: float,
    temperature_c: float,
    ac_intensity: float,
    speed_kmh: float,
    driving_mode: float,
    traffic_condition: float,
    adjustment_factor: float,
) -> dict[str, str | list[str]]:
    drivers: list[str] = []
    driving_mode_label = DRIVING_MODE_LABELS.get(int(round(driving_mode)), "Unknown")
    traffic_condition_label = TRAFFIC_CONDITION_LABELS.get(
        int(round(traffic_condition)), "Unknown"
    )

    if battery_pct <= 25:
        drivers.append("Low battery state is already limiting the remaining baseline range.")
    if temperature_c >= 40:
        drivers.append("Hot UAE ambient temperature is increasing EV energy demand.")
    elif temperature_c >= 30:
        drivers.append("Warm ambient temperature is creating a moderate heat penalty.")

    if ac_intensity >= 7:
        drivers.append("Strong AC usage is reducing range to maintain cabin comfort.")
    elif ac_intensity <= 3:
        drivers.append("Light AC usage helps preserve range.")

    if speed_kmh >= 90:
        drivers.append("Highway-speed demand is one of the strongest range penalties in the dataset.")
    elif speed_kmh <= 40:
        drivers.append("Urban or moderate speed helps keep energy demand lower.")

    if driving_mode_label == "Sport":
        drivers.append("Sport driving mode increases power demand and reduces range.")
    elif driving_mode_label == "Eco":
        drivers.append("Eco driving mode helps preserve range under the same conditions.")

    if traffic_condition_label == "Heavy":
        drivers.append("Heavy traffic adds stop-and-go inefficiency.")
    elif traffic_condition_label == "Light":
        drivers.append("Light traffic supports smoother, more efficient travel.")

    if not drivers:
        drivers.append("Conditions are balanced, so the estimated range remains near the baseline.")

    if adjustment_factor < 0.7:
        summary = "Harsh UAE driving conditions are causing a strong range reduction."
    elif adjustment_factor < 0.86:
        summary = "Current conditions are causing a noticeable range reduction."
    elif adjustment_factor < 0.95:
        summary = "Conditions are only slightly below ideal for EV range."
    else:
        summary = "Conditions are favorable and the EV stays close to its nominal range."

    return {
        "summary": summary,
        "drivers": drivers,
    }
