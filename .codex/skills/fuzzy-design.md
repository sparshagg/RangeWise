# Fuzzy Design Skill

## Purpose
Guide fuzzy logic updates so they stay explainable and classroom-ready.

## Rules
- Keep the number of inputs small and presentation-friendly.
- Use linguistic labels as the primary user-facing fuzzy interface.
- Preserve UAE calibration for heat, speed, and traffic assumptions unless the project scope changes.
- Treat dataset-backed efficiency and fuzzy UAE correction as separate stages when range math is revised.
- Never leave a user-selectable state outside all membership functions.
- Never leave a user-selectable temperature or AC state without at least one rule path to the fuzzy output.
- Add broad fallback coverage rules so inference always returns an output.
- Resolve dataset buckets with explicit fallback order and test each fallback path.
- Write directional tests for every major factor: dataset speed/mode/traffic and fuzzy temperature/AC/speed/mode/traffic.
- Write combination coverage tests across representative input-space samples before considering the model complete.
- Prefer explainable rule tables over sparse ad hoc rules.
- Do not let fuzzy logic silently replace the dataset-backed shown-range stage.
