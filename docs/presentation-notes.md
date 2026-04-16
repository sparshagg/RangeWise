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
3. Increase heat and AC load to represent UAE conditions.
4. Increase speed and switch to sport mode to show a sharper range drop.
5. Increase traffic condition to show the extra urban penalty.
6. Show the explanation text and speed-based dataset insights.

## Key Talking Points
- Fuzzy logic models gradual transitions between mild, warm, and hot conditions.
- The system is interpretable because each output comes from understandable rules.
- The project uses a hybrid design: UAE heat and AC are domain-driven, while speed, driving mode, and traffic condition are dataset-backed.
- The project focuses on explainability and academic demonstration rather than production deployment.
