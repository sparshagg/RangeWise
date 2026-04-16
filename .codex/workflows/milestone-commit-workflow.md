# Milestone Commit Workflow

## When To Commit
Commit after a complete and verified milestone such as:
- repository bootstrap
- fuzzy engine added
- dashboard completed
- docs and tests aligned

## Commit Steps
1. Update `.codex/plans/project-checklist.md`.
2. Run the relevant verification commands.
3. Review the changed files.
4. Run `./scripts/commit_milestone.sh "type: message"`.
5. Confirm the commit and push completed cleanly.

## Commit Message Style
- `chore: bootstrap project repository`
- `feat: add fuzzy range prediction engine`
- `feat: build streamlit dashboard`
- `docs: add team workflow and setup guides`
- `test: cover range adjustment behavior`

## Terminal Rule
Milestone commits should be triggered from the terminal only after the current work is coherent and verified.
