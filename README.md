# Smart EV Range Predictor

Smart EV Range Predictor is a university project that estimates how far an electric vehicle can travel under realistic UAE driving conditions. Instead of relying on a simple battery-percentage calculation, the app combines battery state with a fuzzy logic adjustment layer that reacts to ambient heat, AC intensity, driving style, and traffic load.

## Project Scope
- Local Streamlit app for class demonstration
- Explainable fuzzy inference system
- Dataset-backed analysis using the EV Energy Consumption Dataset
- UAE year-round weather calibration with explicit heat and AC impact

## Tech Stack
- Python 3.10+
- Streamlit
- pandas
- numpy
- scikit-fuzzy
- plotly
- pytest

## Repository Layout
- `src/`: app code, fuzzy system, data loaders, analysis helpers, and UI helpers
- `tests/`: unit and smoke tests
- `docs/`: project docs for the team and presentation prep
- `.codex/`: workflows, project skills, and the living checklist
- `data/`: raw dataset location and provenance notes

## Dataset
Expected dataset path:

```text
data/raw/ev_energy_consumption_dataset.csv
```

If the CSV is not already present in your clone, download it from Kaggle and place it at that path:

- Source: <https://www.kaggle.com/datasets/ziya07/ev-energy-consumption-dataset>

Project code automatically validates the dataset columns and shows a readable setup warning if the CSV is missing.

## Setup
Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run The App

```bash
streamlit run src/app.py
```

Open the local Streamlit URL printed in the terminal. The dashboard lets you:
- enter the manufacturer-rated EV range
- set battery percentage
- model UAE temperature conditions
- adjust AC intensity, driving style, and traffic
- compare nominal range against fuzzy-adjusted range
- inspect dataset summary insights

## Run Tests

```bash
pytest
```

## Team Workflow
1. Check `.codex/plans/project-checklist.md` before starting work.
2. Update the checklist when a milestone moves from planned to in progress or completed.
3. Keep changes within the university-demo scope.
4. Commit after meaningful completed work using the milestone workflow in `.codex/workflows/milestone-commit-workflow.md`.

## Demo Narrative
Use the app in this order during your presentation:
1. Show the manufacturer range and battery-state baseline.
2. Change the temperature to a hot UAE scenario and raise AC intensity.
3. Increase driving aggressiveness and traffic to demonstrate a sharper range drop.
4. Open the dataset insights section to connect the fuzzy logic design back to the data source.

