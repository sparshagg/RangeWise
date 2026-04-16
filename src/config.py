from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "EV_Energy_Consumption_Dataset.csv"
PROCESSED_DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "EV_Range_Model_Processed.csv"

SPEED_LEVEL_BINS = [0, 50, 80, 120, 140, float("inf")]
SPEED_LEVEL_LABELS = [
    "Local",
    "City",
    "Highway",
    "Fast Highway",
    "Extreme Highway",
]
SPEED_LEVEL_PROXY = {
    "Local": "Local",
    "City": "City",
    "Highway": "Highway",
    "Fast Highway": "Highway",
    "Extreme Highway": "Highway",
}
SPEED_LEVEL_EXTRAPOLATION = {
    "Local": 1.0,
    "City": 1.0,
    "Highway": 1.0,
    "Fast Highway": 0.93,
    "Extreme Highway": 0.87,
}
REFERENCE_RANGE_BUCKET = ("City", "Comfort", "Moderate")
EXACT_GROUP_MIN_COUNT = 20
SPEED_MODE_MIN_COUNT = 40
SPEED_MIN_COUNT = 80
FUZZY_FACTOR_MIN = 0.82
FUZZY_FACTOR_MAX = 1.08
FINAL_RANGE_CLAIM_CAP = 1.15

TEMPERATURE_LEVEL_VALUES = {
    "Pleasant": 24.0,
    "Hot": 34.0,
    "Very Hot": 43.0,
    "Extremely Hot": 52.0,
}
TEMPERATURE_LEVEL_RANGES = {
    "Pleasant": "20C to 28C",
    "Hot": "30C to 38C",
    "Very Hot": "40C to 46C",
    "Extremely Hot": "48C and above",
}

AC_LEVEL_VALUES = {
    "Low": 2.0,
    "Medium": 5.0,
    "High": 8.0,
}
AC_LEVEL_GUIDE = {
    "Low": "light cabin cooling",
    "Medium": "normal UAE cabin cooling",
    "High": "strong sustained cooling demand",
}

SPEED_LEVEL_VALUES = {
    "Local": 45.0,
    "City": 60.0,
    "Highway": 110.0,
    "Fast Highway": 135.0,
    "Extreme Highway": 155.0,
}
SPEED_LEVEL_RANGES = {
    "Local": "40 to 50 km/h",
    "City": "51 to 80 km/h",
    "Highway": "81 to 120 km/h",
    "Fast Highway": "121 to 140 km/h",
    "Extreme Highway": "141 to 160+ km/h",
}

DRIVING_MODE_LEVEL_VALUES = {
    "Eco": 1.1,
    "Comfort": 2.0,
    "Sport": 2.9,
}
DRIVING_MODE_GUIDE = {
    "Eco": "efficiency-priority driving",
    "Comfort": "balanced daily driving",
    "Sport": "higher-performance driving",
}

TRAFFIC_LEVEL_VALUES = {
    "No Traffic": 1.1,
    "Moderate": 2.0,
    "High": 2.9,
}
TRAFFIC_LEVEL_GUIDE = {
    "No Traffic": "open-flow traffic",
    "Moderate": "normal city flow",
    "High": "heavy stop-and-go traffic",
}

DATASET_DRIVING_MODE_LABELS = {
    1: "Eco",
    2: "Comfort",
    3: "Sport",
}

DATASET_TRAFFIC_CONDITION_LABELS = {
    1: "No Traffic",
    2: "Moderate",
    3: "High",
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
