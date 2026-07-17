# Quick link Reference  

This file contains detailed technical information explaining how the system achieves the requirements refinement process, and how the sub-agents represent the solution design.
This file answers: **How was the Requirements Refinement process broken down into sub-agents as a human intellectual decomposition?**

- [System-Level Decomposition Summary](#system-level-decomposition-summary)
- [Orchestrator](#orchestrator)
- [Sub-Agent A: BDD Validation Analyst](#sub-agent-a-bdd-validation-analyst)
- [Sub-Agent B: Risk Evaluator & QA Strategy](#sub-agent-b-risk-evaluator--qa-strategy)


---

## System-Level Decomposition Summary

The intellectual decomposition follows a **separation of concerns** model where each agent and skill has exactly one reason to exist:

| Component | Reasoning Domain | Standards Harness | Output Contract |
|---|---|---|---|
| **Orchestrator** | Workflow state, validation, delivery | orchestration only | Final merged report + 5 output artifacts |
| **Sub-Agent A / Skill 1** | Functional behavior → Gherkin and optionsal produces validation refinment questions | IEEE Std 830-1998; Example Mapping; Impact Mapping; Story Mapping | Gherkin AC (≥11 scenarios) via `behavioral_translation_template.json` |
| **Sub-Agent A / Skill 2** | Architecture constraints → NFRs | Project Context Manifesto; WCAG 2.1 AA | `bdd_validation_{RF_ID}.md` |
| **Sub-Agent B / Skill 1** | Quantitative risk diagnosis | OWASP Top 10; Weighted formula; Historical ADR | Risk score + severity + justification JSON |
| **Sub-Agent B / Skill 2** | Risk → Test strategy mapping | ISO/IEC/IEEE 29119; ISTQB RBT methodology; NFR-to-test matrix | `strategy_{RF_ID}.json` + consolidated report |

**Key architectural decisions that enforce this decomposition:**

- **No cross-contamination:** Agent A never touches risk or strategy. Agent B never modifies BDD scenarios or adds ACs
- **Data-driven scoring:** Risk scoring uses `scripts/risk_calculator.py`, not free-form LLM judgment
- **Historical memory:** `risk.log` and `history_{RF_ID}.json` provide an ADR trail across multiple requirements, enforcing evaluation consistency over time
- **Fail-fast with traceability:** Every validation failure emits a structured JSON error with trace information for end-to-end audit
- **Standards as harness:** Every reasoning step is grounded in a reference file in the skill's `reference/` directory — the LLM cannot deviate from the standard framework

>[Back to Top](#quick-link-reference)


**SOLID Principles Application**

| SOLID Principle | Application in System Design |
|-------------------|--------------------------------|
| **Single Responsibility** | Each agent and skill has one well-defined responsibility. Sub-Agent A focuses only on functional requirements and NFR extraction, never touching risk or strategy. Sub-Agent B focuses only on risk assessment and test strategy planning. The Orchestrator handles only workflow management and validation |
| **Open/Closed** | The system is open for extension but closed for modification. New QA processes can be added as new agents or skills without modifying existing code. For example, performance testing or security testing logics could be added as new sub-agents or procedures into new existing su-agent skills |
| **Liskov Substitution** | All sub-agents implement the same interface for the Orchestrator. The Orchestrator can substitute any sub-agent with another that implements the same interface without breaking the system. Example BDD Validation Analyst could be substituted by another sub-agent that also takes an  Requierement Framgment and userstory and produce BDD scenarios |
| **Interface Segregation** | Each agent has a minimal, role-specific interface. Sub-Agent A doesn't need risk management interfaces, and Sub-Agent B doesn't need BDD scenario generation interfaces. This keeps agents lightweight and focused |
| **Dependency Inversion** | High-level modules (Orchestrator) depend on abstractions (sub-agent interfaces) rather than low-level modules (specific agent implementations). This enables flexible composition and easier testing |

>[Back to Top](#quick-link-reference)

---

## Orchestrator

**File:** `orchestrator-agent.md` | Temperature: `0.3` | Role: Lead QA Orchestrator

### Agent Logic

The Orchestrator is the **central router and state manager** of the entire framework. It is the sole entry/exit point for user interaction and is responsible for every state transition in the workflow. It does not perform any analysis itself, it delegates, validates, and consolidates.

#### Responsibilities

| Responsibility | Description |
|---|---|
| **Hook Gate (Step 0)** | Before any action, reads `execute_workflow` from the `PreToolUse` hook (`hooks/security_language.py`). Aborts immediately if `false`, surfaces `block_reason` and `trace_id` to the user |
| **Language Rule Injection (Step 0.1)** | Prepends `HookResult.language_rule` verbatim to every sub-agent invocation to ensure language consistency across all artifacts |
| **Input Validation** | Validates the user input against the IEEE `RF-ID: "The system must [action]"` and User Story `US[as a [role]...]` formats. Hard-stops if format is invalid — never infers missing information |
| **Context Manifesto Validation** | Confirms `project-context/project_context_manifesto.md` exists and is readable. Invokes the `context-manifesto-user-guidance` skill if absent |
| **Context Injection** | Extracts and injects only the relevant slice of the Project Context Manifesto (tech stack, business rules, QA baselines) into sub-agent prompts — never the full file (DRY / token optimization principle) |
| **Delegation** | Triggers Sub-Agent A with the RF-ID, US, and context snippet. Responds to Sub-Agent B's context requests. Does not intervene in the A→B handoff |
| **Artifact Validation** | Validates sub-agent output artifacts against predefined JSON schemas via the `artifact-validation-fixing-loop` skill. Checks handoff compliance, artifact completeness, and Risk Matrix consistency |
| **Fixing Loop Control** | Manages the iterative correction loop (max 2 retries). Falls back to a structured failure report if unresolved |
| **Deliverable Generation** | Merges `bdd_validation_{RF_ID}.md` and `risk_evaluator_qa_strategy_{RF_ID}.md` into final artifacts in `outputs/{RF_ID}/` following `assets/final_report_schema.md` |
| **Self-Validation** | Performs a checklist verification of all output artifacts before emitting the final user message |
| **Failure Handling** | Documents persistent failures in `artifacts/logs/failure_log_workflow_{RF_ID}.json` |
| **State Management** | Tracks the status of every sub-agent invocation and ensures requirements are processed systematically |

>  **Note:** For more detailed information see [Orchestrator system Prompt](../orchestrator-agent.md)
> You could see rules, flow, ilustrative diagrams, contraints an contract scema used for validation. 
> You could also see the orchestrator skills details for validation, fixing loop,  failure hanlding and user guidance for context generation.

>[Back to Top](#quick-link-reference)

---

## Sub-Agent A: BDD Validation Analyst

**File:** `agents/bdd-validation-analyst-agent/bdd-validation-analyst-agent.md` 

### Agent Logic

Sub-Agent A is the **functional analysis specialist**. Its sole purpose is to transform a raw IEEE requirement and User Story into a structured Gherkin specification and extract implicit Non-Functional Requirements (NFRs). It operates as two strictly sequential internal skills and never interacts directly with the user.

#### Problem Decomposition Rationale

The intellectual decomposition here mirrors how a senior QA engineer approaches a new requirement:
1. First, understand *what* the system must do — functional behavior → BDD acceptance criteria
2. Then, understand *how well* the system must do it — non-functional constraints → NFRs

Separating these into two skills that represents 2 procedure scope funtional and non-funtional, optimizing reasoning depth, accuracy, narrow window of context to process, token usage and reducing error proneness.

**Skills general Details**
- Include input and output dependencies.
- Use specific schemas as handoff contracts between skills
- Apply spcific rules and conditionals
- Use self-validations.
- Apply specifics constraints, using `Must`, `Should`, `Could`, `Won't`, methods 

> **Note:** For more detailed information see [BDD Validation Analyst system Prompt](../agents/bdd-validation-analyst-agent/bdd-validation-analyst-agent.md)

>[Back to Top](#quick-link-reference)

---

#### Skill 1: `behavioral-translation`

**Responsibility:** Isolate functional test design logic. Translate the IEEE requirement into Gherkin Acceptance Criteria.

**Seven Stage Internal Process**

| Stage | Action |
|---|---|
| **1. Input Validation** | Validates all 3 mandatory inputs (IEEE Req, US, Context Snippet). Aborts with structured error JSON if any is missing — never infers |
| **2. Extraction** | Extracts `RF_ID` from the IEEE format to maintain full traceability |
| **3. Analysis** | Identifies preconditions (`Given`), triggering actions (`When`), observable outcomes (`Then`). Separates business rules from examples |
| **4. Generation** | Generates ≥11 acceptance criteria: 3 happy paths, 4 alternative/boundary/edge cases, 4 error scenarios. Must cover ≥95% of requirement complexity |
| **5. Style Conventions** | Enforces Gherkin rules: English keywords only, behavior-focused language, abstract data constraints (never invent specific values) |
| **6. Validation Questions** | Generate a list of validation questions to be answered by the business analysts or stakeholders | 
| **7. Self-Validation** | Pre-handoff checklist: syntax correctness, traceability to requirement, no unsupported assumptions, abstract constraints used for unspecified limits |

**Reasoning Reference Harness**

| Reference | File | Standards Embedded |
|---|---|---|
| **Requirements Analysis Techniques** | `skills/behavioral-translation/reference/requirements_analysis_techniques.md` | IEEE Std 830-1998; Example Mapping; Impact Mapping; Story Mapping |

**Three-technique combined strategy:**

| Phase | Technique | Reasoning Goal |
|---|---|---|
| **Phase 1 — Strategic Validation** | Impact Mapping | Validates *why* the feature exists, which actor it serves, and which behavioral change is expected. Guards against scenarios disconnected from measurable business goals |
| **Phase 2 — Journey Construction** | Story Mapping | Constructs the user workflow sequence. Ensures step transitions are covered. Identifies release slices |
| **Phase 3 — Behavioral Validation** | Example Mapping | Derives business rules → concrete examples → Gherkin scenarios. Primary tool for generating happy paths, boundary conditions, and error scenarios |

**Validation Questions Rationale**

Apply Validation Pattern Matrix
During refinement, for every input/control appearing in a BDD scenario, classify it first using validation pattern, and them apply a pattern checklist based in the classification to generate refinement questions to take in consideration for stakeholders users , Instead of only asking "Does this work?", ask: What type of input is this?

Example:

| Input/Control | Type | Question Pattern |
|:--- |:--- |:--- |
| First Name field | Text Input | What is the minimum/maximum length? Are special characters allowed? What encoding should be accepted? |
| Date of Birth | Date Picker | What calendar system? Timezone handling? Default value? Range of accepted dates? |
| Submit button | Action | Is there a confirmation step? What happens on network failure? Can the action be undone? |
| Password field | Masked Input | Password complexity rules? Recovery flow? Maximum attempts? |
| Email field | Pattern Input | Regex validation? International domains? Domain verification (MX)? |



**Core behavioral principles enforced by the reference:**
- Identify observable behavior, not implementation details
- Separate business rules from examples
- Treat ambiguities as *findings*, not assumptions — never resolve unknowns through inference
- Every scenario must trace to a requirement, rule, task, or business impact
- If no impact can be identified, report weak traceability instead of generating speculative scenarios

>[Back to Top](#quick-link-reference)

---

#### Skill 2: `nfr-extraction-and-reporting`

**Responsibility:** Extract implicit NFRs cross-referenced with the Project Manifesto, consolidate the final artifact, and perform the external handoff.

**Key Tasks**
1. **NFR Extraction** — Each NFR must directly reference a rule in the Manifesto. Categories: Security, Performance, Accessibility/UX (WCAG 2.1 AA), Compliance, Reliability
2. **Artifact Consolidation** — Merges Skill 1 output (Gherkin) + NFRs into a single structured Markdown report
3. **Resource Usage Capture** — Records: Input/Output/Total Tokens, Processing Time, Tools Called, Total RAM Used
4. **File Generation** — Writes `outputs/bdd_validation_{RF_ID}.md` using `skills/nfr-extraction-and-reporting/assets/bdd_validation_template.md`
5. **External Handoff** — Emits the trigger JSON to activate Sub-Agent B

**Reasoning Reference Harness**

| Reference | File | Standards Embedded |
|---|---|---|
| **Non-functional requirements (NFRs): Definitions, Categories, and Examples, NFR patterns** | `skills/nfr-extraction-and-reporting/reference/nfr_analysis.md` | Non-functional requirements (NFRs): Definitions, Categories, and Examples, NFR patterns |

>[Back to Top](#quick-link-reference)

---

## Sub-Agent B: Risk Evaluator & QA Strategy

> **File:** `agents/risk-evaluator-qa-strategy-agent/risk-evaluator-qa-strategy-agent.md` | Temperature: `0.4`

### Agent Logic

Sub-Agent B is the **quantitative risk and strategy specialist**. It is activated exclusively by the trigger JSON emitted by Sub-Agent A. It reads Sub-Agent A's output artifact, requests additional business context from the Orchestrator, and produces a data-driven risk matrix and test strategy.

#### Problem Decomposition Rationale

The intellectual decomposition here mirrors how a QA Lead and Test Architect collaborate after a BDD session:
1. First, evaluate *how critical a failure would be* — risk quantification using math and standards, not opinion
2. Then, design *what test coverage is justified* given that risk profile — ROI-optimized strategy grounded in the calculated score

Separating these into two skills prevents the model from conflating diagnostic analysis with prescriptive strategy, and forces it to ground strategy recommendations in a calculated, reproducible score.
This separation in 2 skills procedure allows to restrict scopes, optimizing reasoning depth, accuracy, narrow window of context to process, token usage and reducing error proneness.

> **Note:** For more detailed information see [Risk Evaluator system Prompt](../agents/risk-evaluator-qa-strategy-agent/risk-evaluator-qa-strategy-agent.md)

>[Back to Top](#quick-link-reference)

---

### Skill 1: `risk-evaluator`

**Responsibility:** Execute a multidimensional, quantitative risk analysis. Produce an objective, evidence-grounded risk score and justification.

**Five Stage Internal Process**

| Stage | Action |
|---|---|
| **1. Input Validation** | Validates the trigger JSON (RF_ID, User Story, BDD file path). Validates `bdd_validation_{RF_ID}.md` content (must contain ≥5 ACs and NFRs by category). Validates mandatory context from Orchestrator (Business Priorities, Related Functionalities, Tech Stack). Aborts with structured error if any mandatory input is missing |
| **2. Standard Alignment (Reference Check)** | Cross-references the BDD artifact and context with `reference/reference_risk_standard.md`. Identifies OWASP Top 10 matches and applies Red Flag rules (e.g., auth + PII → minimum Impact=5, minimum Complexity=5) |
| **3. Algorithmic Matrix Calculation** | Executes `scripts/risk_calculator.py`. Inputs: Business Impact (1–5 scale) and Technical Complexity (1–5 scale). Formula: `Risk_Score = (Impact × 0.7) + (Complexity × 0.3)`. Maps score to severity threshold |
| **4. Historical Consistency Verification** | Reads `assets/risk.log` to find requirements with similar tags. If current score deviates from historical patterns, generates a `technical_justification` clarification note. Updates `risk.log` (append only — never overwrite). Creates `outputs/history_records/history_{RF_ID}.json` |
| **5. Self-Validation** | Pre-handoff checklist: all mandatory fields populated, `technical_justification` references a standard, `Risk_Score` is mathematically correct, output format compliant, score consistent with NFRs from Agent A |

**Risk Score Formula and Thresholds**

The risc calculation logic is described in `scripts/risk_calculator.py`. See also `reference/reference_risk_standard.md` for the standards used for risk evaluation.

```
Risk_Score = (Business_Impact × 0.7) + (Technical_Complexity × 0.3)

  0.0 – 3.9  →  Low
  4.0 – 6.9  →  Medium
  7.0 – 8.9  →  High
  9.0 – 10.0 →  Critical
```

**Reasoning Reference Harness for Risk Standards**: (`reference/reference_risk_standard.md`)

Defines the objective criteria for assigning Impact and Complexity values used by `risk_calculator.py`.

| Dimension | Scale | Key Anchors |
|---|---|---|
| **Business Impact** | 1→5 | 1=minor visual change; 5=Auth/PII/Payments/Checkout |
| **Technical Complexity** | 1→5 | 1=CSS/static assets; 5=third-party integrations (Stripe/PayPal), DB schema changes |
| **OWASP Top 10 Adjustments** | +1 / +2 | 1 OWASP match → Complexity +1; ≥2 matches → Complexity +2 (max 5) |
| **Red Flag Rules** | Hard minimums | Auth/PII/Payments/Checkout → Impact ≥5, Complexity ≥5 regardless of calculation |

**OWASP Top 10 detection**

Applied as reasoning guards, here some examples:

| OWASP Category | Detected When Requirement Mentions |
|---|---|
| A01 Broken Access Control | Roles, permissions, private resources, multi-tenancy |
| A02 Cryptographic Failures | Passwords, tokens, PII, financial/sensitive data |
| A03 Injection | Free text inputs, search filters, dynamic queries, imports |
| A04 Insecure Design | New critical flows, incomplete/ambiguous validation criteria |
| A07 Identification & Auth Failures | Login, MFA, OTP, session management, SSO, password recovery |
| A08 Software & Data Integrity | Webhooks, pipeline automations, synchronizations |


**Deterministic Risk Calculation Script** (`scripts/risk_calculator.py`)

A deterministic Python script that enforces the weighted formula. Execution is **mandatory**, any deviation is classified as a critical failure. This moves the scoring decision out of the LLM's probabilistic reasoning domain into deterministic, reproducible code.

>[Back to Top](#quick-link-reference)

---

### Skill 2: `qa-strategy`

**Responsibility:** Translate the risk score from Skill 1 into a concrete, ROI-optimized test strategy and identify automation candidates.

#### Key Tasks
1. **Risk Coverage Mapping** — Maps the risk severity to required test levels using the decision matrix from `reference/qa_strategy_standards.md`
2. **NFR-Driven Test Augmentation** — If Agent A extracted Security, Performance, or UX NFRs, the corresponding test type is mandatory regardless of the risk score
3. **Automation Candidate Selection** — Risk score ≥3.5 (High/Critical) or recurrent regression flow → `automation_candidate: true`
4. **Resource Usage Capture** — Records full resource consumption including Skill 1's processing
5. **Deliverable Generation** — Writes the consolidated risk and strategy report; emits the final handoff JSON to the Orchestrator

**Reasoning Reference Harness for QA Strategy Standards** (`reference/qa_strategy_standards.md`)

Defines the decision matrix for selecting test levels based on risk and NFR profile.

**Source standards:** ISO/IEC/IEEE 29119 Software Testing; ISTQB Foundation Level Syllabus — Risk-Based Testing (RBT) methodology

| Risk Level | Required Test Levels | ROI Justification |
|---|---|---|
| **Critical (≥4.5)** | Unit, API Contract, DB Testing, Security (DAST), E2E UI | Protection of transactional flows and sensitive data |
| **High (3.5–4.4)** | Unit, API Integration, E2E UI (Happy Path), Performance (Load) | Stability in high-conversion flows |
| **Medium (2.5–3.4)** | Unit, API Functional, Sanity UI | Balance between coverage and delivery speed |
| **Low (<2.5)** | Unit, Manual Exploratory | Minimize script maintenance in low-impact areas |

**NFR-forced test type inclusions (override the risk score):**

| NFR Detected by Agent A | Mandatory Test Type Added |
|---|---|
| Security | Security Testing (DAST/SAST) |
| Performance | Performance/Load Testing |
| UX/Accessibility | Accessibility Testing (WCAG 2.1 AA) |

>[Back to Top](#quick-link-reference)

