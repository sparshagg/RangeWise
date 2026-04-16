from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "EV_Energy_Consumption_Dataset.csv"

DRIVING_MODE_LABELS = {
    1: "Eco",
    2: "Normal",
    3: "Sport",
}

TRAFFIC_CONDITION_LABELS = {
    1: "Light",
    2: "Moderate",
    3: "Heavy",
}

EXPECTED_COLUMNS = {
    "timestamp": ["timestamp", "Timestamp"],
    "vehicle_id": ["vehicle_id", "Vehicle ID", "Vehicle_ID"],
    "speed": ["speed", "Speed", "Speed_kmh"],
    "acceleration": ["acceleration", "Acceleration", "Acceleration_ms2"],
    "driving_mode": ["driving_mode", "Driving Mode", "Driving_Mode", "Driving_Mode"],
    "road_type": ["road_type", "Road Type", "Road_Type"],
    "traffic_level": [
        "traffic_level",
        "Traffic Level",
        "Traffic_Level",
        "Traffic Conditions",
        "Traffic_Condition",
    ],
    "slope_pct": ["slope_pct", "Slope Percentage", "Slope", "Slope_Pct", "Slope_%"],
    "temperature_c": ["temperature_c", "Temperature", "temperature", "Temperature_C"],
    "humidity_pct": ["humidity_pct", "Humidity", "humidity", "Humidity_%"],
    "wind_speed": ["wind_speed", "Wind Speed", "Wind_Speed", "Wind_Speed_ms"],
    "weather_type": ["weather_type", "Weather Type", "Weather_Type", "Weather_Condition"],
    "battery_state_pct": [
        "battery_state_pct",
        "Battery State",
        "Battery State of Charge",
        "State of Charge",
        "Battery_State_%",
    ],
    "voltage_v": ["voltage_v", "Voltage", "voltage", "Battery_Voltage_V"],
    "battery_temp_c": [
        "battery_temp_c",
        "Battery Temperature",
        "Battery_Temperature",
        "Battery_Temperature_C",
    ],
    "tire_pressure_psi": ["tire_pressure_psi", "Tire Pressure", "Tire_Pressure"],
    "distance_travelled_km": ["distance_travelled_km", "Distance_Travelled_km"],
    "vehicle_weight_kg": ["vehicle_weight_kg", "Vehicle_Weight_kg"],
    "energy_consumption_kwh": [
        "energy_consumption_kwh",
        "Energy Consumption (kWh)",
        "Energy Consumption",
        "Energy_Consumption_kWh",
    ],
}

REQUIRED_CANONICAL_COLUMNS = [
    "speed",
    "acceleration",
    "temperature_c",
    "battery_state_pct",
    "energy_consumption_kwh",
]
