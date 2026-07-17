# Quick link Reference  

This files contains detailed technical information about the framework design and implementation.

- [Principles and Philosophy](#principles-and-philosophy)
- [Fixing Loop Strategy](#fixing-loop-strategy)
- [Hook Layer](#hook-layer)
- [Solutions Identified Risks](#solutions-identified-risks)
- [Roadmap](#roadmap)

---
## Principles and Philosophy

| Principle | Description |
| --- | --- |
| **AI EngineeringOps** | The framework applies AI-driven orchestration while embedding software engineering and quality assurance standards into each analysis stage. Every subagent performs its evaluation using recognized industry references and deterministic validation rules rather than relying solely on free-form generative reasoning. |
| **Quality-First, Shift-Left** | The framework's philosophy is to improve the quality of requirements early in the development lifecycle, before code is written. This is known as **Shift-Left** quality. By identifying and addressing issues early, teams can reduce the cost of quality and improve the overall quality of the software. |
|**Human remains accountable**| Although AI agents automate many analysis tasks, the framework preserves human oversight and decision-making authority. The framework supports, but does not replace, human judgment in requirement approval, prioritization, and quality-related trade-offs.<br> The framework does not replace the QA professional, Product Owner, or Business Analyst. The final responsibility for requirements approval, prioritization, and quality decisions remains with the human team.|
|**Best Industry Practices and Standards-based**| The framework embeds recognized software engineering and quality assurance standards into each analysis stage. Each subagent performs its evaluation using deterministic validation rules and established industry references rather than relying solely on free-form generative reasoning.<br>The following references are embedded in the framework:<br>- ISTQB Foundation Level syllabus<br>- IEEE Std 830-1998 and IEEE 29119 standards<br>- OWASP Top 10 security principles<br>- Risk-Based Testing principles<br>- Behavior-Driven Development (BDD) practices<br>- User Story Analysis best practices|
|**Context First**|Currently the framework uses a specific file located at `./project_context_manifesto.md` to provide context to the sub-agents, but this is an agnostic solution, the real project context should be provided in a standardized file to ensure consistency and quality of the analysis. For that reason in case of absence of this context file, the orchestrator-agent will trigger the `context-manifesto-user-guidance` skill to guide the user in the creation of the file in case of absence.||
|**Resource Consumption Control and Optimization**|The framework is designed to minimize resource consumption and costs. That's why the refinement requirement process is decomposed into sub-agents. These agents have separated responsibilities, reasoning parameters, and needed context as persistence memory. It also includes a resource consumption control section as a metric to monitor the resource consumption and costs each time a refinement runtime is executed.|
|**Cross-Platform Compatibility**| The framework is designed to be compatible with various AI agent platforms, including CLI agents (Clude, Antigravity, Wrappy) and IDE Agents (Cursor IDE, ANTIGRAVITY IDE, VsCode, Windsurf, etc). |
|**Cross-Model AI Compatibility**| The framework is designed to be compatible with various AI models, including Claude, GPT, Llama, Mistral, and Gemini. This flexibility allows the framework to be used with different models depending on the user's preference and availability.|
|**Language Agnostic**| The framework is designed to be used with different languages, including English, Spanish, French, German, and Italian. This flexibility allows the framework to be used with different languages depending on the user's preference and availability. Althout the framework use English as processing language, to reduce token consumption, and fallows internationalization standards, it can generate the deliverables in the language of the user request.|

>[Back to Top](#quick-link-reference)
---

## Fixing Loop Strategy

The Fixing Loop is an iterative correction mechanism triggered by the Orchestrator whenever any of the validation layers fail. 
- It evaluates the nature of the failure (e.g., missing artifacts, incomplete risk analysis, schema non-compliance).
- It requests the responsible sub-agent to correct its output, providing explicit feedback on what failed.
- It is constrained by 2 maximum retry limits to prevent infinite loops and excess resource consumption, eventually falling back to a structured failure report if the issue cannot be automatically resolved.

**Failures Clasification strategy**
- The failures are classified and this determine the fixing loop strategy, for example:

  - **Minimal**: If the failures are minimal change such as typos or cosmetic errors, the fixing loop could not be triggered or the change will be requested to the specific sub-agent only if this is required.
  - **Major**: If the failures are only in the second sub-agent the fixing loop will, be triggered only for that agents, but if the failures were in the first sub-agent, the fixing loop will be triggered for the entire workflow, considering the subagents outputs as inputs to the next subagents, this are the risk of the secuencial designe and the dependency between subagents.
  - **Major Internals**: If the failures are detected by sub-agents in the handoff validation rules, the fixing loop will be triggered only for that sub-agent an only once  time, and the failure will be logged in the quality report.
  - **Critical**: If the failures are critical, the fixing loop will be triggered to correct the failures.

  **Failure Report**
  - The `artifacts/validation-report/` sub folder will contain the artifacts validation report of the runtime executed, this will keep auditable and trazability to agents and outputs, including the number of fixing loops triggered.
  - The `artifacts/logs/` sub folder will containg the runtine logs in case the fixing loop will excced the max number of retries.
 and the fix will be done by the user manually or need external responsabilities. 

>[Back to Top](#quick-link-reference)
---

## Hook Layer

The framework includes a **deterministic pre-tool hook** that executes before any file is read or any tool is invoked by the orchestrator. This moves critical governance logic out of the LLM's probabilistic reasoning and into auditable Python code.

> Registered in `agent.settings.json`. Triggers automatically on: `Bash`, `Read`, `Cat`, `Write`, `Edit`.

### Hook Contract

**Stable Hook Interface Contract**

Single source of truth for the interface between any hook and any orchestrator.
This file defines ONLY data structures, no logic, no side-effects.

The Hook Contract is a JSON schema that defines the data structures that:
- The orchestrator passes to the hook (HookContext)
- The hook returns to the orchestrator (HookResult)
- Optional policy overrides (HookExtensions)

#### **HookContext Structure**: 
- Input to every hook invocation
- The orchestrator builds this and passes it to every hook.

| Attribute | Type | Description |
|-----------|------|-------------|
| `user_prompt` | string | The raw text prompt submitted by the user. |
| `input_files` | list | List of file paths referenced in the request (may be empty if the user provided no files). |
| `runtime_config` | dict | Optional dict from agent.settings.json for runtime parameters (e.g. max_file_size_mb).|
| `extensions` | dict | Optional policy overrides (see HookExtensions).|

#### **HookExtensions Structure**: 
- Optional policy overrides passed from agent.settings.json at runtime.
- Optional extensions, backward-compatible additions to HookContext.
- New fields can be added here without breaking existing hook implementations.

| Attribute | Type | Description |
|-----------|------|-------------|
| `allowed_extensions` | list | Explicit allow-list that overrides the default deny-list in the hook (e.g. [".py"] to permit Python files).|
| `blocked_patterns` | list | Additional filename patterns to deny (glob-style).|

#### **HookResult structure**:
- Is the stable output structure.
- Every hook MUST return a value that matches this structure.
- The orchestrator only needs to read execute_workflow to decide whether
- to proceed; all other fields are optional enrichment.

**Mandatory fields**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `execute_workflow` |Boolean|True  → orchestrator proceeds with the workflow. False → orchestrator aborts immediately andsurfaces block_reason to the user.|
| `trace_id` |UUID4 string |linking this hook invocation to all downstream artifacts for audit traceability.|

**Optional enrichment fields** (present when execute_workflow is True): 
| Attribute | Type | Description |
|-----------|------|-------------|
| `language` |string|Detected ISO language name (e.g. "Spanish").|
| `confidence` |float|Detection confidence score [0.0 – 1.0].|
| `language_rule` |string|Fully formed instruction the orchestrator prepends to every sub-agent invocation.|
| `sanitized_context` |dict|Cleaned copy of the user prompt and file list after security scrubbing.|

**Optional block fields** (present when execute_workflow is False):|
| Attribute | Type | Description |
|-----------|------|-------------|
| `risk_level` |string|Severity of the detected threat: "low"|"medium"|"high".|
| `block_reason` |string|Human-readable explanation of why the request was denied.|
    """

>[Back to Top](#quick-link-reference)

### Hook Architecture 

```txt
User Request → PreToolUse Hook (Python) → Orchestrator Agent → Sub-agents
                      ↓
         User Request → stdin (JSON)
         HookResult JSON emitted to stdout
         execute_workflow: true  → proceed
         execute_workflow: false → abort, inform user
```

**Hook protocol** Example(Claude / Antigravity/Copilot PreToolUse):

- **Input**: JSON on stdin with the tool name and tool_input fields.
- **Output**: JSON on stdout. The orchestrator reads execute_workflow to decide.
- **Exit 0**: Always. A non-zero exit would crash the agent runtime.

#### Security Gate

The hook uses a **default-deny file policy**: unknown or unlisted extensions are blocked, not allowed.

**Blocked file types:**

| Category | Extensions |
|---|---|
| Executables & system binaries | `.exe`, `.dll`, `.so`, `.bat`, `.cmd`, `.ps1`, `.sh` |
| Scripts | `.js`, `.vbs`, `.py` |
| Binary / packaged | `.bin`, `.apk`, `.jar` |
| Office macros | `.docm`, `.xlsm` |

**Compound extension detection:** The hook inspects all suffixes in a filename using `pathlib.Path.suffixes`. A file named `requirements.pdf.exe` is detected and blocked regardless of the leading `.pdf`.

**MIME type validation:** When `python-magic` is installed, the hook validates the actual MIME type of the file, catching files that disguise their true type via a misleading extension.

#### `.py` file policy

Python files (`.py`) are **blocked by default**. This decision was taken considering:
- Security posture: scripts could contain arbitrary execution logic
- Resource consumption optimization: Python files are not valid input artifacts for this framework

To override this for a specific project, add the following to `agent.settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Read|Cat|Write|Edit",
        "hooks": [{ "type": "command", "command": "python3 hooks/security_language.py" }],
        "runtime_config": { "allowed_extensions": [".py"] }
      }
    ]
  }
}
```

#### File size limit

The default maximum input file size is **10 MB**. This value was chosen to:
- Prevent oversized payloads from degrading LLM context quality
- Optimize token consumption and processing costs
- Protect against zip-bomb or memory-exhaustion attacks via large archives

To change this limit for your project, edit `MAX_FILE_SIZE_MB` at the top of `hooks/security_language.py`:

```python
MAX_FILE_SIZE_MB: int = 10  # Change to your required limit
```

> Increasing this value will increase token consumption and processing time per run. Evaluate the trade-off based on your project's context file sizes.

#### Language Detection

The hook detects the user's input language **offline** using `lingua-language-detector`. No external API call is made. The detected language is injected as a structured rule into all sub-agent invocations.

**Supported languages (v1):**

| Language | Code | Fallback |
|---|---|---|
| English | `en` | ✅ Default fallback |
| Spanish | `es` | — |
| Portuguese | `pt` | — |
| French | `fr` | — |
| German | `de` | — |
| Italian | `it` | — |

**Confidence threshold: 0.75.** If detection confidence is below this value, the hook falls back to English and logs the raw confidence score in `HookResult.confidence` for diagnostics.

To add a new language, extend `LANGUAGE_RULES` in `hooks/security_language.py` and add the corresponding `Language` enum to the `target_languages` list in `_detect_language()`.

#### Prompt Injection Extraction

The hook enforces a deterministic Prompt Injection security gate using a **Structural Boundary Regex**.

This layer prevents attackers from bypassing LLM format validations by hiding instructions inside a requirement prompt. It applies the regex `r"^(RF-[a-zA-Z0-9\-]+):\s*(.*?)\.?\s*US\[(.*?)\]\.?$"` which:
- Extracts exactly the `rf_id`, the `action`, and the `user_story`.
- Automatically strips off any adversarial or unstructured text outside these exact format boundaries (e.g., `SYSTEM: ignore instructions`).
- Passes the strictly rebuilt, sanitized prompt back to the Orchestrator.
- Universally supports any language while enforcing strict structural boundaries.

**Installation**

Sugestion Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
# Install Python dependencies
pip install -r requirements.txt
# System dependency for MIME detection (optional but recommended)
sudo apt-get install libmagic1   # Debian / Ubuntu
brew install libmagic             # macOS
```

> If `python-magic` is not installed, the hook degrades gracefully — extension and size checks still run. MIME type validation is skipped.

> [Back to Top](#quick-link-reference)

#### Design Principles Applied for Hook Layer
|Principle|Application|
|---|---|
|**Single Responsibility**|Hook = security + language only. Orchestrator = workflow. Subagents = analysis.|
|**Defense in Depth**|Hook blocks first (deterministic). Orchestrator LLM constraint is secondary layer.|
|**Fail Closed**|Default-deny file policy and rigid structural Prompt extraction.|
|**Injection Mitigation**|Deterministic regex extracts only valid IEEE structure slots, dropping adversarial instructions.|
|**Stable Contract**|hook_contract.py is the interface. Neither side needs to know the other's internals.|
|**Model Agnostic**|Hook runs as an external subprocess — no provider-specific code.|
|**Auditability**|trace_id on every invocation links hook execution to generated artifacts.|
|**DRY**|Language rule generated once by hook, passed to all sub-agents via structured context.|


---

## Solutions Identified Risks

---

## Roadmap

### 1.  A Dedicated UI Web Interface 

- Improve the User Experience (UX) of the framework.
- Input requirements in a user friendly way. 
- Execute runtime in esasy btton action `run-refinement`.
- Track the runtime pipeline and artifacts.
- Generate reports of the runtime performance metrics

### 2. Evaluation Feature

A dedicated framework capability to measure the deterministic quality of the agents' outputs over time. This evaluation feature will benchmark generated artifacts (BDD scenarios, risk matrices, and NFR extractions) against a curated dataset of known-good requirements ("Golden Path"). 
For more details see [Skill Test Strategy-Roadmap](docs/qa_criteria_test_components_strategies.md)


>[Back to Top](#quick-link-reference)
