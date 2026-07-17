---
name: nfr-extraction-and-reporting
parent_agent: bdd-validation-analyst-agent
type: skill
description: Use this skill to identifiy applicable non-functional requirements (NFRs) by analyzing the functional behavior when previouis skill provides it, and validating them against project standards. Also consolidates the behavioral analysis, including the previous skill output, derived NFRs, and writes the final artifact and manages the handoff to the next sub-agent.
license: Apache-2.0
compatibility: CLI agents(Clude, Antigravity, Wrappy) and IDE Agents (Cursor IDE, ANTIGRAVITY IDE, VsCode, Windsurf, etc)
metadata:
  author: Leticia Perez Gainza
  version: 1.0.0
--- 

# Skill: `nfr-extraction-and-reporting`

**Goal:** 

Analyze the functional behavior from BDD Scenarios and and identify non-functional requirements related to this behavior. Also writes the final artifact and manages the handoff to the next sub-agent.

**Acronym Clarification Note:** Non-functional Requirements abreviated as `NFRs` are requirements that specify criteria that can be used to judge the operation of a system, rather than specific behaviors.

## **Input (From Skill `behavioral-translation` and `orchestrator`):**

1. **Internal Handoff** from Skill `behavioral-translation`, this contains the original `RF_ID` and User Story  and generated `Gherkin Scenarios`
2. **`Project Context Snippet`**: Applicable project standards (Security, Performance, UX, Usability, Accessibility, Compliance, Reliability, etc.)
3. **NFR Reference**: Parameters for NFR analysis `reference/nfr_analysis.md`, used as the primary reasoning guide.

## **Internal Process:**

The skill operates under a 6-stage process:

1. **Input Validation**
2. **Behavioral Review**` 
3. **NFR Analysis**
4. **Artifact Consolidation**
5. **File Generation:** 
6. **Self-Validation (Quality Verification)**
Finally **Handoff to `risk-evaluator-qa-strategy-agent`**

### 1. Input Validation:

**Handoff Validation**
Validates contract compliance of the previous agents, you must validates that in yhe body payload are included the next keys and values:
- RF_ID exists.
- User Story exists.
- BDD scenarios exist. in Gherkin format (more than 5 scenarios)

**Rule**: The key-values mentionated above are mandatory, which can impact in the quality of the output of this skill, it will be valited.

**Conditional validation**:

- If the **Iternal Handoff** validation is successful, the agent MUST proceed to the next validation stage.
- If the **Internal Handoff** validation fails or is missing, the agent MUST abort the process and inform to the Orchestrator the validation status and the reason of the failure, return example:

```json
{
  "status": "failed",
  "reason": " 'bdd-analyst-agent' handoff or its outputs are missing.",
  "failure_details": "The bdd_scenarios deliver was not in Gherkin format."
}
```

**Optionals key-values**

- `Project Context Snippet`: You could receive this information provided as optional, which can be used to improve the quality of this skill goals, but if  it is unavailable, you can continue the consolidation process, but explicitly state:

```json
No project-specific non-functional baselines were provided.
```
- `Validation Refinement Questions`: This is enrichment information for user stories clarification, you do need to use this for your analysis process, you just needs to preserve this information in the consolidation process and returned as is to the next sub-agent.

### 2. Behavioral Review:
- Review the functional behavior produced by Skill 1.
- Treat the generated BDD scenarios as the functional source of truth.
- Do not modify or regenerate them.

### 3. NFR Analysis:
**Rule**:Use `reference/nfr_analysis.md` to:
- Identify architectural concerns introduced by the functional behavior;
- Determine which NFR categories are applicable;
- Identify candidate project standards;
- Validate applicability using the Project Context;
- Derive only supported non-functional requirements.
Reject every candidate that lacks explicit support.

### 4. Artifact Consolidation:
Assemble the final structured text report combining: 
- analyzed requirement, RF_ID, User Story,
- functional scenarios (BDD), provided by Skill 1,
- validated non-functional requirements, extracted by this skill.

Preserve complete traceability to the original RF_ID.

You must also have to include the computer resource usage for the complete processing executed, included the processing done by Skill 1. 
Extract the data of the tool-calls meemory and log system. Include:

- Input Tokens
- Output Tokens
- Total Tokens
- Processing Time
- Tools Called
- Total RAM Used

### 5. File Generation:
- Generate the final evaluation artifact by merginmg the information related to functional behavior and non-functional requirements in  a single output artifact.
- The generated artifact MUST strictly follow the schema provided in `assets/dd_validation_template.md`. Include all required sections and information.
- You will storaged this artifact in `../outputs/bdd-validation-analyst/` folder as `bdd_validation_{RF_ID}.md`.

### 6. Self-Validation (Quality Verification):
Before generating the artifact and handoff payload to the next sub-agent, you must verify your output to meet the following quality criteria:

- [ ] Validates base on evidence that  every NFR is supported by the Project Context; no unsupported architectural assumptions exist and the inferred requirements have supporting evidence.
- [ ] Validates the coverage evaluation for every applicable NFR category ; non-applicable categories were explicitly marked as `N/A`and functional scenarios remain unchanged.
- [ ] Verify it output artifact Markdown follows the required template: 
  - RF_ID is preserved;
  - required sections exist;
  - report is complete.
---

## Constraints

| **Type** | **Rule** |
| --- | --- |
| **Must** | Use `reference/nfr_analysis.md` as the primary reasoning reference. <br> - Preserve the behavioral analysis generated by Skill 1. <br> - Derive only evidence-supported NFRs. <br> - Preserve complete traceability. <br> - Follow the required Markdown structure exactly. |
| **Must** | Derive only NFRs supported by the Project Context|
| **Must** | follow the required Markdown template exactly |
| **Must** | include the computer resource usage for the complete processing executed |
| **Must** | generate the handoff payload required by the next sub-agent.|
| **Must** | Ignore **Validation Refinement Questions** for NFR analysis |
| **Should** | - Evaluate only applicable NFR categories. <br> - Explicitly report categories that are not applicable. <br> - Preserve deterministic behavior. |
| **Won't** | - Modify Skill 1 outputs. <br>  standards. <br> - Introduce architectural assumptions. <br> - Generate unsupported NFRs. <br> - Skip evidence validation. <br> - Produce additional output beyond the required handoff payload. |
| **Won't** | Invent architectural requirements or arbitrary NFR as project context info, in that case you should work with the information setup as mandatory. |
| **Won't** | Modify the **Validation Refinement Questions**, you should preserve them in the consolidation process and returned as is to the next sub-agent.|
| **Won't** | Use Project Contexts Snippet to avoid unsupported architectural assumptions |

---

## Output File: `outputs/bdd_validation_{RF_ID}_{timestamp}.md`

`bdd_validation_{RF_ID}_{timestamp}.md` file MUST strictly follow the `assets/bdd_validation_template.md` .

> Only categories evaluated by the Project Context should contain derived requirements.


### **Output / External Handoff (To `risk-evaluator-qa-strategy-agent`):**

After successfully generating the Markdown report, emit only the following lightweight handoff payload, keeping inter-agent communication structured

This payload serves as the exclusive communication contract with the next sub-agent. No additional explanatory text should be emitted.

**Example of the Handoff Payload:**

This is the only payload that the agent will deliver outwards upon completing its task, 

```json
{
  "rf_id": "{RF_ID}",
  "user_story": "{user_story}",
  "bdd_validation_file": "${pathTo}/outputs/bdd_validation_{RF_ID}_{timestamp}.md",
  "status": "success",
  "next_action": "evaluate_risk_and_strategy"
}
```



