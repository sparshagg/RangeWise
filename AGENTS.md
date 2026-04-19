# AGENTS

## Purpose
- Build and maintain the Smart EV Range Predictor as a university project focused on fuzzy logic under UAE driving conditions.
- Prefer explainability, clean demos, and strong documentation over advanced production features.

## Working Rules
- Start substantial tasks with a short plan or checklist update before coding.
- Keep `.codex/plans/project-checklist.md` current before and after each milestone.
- Do not expand scope beyond the agreed classroom demo without explicit approval.
- Use milestone-sized commits with clear messages after meaningful completed changes.
- Do not rely on scheduled automations for commits; use terminal-driven milestone commits instead.
- Keep docs aligned with code; run `python3 scripts/sync_project_docs.py` whenever repo facts change.
- Treat `docs/repository-status.md` as generated output and do not hand-edit it.
- Keep the local git hook path pointed at `.githooks` so doc sync runs before commits.
- Keep verification local; do not depend on GitHub Actions for routine project checks.

## Project Constraints
- Local-first Streamlit app only.
- Fuzzy logic is the primary intelligence layer.
- Dataset analysis supports the demo; it is not a separate ML pipeline.
- Model behavior should remain presentation-friendly and easy to justify in class.
