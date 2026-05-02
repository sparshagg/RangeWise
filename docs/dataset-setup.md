# Dataset Setup

## Source
- Kaggle dataset: <https://www.kaggle.com/datasets/ziya07/ev-energy-consumption-dataset>
- Referenced for academic use in this repository

## Expected File Path

```text
data/raw/EV_Energy_Consumption_Dataset.csv
```

## Generated Processed File Path

```text
data/processed/EV_Range_Model_Processed.csv
```

## Current Repository State
- The raw Kaggle CSV is committed to the repository.
- The processed dataset CSV is generated and committed in `data/processed/`.
- The loader is aligned with the real file name and the real column names in the dataset.
- Future preprocessing outputs should live outside `data/raw/`.

## File Purpose
The dataset supports:
- exploratory analysis
- summary statistics for the dashboard
- sanity checks for the fuzzy-input ranges
- a processed preview table that shows exactly how the raw CSV was transformed
- grouped efficiency lookup for `Shown Range`
- optional ANFIS training for the hybrid comparison path
- documentation of why certain rules matter in the UAE context

## Expected Signal Areas
- driving parameters such as speed, acceleration, and driving mode
- road and traffic conditions
- weather variables such as temperature and wind
- vehicle state such as battery level and battery temperature
- target energy consumption values

## Notes
- The current app runs without retraining, but the optional ANFIS weights can be refreshed locally.
- If the CSV is missing, the app still runs and explains how to add it.
- Keep the original raw file unchanged and place cleaned derivatives in `data/processed/`.
- Regenerate the processed CSV with `python3 scripts/build_processed_dataset.py` when preprocessing logic changes.
- Refresh the hybrid weights with `python3 scripts/train_anfis.py` when the ANFIS model needs retraining.
