# Presentation Notes

## Problem Statement
Standard EV range displays can feel simplistic because they often do not reflect how real-world conditions reduce available range. Fuzzy logic is useful because it can model uncertain and gradual effects instead of using hard thresholds.

## Why UAE Matters
- High ambient temperatures are common for much of the year.
- AC usage is a practical necessity, not a minor factor.
- Urban traffic and highway commuting both affect consumption.

## Demo Story
1. Start with a nominal manufacturer range.
2. Apply battery percentage to show the naive baseline.
3. Move the temperature from `Pleasant` to `Very Hot` or `Extremely Hot` and increase AC load.
4. Move the speed from `City` to `Highway` or `Fast Highway`.
5. Compare `Eco`, `Comfort`, and `Sport`.
6. Increase traffic from `No Traffic` to `High`.
6. Show the explanation text and speed-based dataset insights.

## Key Talking Points
- Fuzzy logic models gradual transitions between mild, warm, and hot conditions.
- The system is interpretable because each output comes from understandable rules.
- The project uses a hybrid design: UAE heat and AC are domain-driven, while speed is strongly justified by the dataset and the other factors are encoded as explicit fuzzy rules.
- The project focuses on explainability and academic demonstration rather than production deployment.
