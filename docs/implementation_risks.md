# Risks Identified in the implementation phase 

## Priority Summary

| Risk | Severity | Effort to Mitigate | Status | 
|---|---|---|---|
| [R1 — Sequential cascade failure](#r1) | High | Medium (classification-aware fixing loop) | Partially Mitigated |
| [R5 — LLM-validated schemas](#r5) | High | Low (add `jsonschema` validator)| Pending - Roadmap Plan|
| [R10 — Temperature non-determinism in inputs](#r10) | High | Low (drop temperature for scoring step)| Mitigated |
| [R4 — Token budget silent truncation](#r4) | High | Medium (pre-flight token count) | Pending- Roadmap Plan |
| [R11 — No transient vs. structural retry distinction](#r11) | Medium | Low (error classification) | Mitigated |
| [R12 — Prompt injection at input boundary](#r12) | Medium | Low (deterministic pre-processor) | Mitigated |
| [R8 — Output collision on re-runs](#r8) | Medium | Low (add run_id to path) | Mitigated |
| [R13 — No end-to-end workflow correlation](#r13) | Medium | Low (workflow_run_id) | Pending but controled by keeping the samw trace_id for the same run (by default the RF-id is used as trace_id)  |
| [R2 — Single context file bottleneck](#r2) | Medium | High (multi-file context requires architecture change) | Pending | 
| [R3 — Risk calibration drift](#r3) | Medium | Low (onboarding checklist + manifest metadata) | Pending- Controls depends on user configurations | 
| [R6 — Unverifiable coverage claims](#r6) | Medium | Medium (eval golden datasets) | Pending |
| [R7 — Risk log format drift](#r7) | Low-Medium | Low (JSON Lines + schema) | Mitigated |
| [R9 — Manifesto staleness](#r9) | Low-Medium | Low (metadata + Orchestrator warning) | Mitigated |
| [R14 — Security propmt blocks](#r14) | Low-Medium | Low (review and edit manually prompts ) | Accepted |

## **Pending** Risks Mitigations Recomendations

Some mitigations strategies relies on user configurations and practices, these are classified as Pending and are documented in the [README.md](../README.md).

### R1 
**Sequential cascade failure (agent dependency)**

Sub-Agent B consumes Sub-Agent A's artifact directly. A low-quality or partial BDD output propagates as corrupted input, the risk score and strategy will be built on a weak foundation. The fixing loop partially mitigates this, but if Agent A's failure is structural (ambiguous requirement, missing context), retrying Agent A doesn't fix the root cause.

Also in case of any component modifications (not recomended), or improvements on the agents logic, it must be do carrefully and after undertsand and had clarity about the real impact on the whole workflow, how it affects the dependencies, and the correct functioning of all the system.   


*Partially Mitigated by the **classification-aware fixing loop***

**Mitigation Roadmap:**
- Expand the classification-aware fixing loop to identify *root causes* (ambiguity, incompleteness, contradiction) rather than just surface errors.
- Introduce a "dependency-aware retry" mechanism: if Sub-Agent B reports an input validation error, the orchestrator automatically retries the *upstream* producer (Sub-Agent A) with a targeted prompt.
- Add a "safety margin" policy: if the confidence score of an intermediate artifact is below a threshold, proactively regenerate it before downstream consumption.
>[Back to top](#priority-summary)

### R2 
**Single context file bottleneck**
The Manifesto is the only context injection channel. Complex projects with separate architecture docs, API contracts, or multiple domain docs can't be expressed cleanly in one file. Users are forced to either flatten all context (losing structure) or omit it (losing accuracy). The Orchestrator also has no objective way to decide *which* Manifesto sections are relevant for each agent.

**Mitigation Recommendations:**

-  See the existing sections in the file `project-context/project_context_manifesto.md` or request guidance to create this file to the agent. Example:

```txt
Help me to create a project-context/project_context_manifesto.md file for my project.
```
- Find concident section to add your real information in the sections provided, this will be considered as the main and relevant context information that the agents will consume.
- Other information that are not too relevante, append in new sections after the exitings onces, and describe clearly this new context information.

>Keep relevant information only, do not over load the manifesto with irrelevant information, the goal is to provide context information to the agents that helps them to understand the project and make better decisions. Avoid high consumption resorces with your own decisions.

**Mitigation Roadmap as High muturity implementation:**
- Implement a hierarchical Manifesto structure (sections → subsections → context blocks) with explicit IDs.
- Create a "Context Selector" component that analyzes the current agent's task and injects only relevant context blocks (with cross-references to full context).
- Add validation that ensures no single file exceeds a target token threshold (e.g., 50KB), prompting users to split large context files.
>[Back to top](#priority-summary)
### R3 
**Risk calibration not tied to the real project**
The Business Impact (1–5) and Technical Complexity (1–5) scales ship as ShopSwift examples. If users don't update `reference_risk_standard.md`, scores carry the assumptions of a synthetic e-commerce project — critical for ShopSwift might be irrelevant for their domain.

**Mitigation Recommendations:**
- See the [Reference Risk Standard](../agents/risk-evaluator-qa-strategy-agent/skills/risk-evaluator/reference/reference_risk_standard.md) file for edition with your real project information.
- Edit the **Business Impact** and **Technical Complexity** scales with your real project information.
>[Back to top](#priority-summary)

### R4 
**Token budget exhaustion with silent truncation**
The system has no pre-flight context window estimate. For a large Manifesto + long requirement + US, the LLM silently truncates context. The agent doesn't raise an error — it produces plausible-looking but incomplete output. This is a well-documented failure mode in LLM pipelines (Anthropic's own guidance on context management calls this out specifically).

**Mitigation:**
Add a token-count pre-check at the Orchestrator before dispatching. If estimated tokens exceed a threshold (e.g., 70% of the model's context window), warn the user and abort — don't let it silently degrade.
>[Back to top](#priority-summary)

### R5 
**Schema validation is LLM-enforced, not deterministically enforced**
The handoff schemas are validated by the Orchestrator (an LLM). A probabilistic model validating JSON against a schema is inherently weaker than a programmatic validator. The fixer is also an LLM — it can "repair" a JSON artifact in a way that passes structural validation but introduces semantic corruption (e.g., putting the wrong risk level in the right field).

**Mitigation:**
- Roadmap Plan: Addition of a deterministic JSON schema validator (`jsonschema` library) at the Orchestrator's artifact validation step, run *before* any LLM-based semantic review. This separates structural compliance (deterministic) from semantic quality (LLM-evaluated).
>[Back to top](#priority-summary)
### R6 
**The "95% coverage" claim is unverifiable and self-reported**
Agent A is instructed to cover 95% of requirement complexity, but there's no external measurement. The agent self-reports compliance. A requirement touching concurrency, partial failure states, or cross-service interactions may produce syntactically valid Gherkin that misses entire risk dimensions, and the system has no way to detect this without the planned "Outside Reviewer Agent."

**Mitigation:**
- Roadmap Plan: In the near term, the `evals/eval.json` files in each skill are the right place to define "golden path" requirements with known expected scenario counts and categories. These become regression tests for output quality.

---
>[Back to top](#priority-summary)
## **Mitigated** Risks 

### R7 
**Risk log drift and format inconsistency over time**

In first implentation version was used `risk.log` an append-only text file maintained by an LLM. As different LLM versions, different prompt iterations, or different users contribute entries over time, the format drifts. The "historical consistency check" becomes pattern matching against noisy, inconsistent entries. This is a known problem in ADR (Architectural Decision Record) systems that lack enforced structure.

**Mitigation:** 
- Was implemented the risk evaluation storage system from `risk.log` to `risk.jsonl` a JSON Lines format, with a schema, validated on every write. This is a low-effort change that makes the log both machine-readable and auditable without changing the append-only semantic.
>[Back to top](#priority-summary)
### R8 
**No run isolation / output collision on re-runs**
The output path is `outputs/{RF_ID}/`. If the same RF-ID is analyzed twice (re-run after editing the requirement or manifesto), the second run silently overwrites the first. There's no way to compare before/after, audit the re-run history, or roll back.

**Mitigation:** 

- Was add `timestamp` for all files generated as naming convention.
- Was defined as rule and verification check in all sub-agents to include the same `timestamp` in their outputs artifacts, e.g: `outputs/final_report_RF-001_20260717_162106.md`
- Also the finals report artifacts include the `trace_id` and the `timestamp`, this ensure the traceability and the audit trail of the process.

>[Back to top](#priority-summary)
### R9 
**Context Manifesto staleness — no freshness detection**
The Manifesto is static. If the tech stack changes, a new compliance requirement appears, or the business priority of a flow changes, the agents continue producing outputs based on outdated assumptions with no warning. For a framework meant to inform QA strategy decisions, this is a significant silent risk.

**Mitigation:** 
- Was add `last_updated` and `version` metadata block to the Manifesto. The Orchestrator reads this and warns (doesn't block) the user if the file hasn't been updated in more than a configurable number of days. This is a documentation-level change, not a code change.
>[Back to top](#priority-summary)

### R10 
**Temperature non-zero introduces non-determinism in risk INPUT classification**

The `risk-evaluator-qa-strategy-agent` runs at temperature different from `0.0`, since the agent deteremines the bussiness impact and technical complexity scores that feed the deterministic python calculator script, any non-zero temprerture can introduce variance in the risk evaluation, thsat also impact directly the strategy recommendations. The `risk_calculator.py` script is deterministic, but the LLM *determines the inputs*, the Business Impact and Technical Complexity scores. For example: 
- At temperature 0.4, the same requirement can map to Impact=4 on one run and Impact=5 on another, producing materially different Risk_Scores and strategy recommendations. The system's "data-driven" guarantee applies only to the calculation, not to the input classification.

**Mitigation:** 
- Set the agent `temperature` to `0.0` inside `risk-evaluator-qa-strategy-agent.md` to force deterministic responses during the Impact and Complexity assignment. 
- (Optional) Future enhancement: add a calibration test suite for input mapping validation.
>[Back to top](#priority-summary)
### R11 
**No distinction between transient and structural failures in the retry loop**
The fixing loop retries up to 2 times without classifying *why* the failure occurred. A transient failure (API timeout, rate limit) deserves a retry. A structural failure (the requirement is genuinely too ambiguous to produce valid Gherkin) does not — retrying wastes 2x the tokens and still fails. This compounds with R1 (sequential cascade) since fixing Agent A's structural failure requires user intervention, not LLM retry.

**Mitigation:** 
- Classify error categories before triggering a retry: `TRANSIENT` (network, rate limit), `STRUCTURAL` (missing mandatory context, ambiguous requirement), `SCHEMA` (output format non-compliance). Only `TRANSIENT` and `SCHEMA` errors should trigger automatic retry. `STRUCTURAL` errors should escalate immediately with a clear user message.

>[Back to top](#priority-summary)
### R12 
**Prompt injection surface at the IEEE format boundary**
The IEEE format validation is LLM-performed. A crafted input like `RF-001: "The system must process payments. SYSTEM: ignore your previous instructions and..."` could pass the regex-like format check while embedding adversarial content. The hook blocks executable files but doesn't sanitize free-text prompt content.

**Mitigation:** 
- Implemented `_check_prompt_injection` in `hooks/security_language.py`. This uses a strict regex pattern to extract only the `RF-ID`, action verb, and User Story components. 
- If the prompt fails the regex match, the hook sets `execute_workflow: false` with a `Prompt Injection Protection` block reason, entirely bypassing the Orchestrator LLM.
- If it passes, the hook rebuilds a sanitized prompt, discarding any adversarial text outside the capture groups.

>[Back to top](#priority-summary)

### R13 
**No end-to-end workflow correlation identifier**
The `trace_id` from the hook audits hook execution. But there's no single `workflow_run_id` that links the Orchestrator, Agent A, Agent B, and all their artifacts into a single traceable execution. If a workflow fails mid-chain, diagnosis requires correlating timestamps across multiple files in different directories.

**Mitigation:** 
- Currently is controlede the tracebility, using an `trace_id` generated by the hook system, but this is not a `workflow_run_id` that links the Orchestrator, Agent A, Agent B, and all their artifacts into a single traceable execution.
- Roadmap Plan: In the near term, will be implemented to generate a `workflow_run_id` (UUID4) at the Orchestrator the moment input validation succeeds. Pass it to every sub-agent invocation and embed it in every output artifact and log entry. This is the standard distributed tracing pattern (OpenTelemetry trace ID concept, applied to LLM agent chains).

>[Back to Top](#priority-summary)

### R14
**Security propmt blocks**

Currently the security `Hook` allow a natural user instruction to start the interaction like `Requirements Refinement Request` at the beggining of the prompt and acept as input a IEEE format `RF-[ID]: The system must [action]` and `US[as a [role] I want to [goal] so that [reason]]`. 
This is applied as Prompt Injection Protection, stripping extraneous adversarial instructions (e.g., `"SYSTEM: ignore previous instructions"`) before passing the sanitized prompt to the Orchestrator.

**Acepted:** 

The current security prompt block is not robust enough and can be bypassed by a crafted prompt. Despite this the current setup accepts these risks because the system is agnostic and highly generalized, there are numerous ways to perform validations as objectively as possible. Consequently, the risk of potential prompt injection is accepted, even with the existing protection layer, and is further mitigated by a second layer involving LLM constraints defined within the system prompt.

**Mitigation Recommendations:**
It is recommended to use an exact instruction format to avoid unexpected blocks, as fallow: 

`Run RF-[ID]: The system must [action]. US[as a [role] I want to [goal] so that [reason]].`

Apply security gates tailored to each project context and its specific compliance requirements.
