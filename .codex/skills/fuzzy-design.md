# Fuzzy Design Skill

## Purpose
Guide fuzzy and neuro-fuzzy updates so they stay explainable and classroom-ready.

## Rules
- Keep the number of user-facing inputs small and presentation-friendly.
- Use linguistic labels as the primary interface for fuzzy inputs.
- Preserve UAE calibration for heat, speed, and traffic assumptions unless the scope changes.
- Keep the three-stage flow explicit:
  - `Claimed Remaining`
  - `Shown Range` from dataset-backed grouped efficiency
  - `Fuzzy-Only Range`, with optional ANFIS-backed `Hybrid Range`
- Never leave a user-selectable state outside all membership functions.
- Never leave a user-selectable state without at least one rule path to the fuzzy output.
- Add broad fallback coverage rules so fuzzy inference always returns an output.
- Resolve dataset buckets with explicit fallback order and test each fallback path.
- Keep ANFIS as a comparative enhancement layer, not a replacement for the explainable fuzzy baseline.
- Write directional tests for every major factor: dataset speed/mode/traffic and fuzzy temperature/AC/speed/mode/traffic.
- Write combination coverage tests across representative input-space samples before considering the model complete.
