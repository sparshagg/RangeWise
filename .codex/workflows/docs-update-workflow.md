# Docs Update Workflow

1. Identify which behavior or setup detail changed.
2. Update the README first if the change affects teammates.
3. Update the related `docs/` page.
4. Run `python3 scripts/sync_project_docs.py` if repository facts changed.
5. Update the project checklist.
6. Verify the docs still match commands, paths, and expected outputs.
