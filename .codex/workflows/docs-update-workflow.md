# Docs Update Workflow

## Trigger
Run this when setup, model behavior, workflow, or repository facts change.

## Steps
1. Update the relevant Markdown pages manually.
2. Regenerate the processed dataset if preprocessing changed.
3. Run `python3 scripts/sync_project_docs.py`.
4. Review `docs/repository-status.md` as generated output only.
5. Stage both manual and generated doc changes together.
