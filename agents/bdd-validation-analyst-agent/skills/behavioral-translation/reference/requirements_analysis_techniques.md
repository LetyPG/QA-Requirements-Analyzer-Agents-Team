# Behavioral Analysis Reference

The fallowing reference use IEEE Std 830-1998- Recommended Practice for
Software Requirements Specifications, and best industries practices for analyzing software requirements.

## Purpose
This reference defines how to derive behavioral scenarios from software requirements using three complementary analysis techniques:
- Example Mapping
- Impact Mapping
- Story Mapping
The focus is on **reasoning behavior**, not on explaining the methodologies themselves.

---
# General Behavioral Principles
When analyzing a requirement:
- Identify observable behavior instead of implementation details.
- Separate business rules from examples.
- Convert abstract requirements into concrete scenarios.
- Detect missing information before generating scenarios.
- Preserve traceability between business objectives, user behavior, and testable functionality.
- Treat ambiguities as findings, not assumptions.
- Produce scenarios only from supported evidence.
Never:
- Invent business rules.
- Infer unspecified behavior as fact.
- Hide unanswered questions.
- Mix strategic objectives with user interaction flows.
---
# Technique 1 — Example Mapping
## Objective
Derive executable behavioral scenarios by decomposing a requirement into rules, examples, and unresolved questions.
## Analysis Process
For each requirement:
### Step 1 — Identify the Story
Determine the feature or capability being discussed.
Ask:
- What functionality is being described?
- What user behavior is expected?

### Step 2 — Extract Rules
Identify explicit business constraints.
Rules describe:
- conditions
- restrictions
- validation logic
- acceptance criteria
Rules should be declarative.
Do not confuse rules with examples.

### Step 3 — Generate Concrete Examples
For every rule, derive one or more concrete behavioral examples.
Examples should describe:
- a specific situation
- relevant inputs
- expected outcome
Each example should demonstrate how a rule behaves under realistic conditions.
Cover:
- normal behavior
- alternative behavior
- boundary situations
- failure situations when supported by the requirement

### Step 4 — Identify Unknowns
Whenever required information is missing, record it as an unresolved question.
Typical indicators include:
- undefined behavior
- missing acceptance criteria
- unspecified limits
- conflicting rules
Do not resolve unknowns through inference.

## Scenario Derivation Behavior
Generate scenarios by mapping:
Rule -> Concrete Example -> Expected Behavior
Every scenario should validate one observable business rule.
If a rule cannot be demonstrated through an example, treat the requirement as incomplete.

## Story Splitting Behavior
If analysis reveals:
- excessive rules
- many unresolved questions
- unrelated behaviors
identify the requirement as a candidate for decomposition rather than continuing to expand scenarios.

---

# Technique 2 — Impact Mapping
## Objective
Derive scenarios that remain traceable to measurable business outcomes.
## Analysis Process
### Step 1 — Identify the Goal
Locate the measurable business objective.
The goal should define:
- desired outcome
- measurable success
- business direction
If no measurable goal exists, report the limitation.

### Step 2 — Identify Actors
Determine who can influence the goal.
Actors may include:
- end users
- administrators
- internal teams
- external stakeholders
- partner systems
Avoid collapsing all behavior into a generic "user."

### Step 3 — Identify Behavioral Impacts
For each actor, determine:
What behavior must change to move the goal?
Impacts describe behavioral change, not features.
Examples of impacts include:
- completing onboarding
- sharing content
- increasing adoption
- reducing abandonment

### Step 4 — Identify Deliverables
Only after identifying impacts should implementation ideas be considered.
Deliverables exist to create the behavioral impact.
Never reverse the reasoning by starting from features.

## Scenario Derivation Behavior
Behavioral scenarios should preserve this traceability:
Goal -> Actor -> Behavior Change -> Deliverable -> Scenario

Every generated scenario should clearly answer:
- Which actor performs the behavior?
- Which behavioral impact is exercised?
- Which business goal does it support?
If no impact can be identified, report weak traceability instead of generating speculative scenarios.

## Feature Validation Behavior
When reviewing proposed functionality, verify that every deliverable can be justified through:
- an actor
- an expected behavioral impact
- a measurable goal
Deliverables without traceability should be identified as unsupported.

---
# Technique 3 — Story Mapping
## Objective
Derive scenarios that preserve the complete user journey and support incremental delivery.
## Analysis Process
### Step 1 — Identify Activities
Determine the major stages of the user's journey.
Activities represent high-level workflow steps.

### Step 2 — Identify Tasks
Within each activity, identify the tasks users perform.
Tasks represent meaningful interactions.
Do not confuse tasks with user stories.

### Step 3 — Derive User Stories
Generate user stories beneath each task.
Stories describe individual behaviors that implement the task.

### Step 4 — Organize by Priority
Arrange stories from:
Essential behavior -> Additional behavior -> Enhancements
This ordering defines incremental releases.

## Scenario Derivation Behavior
Generate scenarios that validate:
- individual tasks
- transitions between tasks
- end-to-end workflow continuity
Scenarios should preserve the logical sequence of the user journey.
Avoid generating isolated scenarios that ignore preceding or following interactions.

## Journey Validation Behavior
Walk through the workflow from beginning to end.
At every transition ask:
- Is a required step missing?
- Does the workflow remain coherent?
- Can the user continue successfully?
Treat missing transitions as scenario gaps.

## Release Slicing Behavior
When defining an MVP:
derive scenarios only for the minimum end-to-end slice that delivers user value.
Avoid generating scenarios for lower-priority enhancements until the core journey is complete.

---
# Combined Analysis Strategy
When multiple techniques are available, apply them sequentially.
## Phase 1 — Strategic Validation
Use Impact Mapping to determine:
- why the capability exists
- who it serves
- which behavioral change matters
---
## Phase 2 — Journey Construction
Use Story Mapping to determine:
- how users experience the capability
- workflow order
- task decomposition
- release slices
---
## Phase 3 — Behavioral Validation
Use Example Mapping to derive:
- business rules
- concrete examples
- behavioral scenarios
- unresolved questions
---
# Common Reasoning Checks
Before completing scenario generation, verify:
## Rule Coverage
- Every rule has at least one behavioral scenario.
- Every scenario validates observable behavior.

## Traceability
Every scenario can be traced to:
- a requirement
- a rule
- a task or activity
- or a business impact, depending on the technique used.

## Completeness
Identify:
- missing rules
- missing workflow steps
- missing actor behavior
- unanswered questions
Report gaps explicitly instead of filling them with assumptions.

## Behavioral Quality
Generated scenarios should:
- describe observable behavior
- remain deterministic
- use evidence from the requirement
- avoid implementation details
- avoid speculative reasoning
- remain consistent with the selected analysis technique

## Story Completeness
Each story should represent:
- a single, testable behavior
- a clear user action
- an observable outcome
- complete context (Given/When/Then)
Avoid:
- multi-purpose stories
- ambiguous outcomes
- missing preconditions

## Alignment
All derived scenarios must align with:
- the project context
- the original requirement
- the selected analysis technique's principles
- the defined behavioral quality standards
---
# Non-Goals
This reference does not:
- explain how to perform Example Mapping
- explain how to perform Impact Mapping
- explain how to perform Story Mapping
- define the history or theory of these techniques
- provide templates for non-behavioral documents
The sole focus is on deriving **behavioral scenarios** using these techniques as reasoning tools.

---
# When to Use Each Technique
Choose the technique based on what the requirement emphasizes:
## Use Impact Mapping when:
- The requirement describes a strategic objective.
- The purpose is measurable.
- Traceability to business outcomes is required.
## Use Story Mapping when:
- The requirement describes a user journey or workflow.
- Incremental delivery is expected.
- Transitions between steps matter.
## Use Example Mapping when:
- The requirement contains business rules and conditions.
- You need to explore variations (happy paths, boundaries, failures).
- Testable scenarios are the primary output.
## Use Combined Approach when:
- The requirement is complex.
- Multiple perspectives (strategic, journey, behavioral) are needed.
- A comprehensive understanding is required.

