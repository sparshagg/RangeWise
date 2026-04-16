# Fuzzy System Design

## Objective
The range model estimates EV range for real-world UAE driving conditions using a dataset-backed shown-range stage followed by a compact fuzzy UAE thermal correction. It is intentionally explainable so it can be defended in a classroom presentation.

## Modeling Strategy
- Battery percentage determines the claimed remaining range directly.
- The dataset computes a shown-range multiplier from `speed`, `driving mode`, and `traffic`.
- Fuzzy logic then adjusts that shown range using only UAE `temperature` and `AC`.
- The output is three range values: claimed, shown, and adjusted.

## Hybrid Design Choice
- `Ambient Temperature` and `AC Intensity` stay as explicit UAE demo inputs because they are central to the classroom problem statement.
- `Speed`, `Driving Mode`, and `Traffic Condition` are aligned with the Kaggle dataset and now drive the shown-range estimate directly.
- This keeps the project presentation-friendly while using the data in the actual range calculation rather than only in charts.
- The dataset is not UAE-native and has no AC column, so heat and AC remain domain-driven rather than learned directly.
- The dataset has no direct samples above `120 km/h`, so `Fast Highway` and `Extreme Highway` use the nearest highway bucket with an additional explicit high-speed penalty.

## Inputs
### Battery Percentage
- Used deterministically for claimed remaining range
- Not treated as the main uncertainty source

### Ambient Temperature
UAE-calibrated temperature bands:
- `Pleasant`: cooler UAE driving conditions
- `Hot`: common warm daytime conditions
- `Very Hot`: strong summer heat
- `Extremely Hot`: harsh peak summer conditions

Suggested operating interpretation:
- Pleasant: around `20C to 28C`
- Hot: around `30C to 38C`
- Very Hot: around `40C to 46C`
- Extremely Hot: `48C+`

### AC Intensity
- `Low`: light cabin cooling
- `Medium`: normal AC use
- `High`: sustained heavy cooling in hot conditions

### Speed
UAE-focused speed bands:
- `Local`: roads around `40-50 km/h`
- `City`: common urban travel around `60 km/h`
- `Highway`: common highway travel around `100-120 km/h`
- `Fast Highway`: high-speed roads around `130-140 km/h`
- `Extreme Highway`: harsh high-speed scenario around `140-160 km/h`

Suggested operating interpretation:
- Local: around `45 km/h`
- City: around `60 km/h`
- Highway: around `110 km/h`
- Fast Highway: around `135 km/h`
- Extreme Highway: around `155 km/h`

### Driving Mode
- `Eco`: conservative energy-saving mode
- `Comfort`: balanced everyday mode
- `Sport`: higher-performance mode with stronger energy demand

### Traffic Level
- `No Traffic`: open roads
- `Moderate`: normal city flow
- `High`: stop-and-go urban traffic

## Dataset Stage
- Compute `km_per_kwh = distance_travelled_km / energy_consumption_kwh`
- Aggregate median efficiency by `speed level`, `driving mode`, and `traffic level`
- Use `City / Comfort / Moderate` as the reference bucket when available
- Convert the selected bucket to a shown-range multiplier relative to the reference
- Use fallback order:
  - exact `speed + mode + traffic`
  - `speed + mode`
  - `speed`
  - global median

## Fuzzy Output
### Fuzzy UAE Adjustment Factor
Thermal factor applied to the shown range:
- bounded between `0.82` and `1.08`
- allows modest uplift for `Pleasant + Low AC`
- applies stronger reductions for `Very Hot` or `Extremely Hot` with higher AC

## Rule Themes
- Dataset stage:
  - higher-speed buckets reduce shown range more than lower-speed buckets
  - `Sport` must reduce shown range more than `Comfort`, and `Comfort` more than `Eco`
  - harsher traffic should reduce shown range when the grouped data supports it
- Fuzzy stage:
  - extremely hot weather and high AC create the strongest thermal penalties
  - pleasant weather with low AC can slightly increase range relative to the shown estimate
  - the fuzzy stage adjusts the shown range, not the claimed range directly

## Robustness Rules
- Every selectable UI value must belong to at least one fuzzy set.
- Every selectable temperature/AC combination must activate at least one rule path to the output.
- Dataset lookup always resolves through explicit fallback logic so shown range never goes missing.
- The final range is capped to avoid unrealistic overstatement relative to the claimed battery-scaled value.

## Why This Fits The Course
- Uses fuzzy sets and linguistic rules rather than fixed thresholds
- Uses the dataset to quantify normal efficiency conditions and fuzzy logic to handle thermal gray areas
- Produces interpretable outputs that are easy to explain
