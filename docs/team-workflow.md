# Team Workflow

## Working Style
- Keep the project local-first and classroom-scoped.
- Update the checklist before and after each milestone.
- Prefer small, complete milestones over large unfinished branches.
- Keep generated docs synchronized before commits.

## Suggested Milestones
1. Repository scaffold and documentation
2. Data loading and dataset validation
3. Fuzzy inference system
4. Streamlit dashboard
5. Tests and local verification
6. Presentation polish

## Checklist Discipline
- Move work into `In Progress` before implementation.
- Move work into `Completed` only after verification.
- Keep optional ideas in `Possible Later` so scope does not drift.

## Docs Freshness
- Run `git config core.hooksPath .githooks` once per clone.
- The pre-commit hook regenerates `docs/repository-status.md`.
- Run `python3 scripts/sync_project_docs.py` locally when repo facts change.
- Manual doc updates should still be made when behavior, setup, or workflow changes.

## Commit Style
Use messages such as:
- `chore: bootstrap project repository`
- `feat: add fuzzy inference engine`
- `feat: build streamlit dashboard`
- `docs: expand setup and project workflow`
- `test: cover fuzzy range behavior`

## Branch Guidance
- For solo implementation, working directly on the main branch is acceptable.
- If teammates contribute code later, use short-lived topic branches and merge only complete milestones.

## Terminal Milestone Commits
- Commits should happen only after a coherent, noticeable milestone.
- Run `./scripts/commit_milestone.sh "type: message"` from the terminal after verification.
- The script syncs generated docs, stages the repo, creates the commit, and pushes to `origin`.
- Partial, broken, or purely transient changes should be skipped.
