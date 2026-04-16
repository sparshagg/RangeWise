# Fuzzy Design Skill

## Purpose
Guide fuzzy logic updates so they stay explainable and classroom-ready.

## Rules
- Keep the number of inputs small and presentation-friendly.
- Use linguistic labels as the primary user-facing fuzzy interface.
- Preserve UAE calibration for heat, AC, and speed assumptions unless the project scope changes.
- Never leave a user-selectable state outside all membership functions.
- Never leave a user-selectable factor without at least one rule path to the output.
- Add broad fallback coverage rules so inference always returns an output.
- Write directional tests for every major factor: temperature, AC, speed, mode, and traffic.
- Write combination coverage tests across representative input-space samples before considering the model complete.
- Prefer explainable rule tables over sparse ad hoc rules.
