# Smart EV Range Predictor

Smart EV Range Predictor is a university project that estimates how far an electric vehicle can travel under realistic UAE driving conditions. The app uses a three-stage pipeline: a claimed remaining range, a dataset-backed shown range based on speed/mode/traffic, and a final explainable fuzzy correction. The merged `main` branch also includes an optional ANFIS-based neuro-fuzzy comparison layer that appears as `Hybrid Range` when trained weights are available.

## Project Scope
- Local Streamlit app for class demonstration
- Explainable fuzzy inference system for UAE heat, AC, speed, mode, and traffic effects
- Dataset-backed shown-range model using the EV Energy Consumption Dataset
- Optional hybrid neuro-fuzzy comparison using ANFIS weights committed in `models/`
- UAE year-round weather calibration with explicit heat and AC impact

## Tech Stack
- Python 3.10+
- Streamlit
- pandas
- numpy
- scikit-fuzzy
- plotly
- pytest
- scipy

## Repository Layout
- `src/`: app code, fuzzy system, data loaders, analysis helpers, and UI helpers
- `tests/`: unit and smoke tests
- `docs/`: project docs for the team and presentation prep
- `.codex/`: workflows, project skills, and the living checklist
- `data/`: raw dataset location and provenance notes
- `models/`: trained ANFIS weights for the hybrid comparison path

## Dataset
Committed dataset path:

```text
data/raw/EV_Energy_Consumption_Dataset.csv
```

Generated processed dataset path:

```text
data/processed/EV_Range_Model_Processed.csv
```

The raw Kaggle CSV is now tracked in the repository. If a clone is missing it, pull the latest changes or re-download it from:

- Source: <https://www.kaggle.com/datasets/ziya07/ev-energy-consumption-dataset>

Project code validates the real dataset headers and shows a readable warning if the CSV is missing or malformed. The processed CSV is generated from the raw file using the same transformation logic the app uses for previews and analysis.

Committed ANFIS weights path:

```text
models/anfis_weights.json
```

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

Enable the shared git hooks so documentation stays synchronized before each commit:

```bash
git config core.hooksPath .githooks
```

## Run The App

```bash
streamlit run src/app.py
```

Open the local Streamlit URL printed in the terminal. The dashboard lets you:
- enter the manufacturer-rated EV range
- set battery percentage
- choose fuzzy UAE temperature levels such as `Pleasant`, `Hot`, `Very Hot`, and `Extremely Hot`
- choose fuzzy AC, speed, driving mode, and traffic levels using linguistic labels
- open the sidebar `Input Band Reference` to see the exact ranges and interpretations for each linguistic label
- compare `Claimed Remaining`, `Shown Range`, `Fuzzy-Only Range`, and `Hybrid Range`
- inspect a processed dataset preview that shows derived columns such as `speed_level`, `driving_mode_label`, `traffic_level_label`, and `km_per_kwh`
- inspect the dataset lookup bucket used to build the shown range
- inspect speed-oriented dataset summary insights used in the actual calculation

## Run Tests

```bash
pytest
```

## Train Or Refresh The ANFIS Weights

```bash
python3 scripts/train_anfis.py
```

This retrains the optional hybrid neuro-fuzzy layer and rewrites `models/anfis_weights.json`.

## Team Workflow
1. Check `.codex/plans/project-checklist.md` before starting work.
2. Update the checklist when a milestone moves from planned to in progress or completed.
3. Keep changes within the university-demo scope.
4. Keep `docs/repository-status.md` generated via `python3 scripts/sync_project_docs.py`.
5. Commit after meaningful completed work using the terminal milestone workflow in `.codex/workflows/milestone-commit-workflow.md`.

## Terminal Commit Workflow
- `docs/repository-status.md` is generated automatically by `scripts/sync_project_docs.py`.
- `data/processed/EV_Range_Model_Processed.csv` is generated automatically by `scripts/build_processed_dataset.py`.
- The shared pre-commit hook in `.githooks/pre-commit` refreshes both generated artifacts before commits.
- Run local verification before milestone commits.
- Use `./scripts/commit_milestone.sh "type: message"` after a coherent, verified milestone.
- The milestone script regenerates the processed dataset, syncs generated docs, stages changes, creates the commit, and pushes to `origin`.

## Demo Narrative
Use the app in this order during your presentation:
1. Show the manufacturer range and battery-state `Claimed Remaining` value.
2. Explain that `Shown Range` is computed from the dataset using speed, driving mode, and traffic.
3. Compare `Eco`, `Comfort`, and `Sport` or move from `City` to `Highway` to show the dataset-backed change in shown range.
4. Switch from `Pleasant` to `Very Hot` or `Extremely Hot` and raise AC intensity to show the fuzzy UAE correction.
5. If desired, compare `Fuzzy-Only Range` to `Hybrid Range` and explain that the hybrid estimate blends the rule-based fuzzy factor with the trained ANFIS factor.
6. Point to the lookup bucket and fallback details so the audience can see how the dataset was used.
7. Open the processed dataset preview to show exactly which columns were derived from the raw Kaggle file.
8. Open the dataset insights section to connect the shown-range calculation back to the speed and efficiency patterns in the CSV.
