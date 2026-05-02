# Milestone Commit Workflow

## When To Commit
Commit after a complete and verified milestone such as:
- repository bootstrap
- dataset-backed shown-range update
- fuzzy-model correction
- hybrid ANFIS integration cleanup
- dashboard/docs alignment

## Commit Steps
1. Update `.codex/plans/project-checklist.md`.
2. Run the relevant verification commands.
3. Review the changed files.
4. Run `./scripts/commit_milestone.sh "type: message"`.
5. Confirm the commit and push completed cleanly.

## Commit Message Style
- `chore: restore repo operating files`
- `feat: add dataset-backed shown range`
- `feat: add hybrid neuro-fuzzy comparison`
- `docs: align repository guidance with merged hybrid model`
- `test: cover hybrid range behavior`

## Terminal Rule
Milestone commits should be triggered from the terminal only after the current work is coherent and verified.
