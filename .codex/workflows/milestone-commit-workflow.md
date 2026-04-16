# Milestone Commit Workflow

## When To Commit
Commit after a complete and verified milestone such as:
- repository bootstrap
- fuzzy engine added
- dashboard completed
- docs and tests aligned

## Commit Steps
1. Update `.codex/plans/project-checklist.md`.
2. Run `python3 scripts/sync_project_docs.py`.
3. Run the relevant verification commands.
4. Review the changed files.
5. Commit with a concise milestone message.

## Commit Message Style
- `chore: bootstrap project repository`
- `feat: add fuzzy range prediction engine`
- `feat: build streamlit dashboard`
- `docs: add team workflow and setup guides`
- `test: cover range adjustment behavior`

## Automation Rule
Automatic commits are allowed only for coherent, verified milestones and should push to `origin/main` after a successful commit.
