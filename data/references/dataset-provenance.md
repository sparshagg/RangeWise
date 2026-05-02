# Dataset Provenance

- Dataset name: `EV Energy Consumption Dataset`
- Source URL: <https://www.kaggle.com/datasets/ziya07/ev-energy-consumption-dataset>
- Source owner: `ziya07` on Kaggle
- Referenced on: `2026-04-16`
- Intended use in this repository: academic coursework and local demonstration

## Repository Note
The application expects the raw dataset file at:

```text
data/raw/EV_Energy_Consumption_Dataset.csv
```

The raw CSV is committed to this repository under that path.

The same dataset is used for:
- processed preview generation in `data/processed/EV_Range_Model_Processed.csv`
- grouped efficiency lookup for `Shown Range`
- optional ANFIS training for the hybrid neuro-fuzzy comparison
