# Changelog

All notable changes to this project are documented in this file.

## [1.0.1] - 2026-09-02

### Features
- Not applicable.

### Updates
- Added `README.md` documentation in `outputs/` and `artifacts/` directories detailing folder purposes, deliverables, and user guidance.

### Patches
- Added `.gitignore` placeholder files to track empty output and artifact directory structures in remote Git repositories.

## [1.0.0] - 2026-09-01

### Features
- Added requirements analysis `orchestrator-agent`.
- Added `bdd-validation-analyst-agent`.
- Added `risk-evaluator-qa-strategy-agent`.
- Added security and language pre-processing gate `hooks/security_language.py`.
- Added orchestrator skills `skills/`
- Added subagents skills and RAG components `agents/`
- Added subagents artifacts validation contracts in assets
- Added risk log feature for risk tracking and patterns detection across iterations.
- Added pre-tool use hook as a mechanism to validate and process inputs as a security and language gate before trigger workflow

### Updates
- Initial release.

### Patches
- Not applicable.
