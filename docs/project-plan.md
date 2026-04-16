# Project Plan

## Goal
Build a local Streamlit dashboard that demonstrates how fuzzy logic can produce a more realistic EV range estimate than a naive battery-percentage calculation.

## Deliverable
- One working local app
- One explainable fuzzy model tuned for UAE conditions
- One dataset-backed analysis section
- One team-friendly README
- One living checklist for progress tracking
- One generated repository-status doc kept fresh by hook and local terminal checks

## Core Design
- Claimed remaining range = `manufacturer rated range x battery percentage`
- Shown range = `claimed remaining range x dataset multiplier`
- Dataset multiplier comes from grouped dataset efficiency for:
  - UAE speed band
  - driving mode
  - traffic level
- Fuzzy UAE correction responds to:
  - UAE temperature level
  - AC level
- Final adjusted range = `shown range x fuzzy UAE factor`, capped for realism

## Scope Boundaries
- No cloud deployment
- No real-time EV telemetry
- No authentication or backend services
- No separate machine learning model in version one

## Success Criteria
- App launches locally with one command
- Team members can reproduce setup from the README
- Dataset stage clearly changes shown range across speed, mode, and traffic
- Fuzzy logic clearly changes the final range across pleasant versus harsh UAE temperature and AC scenarios
- Documentation is detailed enough for group collaboration and presentation prep
