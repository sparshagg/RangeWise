# Fuzzy System Design

## Objective
The fuzzy inference system adjusts EV range for real-world UAE driving conditions. It is intentionally compact and explainable so it can be defended in a classroom presentation.

## Modeling Strategy
- Battery percentage determines the baseline remaining range directly.
- Fuzzy logic adjusts that baseline using a linguistic set of UAE demo inputs plus dataset-backed speed justification.
- The output is a range adjustment factor between strong reduction and near-nominal performance.

## Hybrid Design Choice
- `Ambient Temperature` and `AC Intensity` stay as explicit UAE demo inputs because they are central to the classroom problem statement.
- `Speed`, `Driving Mode`, and `Traffic Condition` are aligned with the Kaggle dataset for justification, but the app presents them as linguistic fuzzy sets.
- This keeps the project presentation-friendly while still grounding the model in the available data.
- The dataset is not UAE-native and has no AC column, so heat and AC remain domain-driven rather than learned directly.

## Inputs
### Battery Percentage
- Used deterministically for baseline remaining range
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

## Output
### Adjustment Factor
Range factor applied to the baseline remaining range:
- `Severe Reduction`
- `Moderate Reduction`
- `Mild Reduction`
- `Near Nominal`

## Rule Themes
- Extremely hot weather and high AC create major range penalties.
- Fast and extreme highway speeds create the strongest speed penalties.
- Sport mode must reduce range more than Comfort, and Comfort more than Eco.
- High traffic must reduce range more than Moderate, and Moderate more than No Traffic.
- Pleasant weather, low AC, local or city speeds, Eco mode, and No Traffic should preserve range best.
- Dataset-backed speed behavior should be visible in both the rules and the insight panel.

## Robustness Rules
- Every selectable UI value must belong to at least one fuzzy set.
- Every selectable combination must activate at least one rule path to the output.
- The rule base includes broad fallback coverage so defuzzification never returns a missing output.

## Why This Fits The Course
- Uses fuzzy sets and linguistic rules rather than fixed thresholds
- Handles gray areas between mild and harsh conditions
- Produces interpretable outputs that are easy to explain
