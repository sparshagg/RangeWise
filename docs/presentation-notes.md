# Presentation Notes

## Problem Statement
Standard EV range displays can feel simplistic because they often do not reflect how real-world conditions reduce available range. Fuzzy logic is useful because it can model uncertain and gradual effects instead of using hard thresholds.

## Why UAE Matters
- High ambient temperatures are common for much of the year.
- AC usage is a practical necessity, not a minor factor.
- Urban traffic and highway commuting both affect consumption.

## Demo Story
1. Start with a nominal manufacturer range.
2. Apply battery percentage to show the claimed remaining range.
3. Show how speed, driving mode, and traffic create the dataset-backed shown range.
4. Move the temperature from `Pleasant` to `Very Hot` or `Extremely Hot` and increase AC load.
5. Show how the fuzzy UAE correction moves the final adjusted range above or below the shown range.
6. Open the lookup details and speed-based dataset insights.

## Key Talking Points
- The project separates normal efficiency behavior from UAE thermal uncertainty.
- The dataset drives the shown range through grouped efficiency estimates.
- Fuzzy logic models gradual transitions between pleasant, hot, very hot, and extremely hot conditions.
- The system is interpretable because each output comes from understandable rules.
- The project uses a hybrid design: speed, mode, and traffic are dataset-backed, while UAE heat and AC remain domain-driven.
- The project focuses on explainability and academic demonstration rather than production deployment.
