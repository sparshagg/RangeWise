# Project Plan

## Goal
Build a local Streamlit dashboard that demonstrates how fuzzy logic can produce a more realistic EV range estimate than a naive battery-percentage calculation.

## Deliverable
- One working local app
- One explainable fuzzy model tuned for UAE conditions
- One dataset-backed analysis section
- One team-friendly README
- One living checklist for progress tracking
- One generated repository-status doc kept fresh by hook and CI

## Core Design
- Baseline remaining range = `manufacturer rated range x battery percentage`
- Fuzzy adjustment factor responds to:
  - ambient temperature
  - AC intensity
  - driving style
  - traffic level
- Final adjusted range = `baseline remaining range x fuzzy adjustment factor`

## Scope Boundaries
- No cloud deployment
- No real-time EV telemetry
- No authentication or backend services
- No separate machine learning model in version one

## Success Criteria
- App launches locally with one command
- Team members can reproduce setup from the README
- Fuzzy logic clearly penalizes hot, AC-heavy, aggressive, high-traffic scenarios
- Documentation is detailed enough for group collaboration and presentation prep
