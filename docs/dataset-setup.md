# Dataset Setup

## Source
- Kaggle dataset: <https://www.kaggle.com/datasets/ziya07/ev-energy-consumption-dataset>
- Referenced for academic use in this repository

## Expected File Path

```text
data/raw/EV_Energy_Consumption_Dataset.csv
```

## Current Repository State
- The raw Kaggle CSV is committed to the repository.
- The loader is aligned with the real file name and the real column names in the dataset.
- Future preprocessing outputs should live outside `data/raw/`.

## File Purpose
The dataset supports:
- exploratory analysis
- summary statistics for the dashboard
- sanity checks for the fuzzy-input ranges
- documentation of why certain rules matter in the UAE context

## Expected Signal Areas
- driving parameters such as speed, acceleration, and driving mode
- road and traffic conditions
- weather variables such as temperature and wind
- vehicle state such as battery level and battery temperature
- target energy consumption values

## Notes
- The current app does not require model training.
- If the CSV is missing, the app still runs and explains how to add it.
- Keep the original raw file unchanged and place any future cleaned derivatives in a separate folder if needed.
