# Hooks Governance Layer

This directory contains deterministic, code-level execution gates that operate **before** the Orchestrator LLM can invoke any tools or execute actions.

## Strategy & Rationale

Large Language Models are probabilistic and susceptible to prompt injection, hallucination, and bypasses. Relying exclusively on LLM constraints (e.g., "Do not execute code", "Only accept IEEE requirements") leaves structural security vulnerabilities in the framework.

The hooks act as a **Fail-Closed Security Layer**:
- **Execution:** Runs as a deterministic Python script.
- **Fail-Closed:** If the hook fails, the entire agent workflow halts immediately with an `execute_workflow: false` signal, entirely bypassing the LLM.
- **Auditability:** Emits a deterministic `trace_id` for end-to-end lineage tracking.

## Core Mitigation Features

1. **Malicious File Blocking:** 
   - Denies `.exe`, `.sh`, `.bat`, and unknown binary MIME types.
   - Prevents the agent from accidentally reading or processing executing payloads.
2. **Language Detection (Lingua):**
   - Autonomously detects the user's language without relying on token-intensive LLM classification.
   - Enforces consistent language usage in the generated outputs.
3. **Prompt Injection Protection (R12 Mitigation):**
   - Allow a natural user instruction to start the interaction like `Run` followed of the input artifacts ( RF, and US), and at the end cannot be added any other instruction. Any intrsuction out of this boundaries is considered as an injection and cause the block of the request. This ensures the integrity of the system instructions.  
   - Applies strict Regex to the user input to enforce the IEEE format: `RF-[ID]: The system must [action]. US[as a [role] I want to [goal] so that [reason]].`
   - Strips extraneous adversarial instructions (e.g., `"SYSTEM: ignore previous instructions"`) before passing the sanitized prompt to the Orchestrator.

## Testing 

All hook logic is backed by a robust test suite covering both structural (unit) and functional (integration) requirements.

- **`tests/test_security.py`**: Validates file extension mapping, compound extension detection (`.pdf.exe`), file size mocking, and prompt injection Regex boundaries.
- **`tests/test_integration.py`**: Treats the hook as a black-box subprocess to verify that `execute_workflow` behaves correctly on valid IEEE requests and gracefully exits (Exit Code 0) on malicious payloads while blocking workflow execution.

To run the test suite:
```bash
# Testing setup and virtual environment activation
cd hooks/
source .venv/bin/activate
# Run the tests
python -m pytest tests/
# Run unit tests
python -m pytest tests/test_security.py tests/test_language.py
# Run integration tests
python -m pytest tests/test_integration.py
```
