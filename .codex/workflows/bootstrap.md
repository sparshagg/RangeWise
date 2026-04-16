# Bootstrap Workflow

1. Review `AGENTS.md` and `.codex/plans/project-checklist.md`.
2. Confirm the project remains inside the university demo scope.
3. Set up the Python virtual environment.
4. Install dependencies from `requirements.txt`.
5. Run `git config core.hooksPath .githooks`.
6. Verify the dataset path under `data/raw/`.
7. Run `python3 scripts/sync_project_docs.py`.
8. Run `pytest`.
9. Run `streamlit run src/app.py`.
