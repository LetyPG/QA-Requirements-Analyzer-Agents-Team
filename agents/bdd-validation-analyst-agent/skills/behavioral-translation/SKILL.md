---
name: behavioral-translation
parent_agent: bdd-validation-analyst-agent
type: skill
description: Use this skill to transform the functional analysis into acceptance criteria in Gherkin format, when orchestrator provide IEEE Requirements, User Stories and Project Context Snippet.
license: Apache-2.0
compatibility: CLI agents(Clude, Antigravity, Wrappy) and IDE Agents (Cursor IDE, ANTIGRAVITY IDE, VsCode, Windsurf, etc)
metadata:
  author: Leticia Perez Gainza
  version: 1.0.0
---

# Skill: `behavioral-translation`

**Skill Goal:** Isolate the functional test design logic. It focuses exclusively on interpreting the business requirement and translating it into a standardized language to write Acceptance Criteria in Gherkin format, which describes the expected behavior of the system.

## **Input (From `orchestrator`):**

1. `IEEE Requirement & US`: Expected input used as contract format with this structure (e.g., *RF-ID-01: The system must process payments and the US[as a customer I want to pay with CC to complete my purchase]*).
2. `Project Context Snippet`: Business rules from the Manifesto used as specific context to clarify requirements.
3. `Aceptance Criteria Analysis Reference`: Aceptance Criteria Analysis standards in Gherkin format.

## **Internal Process:**

The skill operates under a seven-stage process:
1. **Input Validation**
2. **Extraction**
3. **Analysis**
4. **Generation**
5. **Acceptance Criteria as User Scenarios (Gherkin) Rules**
6. **Validation Refinement Questions**
7. **Self-Validation (Quality Verification)**
Finally **Handoff to `nfr-extraction-and-reporting` skill**

## **Internal Process:**

### 1. Input Validation:

#### Expected Input format:
- **IEEE Requirement**: RF-ID: "The system must [action]"
- **User Story(US)** : "[as a [role] I want to [goal] so that [reason]]"
#### Context Input

The `Project Context Snippet` could be in different format "plain text", "json", "markdown", it depends of the project structure, but it will always have business rules from the Manifesto.

**Rule**: The 3 expected inputs are mandatory and must strictly follow the format defined above, in case on context input could be in differents formats. 

**Conditional validation**:

- If the 3 inputs validation are successful, the agent MUST proceed to the next validation stage. 
- If the 3 expected input validation are not satisfied, the agent MUST abort the translation process and inform to the Orchestrator the validation status and the reason of the failure, indicating the exact missing input. it MUST NOT infer or hallucinate missing information. Example:

```json
{
  "status": "failed",
  "reason": "Skill 'behavioral-translation' input validation failed",
  "failure_details": "Missing IEEE Requirement"
}
```

### 2. Extraction:
Extracts the `RF_ID` to maintain traceability.

### 3. Analysis:

- Identify explicit business rules and infer observable system behavior
- Identifies the precondition (Given), the triggering action (When) and the observable result (Then).

### 4. Generation:
- Generates a **minimum of 11 Acceptance Criteria as User Scenarios (AC)**, expand this analysis into:
   - 3 **Happy paths**
   - 4 **Alternative flows/Boundary conditions- Edge Cases**
   - 4 **Error scenarios** 

**Procedure**: 
- Use as reasoning parameter the reference file `reference/requirements_analysis_techniques.md`, which contains standards  techniques, such as: Example Mapping, Impact Mapping,  Story Mapping.
- For AC, consider user behavior as **steps** in order to generate this,  use the rules from **5 Acceptance Criteria as User Scenarios (Gherkin) Rules**
- Each AC represent one independent behavior or quality concern per scenario, and it won't combine unrelated concerns such as:
  - functional behavior + performance
  - functional behavior + accessibility
  - functional behavior + security
  - unrelated functional behaviors
**Exception:** Multiple concerns MAY coexist only when they explicitly describe onebehavior that inherently spans those concerns.
- For include data in scenarios, you will use the **5.3 Data Usage Specification** section
- **Complexity Coverage**: the generated acceptance criteria must cover at least 95% of the complexity of the requirement. 

### 5. Acceptance Criteria as User Scenarios (Gherkin) Rules:

The Acceptance Criteria considered as the User Scenarios must be ensure its compliance with the fallowing Rules:

#### 5.1 Gherkin Style Conventions
- Use strictly English keywords (`Given`, `When`, `Then`, `And`) as steps in scenarios.
- Scenario names/titles must be concise and descriptive and use **one single-line, behavior-focused title**, for each `Scenario`.
- The scenarios are considered **domain-level abstractions**express steps at the domain/business level, use product, business, and actor terminology understandable to
a domain stakeholder, and describes what the *actor* does and what the *system* does.

#### 5.2 Structure and Intent
- **Chronological Execution**: The steps inside the scenario must follow a logical flow that mimics how a user would interact with the system.
- **One Single Purpose**: Each scenario must validate a single behavior or outcome, scenario should be granular and independent. Avoid mixing unrelated validations within the same scenario to maintain clarity and focus.
- **Behavior Over Implementation**: Avoid mentioning UI elements, implementation details, or specific technologies (e.g., "click the red button"), focus on the business behavior using behavior-focused language (e.g., "submit the payment form").
- **State Over Navigation**: Prioritize describing scenarios, as far as possible, in terms of system states and transitions rather than page loads or screen navigation, express meaningful starting states instead of reproducing every interaction required to reach that state, **unless** the interaction path itself is the behavior being specified. 

*Example:*

```gherkin
PREFER:
`Given the user is signed in with role "Editor"`

OVER:
`Given the user opens the login page`
`When the user enters the username`
`And the user enters the password`
`And the user clicks Login`
```
- **Scenario Length**: Each scenario must contain fewer than 10 steps, preferrably between 4 or 6 steps, in case a scenario requires more than 10 steps, evaluate whether:
    - multiple behaviors have been combined,
    - unnecessary navigation/setup is present,
- Given context can be reduced,
- a Scenario Outline or data table can simplify repetition.

IF the scenario still represents one coherent behavior after simplification,
it MAY exceed 10 steps.

#### 5.3 Vocabulary (ubiquitous language) and Language

- Use **one stable vocabulary** for roles, domain objects, and states.
- **Do not swap synonyms** for the same concept unless the product meaningfully distinguishes them (for example: "order" vs "purchase" vs "cart").
- **Declarative Language**: Steps should describe "what" needs to happen, not "how" it should happen, it should describe the intended behavior and resulting system state rather than  rescribing implementation procedures.

#### 5.4 Data Usage Specification

**Data Generalization Conventions:**
- Represent unknown values as business constraints.
- Use abstracts data representation instead of specific values.
  - Examples: Valid email, Invalid email, Minimum amount, Maximum amount, etc.
  - More example:

| Description | Bad Example | Good Example |
|------------|-------------|--------------|
| Age | Given the user is 18 years old | Given the user's age is within the allowed registration range |
| Name | Given the user enters "John" | Given the user provides a valid first name |
| Password | Given the password is "Password123!" | Given the password satisfies the password policy |
| Amount | Given the purchase amount is $500 | Given the purchase amount is within the permitted transaction range |

**Rule Priority**

In case that requirement information include data or business rules provided by the orchestrator, the following table shows how to represent them:

| Requirement information       | Representation                               |
| ----------------------------- | -------------------------------------------- |
| Explicit value in requirement | Preserve exactly                             |
| Explicit business rule        | Preserve exactly                             |
| Missing numeric threshold     | Describe as abstract constraint              |
| Missing format                | Describe using the governing validation rule |
| Unknown limits                | Never invent values                          |
| Unknown identifiers           | Use semantic placeholders                    |

Examples:

| Requirement         | Representation      | Rationale         |
| ------------------- | ------------------- | ----------------- |
| Password must contain at least 12 characters. | Given the password contains at least 12 characters | The value exists | because the value exists.|
| Password must be valid. | Given the password satisfies the password policy  | because no policy is defined.|
| User must be an adult. | Given the user meets the minimum age requirement | Not 18 years old|

### 6. Validation Refinement Questions

After all BDD scenarios have been generated and validated.
Enrich the BDD output by identifying validation-related controls or fields referenced in the scenarios and generating refinement questions that help discover missing acceptance criteria.

- Analyze each generated BDD scenario and identify user inputs, UI controls, or API fields mentioned in the scenario. Instead of only asking "Does this work?", ask: What type of input is this?
- Classify each field using a Validation Pattern as this: **Text, Numeric, Email, Password, Date, Phone, Dropdown, Checkbox, File Upload, Search, Currency**, etc.
- After clasification, apply a pattern checklist based in the **Pattern Checklist Selection** section and generate refinement questions only.
- Use abstract references (for example, the field, the input, the control); do not introduce concrete test data.
- Include only questions relevant to the detected validation pattern.

#### **Pattern Checklist Selection**

| Pattern     | Apply Questions About                                                        |
| ----------- | ---------------------------------------------------------------------------- |
| Text        | required, min/max length, character set, spaces, Unicode, special characters |
| Numeric     | min/max value, decimals, negatives, overflow, rounding                       |
| Date        | format, future/past dates, leap year, business restrictions                  |
| Email       | format validation, uniqueness, domain restrictions                           |
| Password    | length, complexity, reuse, expiration, masking                               |
| File Upload | file type, size limit, virus scanning, duplicate uploads                     |
| Dropdown    | default value, mandatory selection, inactive options                         |


**Expected Outcome**

The generated refinement questions should help the team identify missing validation requirements that can later be converted into additional acceptance criteria, BDD scenarios, and test cases during the refinement process.

Example:

**Validation Refinement Questions** (see example below):
**Field:** <Field Name> e.g. First name
**Pattern:** <Validation Pattern> e.g. Text
**Questions:**
* Is the field mandatory?
* What is the minimum allowed length?
* What is the maximum allowed length?
* Which character sets are allowed?
* Should leading or trailing spaces be trimmed?
* Are Unicode or accented characters allowed?
* What validation error message should be displayed?
* Are accessibility requirements applicable?

### 7. Self-Validation (Quality Verification):
Before handoff, you MUST review your own generated Gherkin, fallowing the next success criteria:
    
- [ ] validate Gherkin syntax and there are no missing the leading keywords, not even one.
- [ ] verify every scenario traces to the requirement.
- [ ] verify no scenario introduces unsupported business assumptions.
- [ ] verify abstract constraints are used whenever limits are unspecified.
- [ ] verify scenario names describe observable behavior.
- [ ] verify implementation details are not introduced.

---

## Constraints 

|**Type**|**Rule**|
|---|---|
|**Must**|Validates the 3 expected input before any otger proccessing action, in failure case abort processing and return the error message| 
|**Must**|Use as the main reasoning parameter the reference file `reference/requirements_analysis_techniques.md`, which contains the strictly needed  standards and  techniques
|**Must**|Validate that the generated scenarios follow the **Gherkin Style Conventions** and there are no missing the leading keywords, not even one| 
|**Must**|Generate a minimum of 11 Aceptance Criteros as User Scenarios (3 Happy paths, 4 Alternative flows/Boundary conditions- Edge Cases, 4 Error scenarios) |
|**Must**| Use abstract constraints whenever limits are unspecified.|
|**Must**| Ensure the acceptance criteria cover at least 95% of the requirement complexity.|
|**Must**| Before add any data set in scenarios, you must follow the **Data Usage Specification**.|
|**Should**| Genrate scenario names that describe observable behavior.|
|**Should**| Scenarios be declarative rather than imperative.|
|**Could**| Include traceability markers (e.g., Rule ID, Story ID).
|**Could**| Report unresolved questions separately.|
| **Won't** | NEVER process **Project Context Snippets** if executable files type are provided, like exe, .bat, .sh, .cmd, .ps1, .js, vbs, .py... etc.  |
|**Won't**| Introduce scenarios with unsupported business assumptions |
|**Won't**| For **validation refinement questions**<br>- Generate questions for user inputs, UI controls, or API fields, bussiness rules that are not explicitly mentioned in the scenarios.<br>- Generate hardcoded values, lengths, dates, emails, phone numbers, or identifiers.<br> - Convert the questions into implementation decisions.<br>- Create additional BDD scenarios in this phase.|
|**Won't**|Add implementation details or implementation-neutral descriptions in any scenario|
|**Won't**| conduct Infraestructure leakege, it means, never mention infraestructure terms, enviroment, databases or SQL queries,raw storage operations, internal schemas, servers, clients, platforms, technologies, frameworks, tools, libraries, APIs, implementation-level service details etc. **EXCEPTION**: These MAY be included when the behavior being specified is inherently exposed at that technical layer, such as an API-only product behavior.|  
|**Won't**|Include any UI or automation mechanics such as: selectors, XPath, CSS selectors, element identifiers, click element, wait for, scrolling, browser-specific operations, framework-specific commands|
|**Won't**|Invent values or limits when they are not specified|
|**Won't**| Produce documentation of the analysis methodology|
---

## **Internal Handoff (To Skill 2):**

* Delivers an explicit JSON object to the next skill `nfr-extraction-and-reporting` 
* Use the schema `assets/behavioral_translation_template.json` as strict contract to output JSON object.
* The output MUST perfectly match with the schema.
