# Changelog

All notable changes to this project are documented in this file.

## [1.2.1] - 2026-09-21

### Features
- Added `AGENT.md` root system manifest and discovery registry implementing `agent-protocol-v1` compliance for multi-agent discovery and execution across CLI harnesses (Claude Code, Antigravity, Wrappy, Cursor, GitHub Copilot, Open Code) and IDE extensions (Cursor IDE, Antigravity IDE, VS Code, Windsurf, Devin, Codex).
- Defined centralized agent capability index mapping the primary entry point (`orchestrator-agent`) 
- Formalized the 4-phase Discovery & Execution Protocol (Bootstrap, Intent Matching, Delegation, Consolidation) with strict orchestration routing, state management, and isolation constraints.

### Updates
- Not applicable.   

### Patches
- Not applicable.

## [1.1.2] - 2026-09-17

### Features
- Added BDD discovery technique selection framework (`Gotcha: Choosing the BDD Discovery Technique`) in `requirements_analysis_techniques.md` to systematically select between Impact Mapping, Story Mapping, Example Mapping, or Combined approaches.
- Added strict Gherkin behavioral rules in `behavioral-translation` skill, enforcing domain-level abstractions, state-over-navigation principles, single-purpose scenarios, step length limits, and clear separation of quality concerns.
- Added scenarios descriptions anti-pattern and extended auto-validation checklist in `behavioral-translation` skill.
- Added security guardrails in `orchestrator-agent.md`, establishing proactive Zero Trust workflow protection, data context anti-leakage constraints, and system prompt/manifesto confidentiality.

### Updates
- Updated MoSCoW self-verification criteria in `behavioral-translation` skill to explicitly forbid infrastructure terminology leakage and UI/automation mechanics.

### Patches
- Not applicable.

## [1.0.2] - 2026-09-04

### Features
- Added synthetic triggers (Triggers 3 to 8) to evaluate agent orchestration across high-complexity scenarios: concurrency (`RF-INV-004`), overselling prevention (`FR-INV-003`), authorization (`NFR-INV-005`), idempotence (`FR-INV-008`), and atomicity/rollback (`NFR-INV-002`).
- Expanded risk evaluation scope to calibrate agentic responses against Medium, High, and Critical impact criteria (transactional integrity, OWASP security, and financial risk).

### Updates
- Updated `project_context_manifesto.md` with detailed architectural interactions across FastAPI microservices, Redis distributed locking, and PostgreSQL transactional consistency for flash sales.
- Improved `data-test-poc.md` with step-by-step CLI/IDE agent execution instructions and standardized copy-paste trigger formats for orchestrator sessions.

### Patches
- Not applicable.

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
- Added subagent skills and RAG components `agents/`
- Added subagent artifact validation contracts in assets
- Added risk log feature for risk tracking and pattern detection across iterations.
- Added a pre-tool-use hook as a mechanism to validate and process inputs as a security and language gate before triggering the workflow

### Updates
- Initial release.

### Patches
- Not applicable.
