# Bootstrap Workflow

## Goal
Bring a fresh clone into the expected local working state.

## Steps
1. Create and activate a local virtual environment.
2. Install dependencies from `requirements.txt`.
3. Run `git config core.hooksPath .githooks`.
4. Confirm the raw dataset exists at `data/raw/EV_Energy_Consumption_Dataset.csv`.
5. Generate the processed dataset with `python3 scripts/build_processed_dataset.py`.
6. Run `python3 scripts/sync_project_docs.py`.
7. Run local verification with `python3 -m pytest` or `.venv/bin/python -m pytest`.
