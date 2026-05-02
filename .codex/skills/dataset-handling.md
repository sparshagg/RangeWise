# Dataset Handling Skill

## Rules
- Keep the raw Kaggle CSV committed at `data/raw/EV_Energy_Consumption_Dataset.csv`.
- Generate the processed artifact at `data/processed/EV_Range_Model_Processed.csv` with `scripts/build_processed_dataset.py`.
- Use the processed dataset to show derived fields and lookup-bucket logic during demos.
- Keep dataset-backed `Shown Range` logic separate from fuzzy and ANFIS correction logic.
- When preprocessing rules change, regenerate the processed CSV and update docs that describe the pipeline.
