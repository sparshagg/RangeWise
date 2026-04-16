from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "ev_energy_consumption_dataset.csv"

EXPECTED_COLUMNS = {
    "timestamp": ["timestamp", "Timestamp"],
    "vehicle_id": ["vehicle_id", "Vehicle ID", "Vehicle_ID"],
    "speed": ["speed", "Speed"],
    "acceleration": ["acceleration", "Acceleration"],
    "driving_mode": ["driving_mode", "Driving Mode", "Driving_Mode"],
    "road_type": ["road_type", "Road Type", "Road_Type"],
    "traffic_level": [
        "traffic_level",
        "Traffic Level",
        "Traffic_Level",
        "Traffic Conditions",
    ],
    "slope_pct": ["slope_pct", "Slope Percentage", "Slope", "Slope_Pct"],
    "temperature_c": ["temperature_c", "Temperature", "temperature"],
    "humidity_pct": ["humidity_pct", "Humidity", "humidity"],
    "wind_speed": ["wind_speed", "Wind Speed", "Wind_Speed"],
    "weather_type": ["weather_type", "Weather Type", "Weather_Type"],
    "battery_state_pct": [
        "battery_state_pct",
        "Battery State",
        "Battery State of Charge",
        "State of Charge",
    ],
    "voltage_v": ["voltage_v", "Voltage", "voltage"],
    "battery_temp_c": [
        "battery_temp_c",
        "Battery Temperature",
        "Battery_Temperature",
    ],
    "tire_pressure_psi": ["tire_pressure_psi", "Tire Pressure", "Tire_Pressure"],
    "energy_consumption_kwh": [
        "energy_consumption_kwh",
        "Energy Consumption (kWh)",
        "Energy Consumption",
    ],
}

REQUIRED_CANONICAL_COLUMNS = [
    "speed",
    "acceleration",
    "temperature_c",
    "battery_state_pct",
    "energy_consumption_kwh",
]

