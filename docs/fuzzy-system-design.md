# Fuzzy System Design

## Objective
The fuzzy inference system adjusts EV range for real-world UAE driving conditions. It is intentionally compact and explainable so it can be defended in a classroom presentation.

## Modeling Strategy
- Battery percentage determines the baseline remaining range directly.
- Fuzzy logic adjusts that baseline using environmental and behavioral conditions.
- The output is a range adjustment factor between strong reduction and near-nominal performance.

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

### Driving Style
- `Efficient`: smooth acceleration and moderate speed
- `Balanced`: average mixed driving
- `Aggressive`: sharp acceleration and inefficient usage

### Traffic Level
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
- Aggressive driving and heavy traffic amplify consumption.
- Mild weather, light AC, efficient driving, and light traffic preserve range.
- UAE summer-like conditions should show clearly lower adjusted range than mild conditions.

## Why This Fits The Course
- Uses fuzzy sets and linguistic rules rather than fixed thresholds
- Handles gray areas between mild and harsh conditions
- Produces interpretable outputs that are easy to explain

