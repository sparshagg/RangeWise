# Fuzzy System Design

## Objective
The fuzzy inference system adjusts EV range for real-world UAE driving conditions. It is intentionally compact and explainable so it can be defended in a classroom presentation.

## Modeling Strategy
- Battery percentage determines the baseline remaining range directly.
- Fuzzy logic adjusts that baseline using a hybrid set of UAE demo inputs and dataset-backed behavior inputs.
- The output is a range adjustment factor between strong reduction and near-nominal performance.

## Hybrid Design Choice
- `Ambient Temperature` and `AC Intensity` stay as explicit UAE demo inputs because they are central to the classroom problem statement.
- `Speed`, `Driving Mode`, and `Traffic Condition` are aligned with the Kaggle dataset so the model is not purely hand-waved.
- This keeps the project presentation-friendly while still grounding the model in the available data.

## Inputs
### Battery Percentage
- Used deterministically for baseline remaining range
- Not treated as the main uncertainty source

### Ambient Temperature
UAE-calibrated temperature bands:
- `Mild`: cooler months and nighttime driving
- `Warm`: common daytime conditions
- `Hot`: strong summer heat and harsh urban conditions

Suggested operating interpretation:
- Mild: around `18C to 28C`
- Warm: around `24C to 40C`
- Hot: above `36C`, with strongest penalty in the `42C+` range

### AC Intensity
- `Low`: light cabin cooling
- `Medium`: normal AC use
- `High`: sustained heavy cooling in hot conditions

### Speed
Dataset-driven speed bands:
- `Urban`: lower-speed city driving
- `Mixed`: common everyday mixed-speed travel
- `Highway`: sustained high-speed travel

Suggested operating interpretation:
- Urban: around `0 to 50 km/h`
- Mixed: around `40 to 85 km/h`
- Highway: above `75 km/h`, with strongest penalty near `95+ km/h`

### Driving Mode
- `Eco`: conservative energy-saving mode
- `Normal`: balanced everyday mode
- `Sport`: higher-performance mode with stronger energy demand

### Traffic Condition
- `Light`: open roads
- `Moderate`: normal city flow
- `Heavy`: stop-and-go urban traffic

## Output
### Adjustment Factor
Range factor applied to the baseline remaining range:
- `Severe Reduction`
- `Moderate Reduction`
- `Mild Reduction`
- `Near Nominal`

## Rule Themes
- Hot weather and strong AC together create major range penalties.
- High speed and sport mode create strong range penalties.
- Heavy traffic and high AC add a secondary penalty layer.
- Mild or warm weather, low AC, eco mode, and light traffic preserve range better.
- UAE summer-like conditions should show clearly lower adjusted range than mild conditions.
- Dataset-backed speed behavior should be visible in both the rules and the insight panel.

## Why This Fits The Course
- Uses fuzzy sets and linguistic rules rather than fixed thresholds
- Handles gray areas between mild and harsh conditions
- Produces interpretable outputs that are easy to explain
