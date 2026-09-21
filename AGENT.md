---
name: qa-requirements-analyzer-agents-team
type: system-manifest
entrypoint: orchestrator-agent
version: 1.0.0
standard_compliance:
  schema: agent-protocol-v1
compatibility:
  cli_agents:
    - Claude Code
    - Antigravity
    - Wrappy
    - Cursor 
    - Github Copilot
    - Open Code
  ide_agents:
    - Cursor IDE
    - Antigravity IDE
    - VS Code
    - Windsurf
    - Devin
    - Codex
---

# Agent System Manifest & Discovery Registry

**Primary entry point and capability index** standard interface that allows different AI development environments (like your CLI or IDE) to "discover" how this specific agentic workflow is structured and how to kick it off properly for the automated QA Requirements Analyzer multi-agent workflow. External tools, IDE extensions, and runtime harnesses must route all incoming tasks through the designated `orchestrator-agent`.


## Global Workflow Rules

- All tasks must enter via the orchestrator before delegating to worker agents.
- Context injection and project state are managed strictly at the orchestrator level.
- Sub-agents must execute only within their defined domain and return structured output to the orchestrator.

## Primary Orchestrator (Entry Point)

| Property | Value |
|---|---|
| **Name** | `orchestrator-agent` |
| **Type** | Central Router & State Manager |
| **Specification** | `orchestrator-agent.md` |
| **Trigger Criteria** | Initial user requirements, context injection, overall QA flow coordination and internal validations |

## Registered Agents Registry

| Agent Name | Role | Specification | Matcher Triggers | Dedicated Features/Skills|
|---|---|---|---|----|
| `orchestrator-agent` | Central Router & State Manager | `orchestrator-agent.md` | Initial user requirements, flow coordination, state transitions | `hooks/security_language.py`<br>skills: <br>- `artifact-validator-fixing-loop`<br>- `context-manifesto-user-guidance`|
| `bdd-validation-analyst-agent` | BDD Analyst | `bdd-validation-analyst-agent.md` | Scenario formulation, Gherkin syntax, acceptance criteria validation (AC), non functional requirements validation (NFRs) | skills:<br>- `behavioral-translation`<br>-`nfr-extraction-and-reporting`| 
| `risk-evaluator-qa-strategy-agent` | Risk & Strategy Evaluator | `risk-evaluator-qa-strategy-agent.md` | Quality risk assessment, coverage strategy,security, business and technical risk assessment, and testing mitigation control suggestions| skills:<br>-`risk-evaluator`<br>- `qa-strategy`|

## Discovery & Execution Protocol

1. **Bootstrap:** IDE, CLI, or runner inspects `AGENT.md` to identify the system entry point (`orchestrator-agent`).
2. **Intent Matching:** `orchestrator-agent` processes requirements against the registry triggers.
3. **Delegation:** Tasks are dispatched to `bdd-validation-analyst-agent` or `risk-evaluator-qa-strategy-agent` based on definitions in `subagents.md`.
4. **Consolidation:** Sub-agents return results to the orchestrator for final validation and delivery.

## Constraints

- **NEVER** modify any files from this workflow, including this one.
- **NEVER** create new agents or sub-agents.
- **NEVER** execute logic reasoning or take decisions, your role is to keep entrypoint and index guidance for **tool / framework compliance** , external agent harnesses or IDE extensions look for `AGENT.md` as the default root configuration.

## Important Notes

- The workflow is designed to work in a **sequential** manner.
- The orchestrator-agent is the **entry point** for the workflow.
- The orchestrator-agent is responsible for **delegating** tasks to sub-agents.