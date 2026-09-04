# QA Requirements Analyzer Agents Team
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)[![Ruff](https://custom-icon-badges.demolab.com/badge/Ruff-261230.svg?logo=ruff-logo)](#)[![Pytest](https://img.shields.io/badge/Pytest-fff?logo=pytest&logoColor=000)](#)[![PyPI](https://img.shields.io/badge/PyPI-3775A9?logo=pypi&logoColor=fff)](#)[![Markdown](https://img.shields.io/badge/Markdown-%23000000.svg?logo=markdown&logoColor=white)](#)[![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white)](#)[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-886FBF?logo=googlegemini&logoColor=fff)](#)[![Claude](https://img.shields.io/badge/Claude-D97757?logo=claude&logoColor=fff)](#)[![ChatGPT](https://custom-icon-badges.demolab.com/badge/ChatGPT-74aa9c?logo=openai&logoColor=white)](#)[![Mistral AI](https://img.shields.io/badge/Mistral%20AI-FA520F?logo=mistral-ai&logoColor=fff)](#)[![Ollama](https://img.shields.io/badge/Ollama-fff?logo=ollama&logoColor=000)](#)[![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-000?logo=githubcopilot&logoColor=fff)](#)


![Runtime Illustration](./docs/images/runtime_example.png)

## Problem Origin 

The framework is designed as an **AI EngineeringOps** solution which introduces a **Shift-Left Quality** approach through a team of specialized AI Agents for Requirements Refinement Analysis. The framework orchestrates the analysis process, but the final responsibility for requirement approval, prioritization, and quality decisions remains with the human team. Its goal is to increase refinement efficiency, expose hidden quality concerns early, and support QA professionals, analysts, and product teams in producing implementation-ready requirements.

Think of this as an LLM narrow capability which enhances and conditions its reasoning through specific parameters and knowledge bases, reproducing the intellectual human process of a Software QA Specialist during Requirement Analysis. This increases deterministic validation, reduces hallucinations and solution variability, resulting in higher response reliability and consistency, augmented by human oversight and decision-making authority.

## INDEX

| INDEX | Description |
|---|---|
| [What Problem Does It Solve?](#what-problem-does-it-solve) | Describes common problems in projects caused by lack of strong quality assurance practices in early development cycles during planning and analysis phases |
| [How to Use It?](#how-to-use-it) | Description of prerequisites, configuration steps, user responsibilities (remember this is an agnostic solution and must be adjusted to your real project needs and context), and execution instructions |
| [How Does It Work?](#how-does-it-work) | Describes teamwork scenarios and solution access points |
| [What the Framework Produces?](#what-the-framework-produces) | Describes what the framework produces |
| [Benefits](#benefits) | Description of the benefits of the framework |
| [Workflow Overview](#workflow-overview) | Description of the workflow of the framework |

## Release History and Roadmap Completion

- [CHANGELOG](./CHANGELOG.md) at this point the new features, patches, and updates will be registered here.

## Quick Link Reference to Project Documentation:
- [Architecture, Implementation and Roadmap Details](./docs/architecture_implementation_details_roadmap.md)
- [QA Criteria and Test Components Strategies](./docs/qa_criteria_test_components_strategies.md)
- [Problem Decomposition & Subagents Design](./docs/problem_decomposition_subagents_design.md)
- [Implementation Risks](./docs/implementation_risks.md)
- [User Guide and Best Practices](./docs/user_guide.md)

## Repo Structure 

The repo structure is organized as follows:

```text
|_agents/                  # Sub-agent capabilities, skills, and knowledge base/RAG components
|_artifacts/               # Storage for assessment results of sub-agent validations executed by the orchestrator agent, including log traces
|_assets/                  # Static schemas used for artifact validation and contract compliance for final report generation
|_data-test-poc/           # Test data to validate the solution
|_docs/                    # Project documentation and implementation details
|_hooks/                   # PreToolUse hooks
|_output/                  # Storage for final report generation
|_project-context/         # Project context documentation used as persistent memory
|_skills/                  # Specific orchestrator procedure packages as skill definitions
|_tests/                   # Unit tests and integration tests for framework capabilities and hooks
|_requirements.txt         # Python dependencies for hook logic
|_orchestrator-agent.md
|_README.md                # Main project documentation
```
>[Back to Top](#index)

---
## What Problem Does It Solve?

The framework addresses a common situation in startups and fast-moving product teams:

**Typical gaps**
- Early-stage risk
- Requirements are written quickly and often contain ambiguities.
- Acceptance criteria are incomplete or inconsistent.
- Non-functional requirements remain implicit.
- Security considerations are discovered late.
- QA involvement occurs after development has started.
- Small teams may not have a dedicated QA specialist available during refinement.

>[Back to Top](#index)

---
## How to Use it?

### Prerequisites

**AI Agent LLM Solutions:** 
- IDE Embedded Agents, e.g.: GitHub Copilot in VSCode, Antigravity, Windsurf, Cursor IDE, etc.
- Or CLI Agents, e.g.: Claude CLI, Antigravity CLI, Ollama, etc.

**Input Artifacts:**

| Condition| Input Artifact | Description|
|---|---|---|
|Mandatory| IEEE Format RF | `RF-ID: "The system must [action]"`|
|Mandatory| User Story | `User Story: [as a [role] I want to [goal] so that [reason]]`|
|Mandatory| Project Context Manifesto | `./project-context/project_context_manifesto.md`, must be placed within the `project-context` directory |
|Optional | Other context details | Any other relevant context details provided by the user, via prompt or file (avoid high-volume context formats not optimized for AI) |

### Quick Start

```bash
git clone https://github.com/LetyPG/qa-requirements-analyzer-agents-team.git
cd qa-requirements-analyzer-agents-team
pip install -r requirements.txt
```

- Initialize a chat prompt in the IDE or via CLI, requesting the refinement process with `orchestrator-agent.md`. 
- Use the specific command instruction format starting with **Run**, followed by the input artifacts (RF and US). If you don't follow this format setup, the `PreToolUse` hook will block the request. This was implemented as a security measure; see more details in [Architecture Details - Hook Section](./docs/architecture_implementation_details_roadmap.md#hook-layer) and [PreToolUse Hooks](./hooks/README.md).
- Remember the `project_context_manifesto.md` must exist and be placed in the `./project-context` directory.
- Wait until the full pipeline completes and delivers the results.

**Example Prompt**

```txt
Run RF-ID "RF-001" The system must allow users to log in
User Story "User Story: as a user I want to log in so that I can access the system"
```
>See [data-test-poc](data-test-poc/data-test-poc.md) for more examples

**Strongly recommended: Avoid running multiple requirements refinement processes within the same chat session to prevent context window overload and high resource consumption. Instead run diffrent session by each requiremrnt Refinement proccesses**

For best practices and usage, see:
- [Post Deploy Monitoring and Metrics](./docs/user_guide.md#post-deploy-monitoring-and-metrics)
- [Directives Recommendations](./docs/user_guide.md#directives-recommendations)
- [Final Thoughts](./docs/user_guide.md#final-thoughts), includes a model comparison table with performance and reasoning process benchmarks.

>[Back to Top](#index)

### Configuration Notes - User Setup Responsibilities

The project uses 2 important artifacts considered as constants for reasoning and persistent contextual memory. These must be adapted to the real project context, for example:

- The [`risk_standard`](./agents/risk-evaluator-qa-strategy-agent/skills/risk-evaluator/reference/reference_risk_standard.md) file is a synthetic example of a Risk matrix (Business Impact and Technical complexity), so it must be updated according to the organization's real risk matrix.

- The [`project_context_manifesto`](./project-context/project_context_manifesto.md) file is a synthetic example of project context, so it must be updated according to the organization's real project context.

>For more details about these setup requirements, see [user_guide.md](./docs/user_guide.md#user-setup-responsabilities--configuration-notes).

>[Back to Top](#index)
---
## How Does It Work?

Teams integrate the framework into their existing requirements workflow, typically before development handoff. The framework acts as a virtual QA analyst that reviews requirements collaboratively with the team. It can also be integrated with external ticketing or documentation platforms through MCP.

The solution runs the workflow using AI agents in a sequential agent chain pipeline. The workflow is orchestrated by `orchestrator-agent.md` and uses the sub-agents and their skills for each refinement activity. Each subagent applies established software quality and testing references, including ISTQB, IEEE Std 830-1998, IEEE 29119, and OWASP Top 10, to provide structured, evidence-oriented assistance during requirements refinement. 

See more details about custom integration suggestions and solution access points in [Usage Flow Details](./docs/user_guide.md#usage-flow-details-)

**Strongly recommended**: **DO NOT modify the `orchestrator-agent.md` file or any other system prompt file in the framework**; doing so may cause the framework to not work as expected.

>[Back to Top](#index)

---
## What the Framework Produces?

Instead of generating code, the framework focuses on quality engineering artifacts that improve the readiness of a requirement for implementation.

- **Functional refinement:**
  - Acceptance criteria derived from the RF (IEEE format) and the User Story.
  - BDD/Gherkin scenarios for Happy Path, Alternative Path, and Negative Path behaviors.
  - Validation of requirement consistency and completeness.

- **Non-functional refinement:**
  - Identification of applicable NFR categories (performance, reliability, availability, usability, maintainability, etc.).
  - Dedicated security analysis inspired by threat modeling practices.
  - Detection of potential risks and estimation of risk severity based on business impact.

>[Back to Top](#index)
---
## Benefits

- Faster requirement refinement
- Guarantees multi-perspective analysis:
  - User Scenario
  - Functional and Non-Functional requirements
  - Business Goals
  - Technical Implementation
  - Security Preventive Measures
  - Performance Parameters
  - Usability Considerations
  - Accessibility Guidelines

> Even if the team doesn't have a dedicated QA professional, or does not have all the methodologies and base knowledge, it is expected that beginner users can scale their learning by applying Shift-Left, BDD, Risk-Based Testing, Threat Modeling, etc.
  
- Improved requirement quality
- Early identification of risks
- Prevents cascade failures
- Saves bug-fix time and development budget by preventing production incidents
- Operational efficiency by leveraging development resources from bug-fixing to feature development
- Improved system quality and reliability for delivered code
- Improved test planning
- Early identification of non-functional requirements
- Improved testability
- Early identification of security considerations
- Improved security
- Fosters a quality mindset across teams

**Enhance AI-native development** combining Specification Driven Development (SDD) with the acceptance criteria capability as a practice of Behavior Driven Development (BDD) methodology.

>[Back to Top](#index)

---
## Workflow Overview

This framework works as a sequential AI Agent pipeline using orchestration workflow architecture.

### **Framework High-Level Components Overview**

|Component | Type | Functionalities|
|---|---|---|
|`PreToolUse` Hooks | Scripts | Execute scripts before agent tool calls for workflow execution; control in a deterministic way security checks to prevent command and prompt injection; validate user prompt language to guarantee consistency between user request language and artifact outputs, providing better UX. For more details see [Hook Details](./hooks/README.md).|
|`orchestrator-agent` | Agent/Skills | Manages Project Context, Delegates Tasks, Evaluates Output Artifacts, Deliverables Generation, Handles Failures|
|`bdd-validation-analyst-agent` | Agent/Skills | Generates Acceptance Criteria in Gherkin Format, Extracts Non-Functional Requirements (NFRs), Generates BDD Validation artifact|
|`risk-evaluator-qa-strategy-agent` | Agent/Skills | Calculates Risk Matrix, Proposes a QA Strategy|

## Support Features
There are additional support features as follows:

**LLM dependency:**
- `orchestrator-agent`SKILLS:
  - `artifact-validator-fixing-loop`
  - `context-manifesto-user-guidance`
- `bdd-validation-analyst-agent`SKILLS:
  - `behavioral-translation`
  - `nfr-extraction-and-reporting`
- `risk-evaluator-qa-strategy-agent` SKILLS:
  - `risk-evaluator`
  - `qa-strategy`

- Context Memory and reasoning RAG:
  - `project-context/project_context_manifesto.md`
  - `nfr_analysis.md`
  - `reference_risk_standard.md`
  - `qa-strategy_standard.md`

**Deterministic behavior control:**
- Dedicated Hooks:
  - `pre-tool-use-hooks`:
    - `language-detection-hook`:
    - `security-guard-hook`:
    - `context-consistency-hook`:
- Risk Calculator `risk-calculator.py`

>[Back to Top](#index)

### `orchestrator-agent` Responsibilities:

- **State Management**
- **User Request Validation**
- **Context Injection**
- **Delegation**
- **Artifact Validation**
- **Deliverables Generation**
- **Failure Handling**

### Sub-Agents:
The Orchestrator manages a team of two specialized sub-agents to maintain separation of concerns and token efficiency:

1. **`bdd-validation-analyst-agent`:** `bdd-validation-analyst-agent.md` - In charge of Gherkin translation and NFR (Non-Functional Requirements) extraction.
2. **`risk-evaluator-qa-strategy-agent`:** `risk-evaluator-qa-strategy-agent.md` - In charge of calculating the risk matrix and suggesting the test strategy based on impact.


```mermaid
graph TD
    User([User Input: IEEE Requirement + User Story + Project Context Precondition]) --> Orchestrator
    subgraph AI QA Requirements Team
        Orchestrator[Orchestrator Agent:
- Manages Project Context
- Delegates Tasks
- Evaluates Output Artifacts
- Deliverables Generation
- Handles Failures]
        BDD_Analyst[BDD and Validation Analyst:
- Generates Acceptance Criteria in Gherkin Format
- Extracts Non-Functional Requirements NFRs
- Generates BDD Validation artifact]
        Risk_Evaluator_QA_Strategy[Risk Evaluator and QA Strategy:
- Calculates Risk Matrix
- Proposes a QA Strategy]
    end

    Orchestrator -- "1. Validate Input Req  \n2. Trigger Workflow: \nSends Req + Context" --> BDD_Analyst
    BDD_Analyst -- "3. Handoff: AC & Rules" --> Risk_Evaluator_QA_Strategy
    Risk_Evaluator_QA_Strategy -- "4. Requests Context Info" --> Orchestrator
    Risk_Evaluator_QA_Strategy -- "5. Handoff: Risk Matrix and QA Strategy" --> Orchestrator
    Orchestrator -- "6. Validation Loop" --> Orchestrator
    Orchestrator -- "7. Compiles Validated Deliverables" --> Outputs
    
    subgraph Deliverables
        Outputs[(Final Report.md & Payload JSON)]
        Notification([Notifies User: Location and Status])
    end
    
    Outputs --> Notification
```

>[Back to Top](#index)

## License

Copyright 2026 Leticia Perez Gainza. Licensed under the Apache License 2.0.

See [LICENSE](LICENSE) for details.

