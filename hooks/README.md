# Hooks Governance Layer

This directory contains deterministic, code-level execution gates that operate **before** the Orchestrator LLM can invoke any tools or execute actions.

## Implementation Notes

Currently the `hook` is only triggered for the `PreToolUse` hook and was setup into different options, this means that you can keep wath yopu consider as the best for your AI work methodology (as tiers):
- **Tier 1 Agent Setting**: The hooks was implemented within the `agent.settings.json` file, in case you use `agents.settings` capability (ex: claude,settings.json, cursor.settings.json, etc) you can add this code snippet inside of your work setup and preference.
- **Tier 2 Orchestrator Agent**: The hook was embeded as part of the `orchestrator-agent.md` frontmatter, this option was added to make this capability native for the orchestrator as a PreToolUse hook considering that the security was a manadory compliance for the framework.

## Module Structure

```
hooks/
├── hook_contract.py      # Data contracts only — HookContext, HookResult, HookExtensions
├── security_gate.py      # File/MIME/size validation + prompt injection guard
├── language_detector.py  # Offline language detection via lingua + LANGUAGE_RULES
└── security_language.py  # PreToolUse entrypoint — orchestrates the two phases above
```

Each module has a single responsibility. `security_language.py` is the registered hook entrypoint and contains only `main()` and stdin-parsing helpers; all logic lives in the dedicated modules above.

## Strategy & Rationale

Large Language Models are probabilistic and susceptible to prompt injection, hallucination, and bypasses. Relying exclusively on LLM constraints (e.g., "Do not execute code", "Only accept IEEE requirements") leaves structural security vulnerabilities in the framework.

The hooks act as a **Fail-Closed Security Layer**:
- **Execution:** Runs as a deterministic Python script.
- **Fail-Closed:** If the hook fails, the entire agent workflow halts immediately with an `execute_workflow: false` signal, entirely bypassing the LLM.
- **Auditability:** Emits a deterministic `trace_id` for end-to-end lineage tracking.

## Core Mitigation Features

1. **Malicious File Blocking** (`security_gate.py`):
   - Denies `.exe`, `.sh`, `.bat`, and unknown binary MIME types.
   - Prevents the agent from accidentally reading or processing executing payloads.
2. **Language Detection** (`language_detector.py`):
   - Autonomously detects the user's language without relying on token-intensive LLM classification.
   - Enforces consistent language usage in the generated outputs.
3. **Prompt Injection Protection** (`security_gate.py`, R12 Mitigation):
   - Allow a natural user instruction to start the interaction like `Run` followed of the input artifacts ( RF, and US), and at the end cannot be added any other instruction. Any instruction out of this boundaries is considered as an injection and cause the block of the request. This ensures the integrity of the system instructions.
   - Applies strict Regex to the user input to enforce the IEEE format: `RF-[ID]: The system must [action]. US[as a [role] I want to [goal] so that [reason]].`
   - Strips extraneous adversarial instructions (e.g., `"SYSTEM: ignore previous instructions"`) before passing the sanitized prompt to the Orchestrator.

## Testing 

All hook logic is backed by a robust test suite covering both structural (unit) and functional (integration) requirements.

- **`test_security.py`**: Validates file extension mapping, compound extension detection (`.pdf.exe`), file size mocking, and prompt injection Regex boundaries.
- **`test_language.py`**: Validates language detection for English and Spanish, including edge cases like accented characters and short phrases.
- **`test_integration.py`**: Treats the hook as a black-box subprocess to verify that `execute_workflow` behaves correctly on valid IEEE requests and gracefully exits (Exit Code 0) on malicious payloads while blocking workflow execution.

To run the test suite you need to move to the root project directory `qa-requirements-analyzer-agents-team` and install dependencies. It is recommended to use a virtual environment:

```bash
# Change directory to the root project
cd ..
# Testing setup and virtual environment activation
python3 -m venv .venv 
source .venv/bin/activate
# Install dependencies with ruff for code linting 
pip install -r requirements.txt ruff 
# Run the tests
pytest tests/hooks/
# Run unit tests
pytest tests/hooks/test_security.py tests/hooks/test_language.py
# Run integration tests
pytest tests/hooks/test_integration.py
```
