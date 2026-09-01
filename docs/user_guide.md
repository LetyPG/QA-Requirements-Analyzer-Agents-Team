# User Guide and Best Practices

This document explains user best practices, responsibilities, and usage of the framework for requirements analysis. It also includes additional recommendations that become useful during usage, validated from real usage experience.

## INDEX

| Index | Description|
| ----- | -----|
| [Usage Flow Details](#usage-flow-details) | Explains the usage flow of the framework for real teamwork, mentioning custom integration suggestions and current access points.|
| [User Setup Responsibilities & Configuration Notes](#user-setup-responsabilities--configuration-notes) | Explains the solution setup and configuration notes for users.|
| [Post Deploy Monitoring and Metrics](#post-deploy-monitoring-and-metrics) | Explains the metrics and KPIs to monitor the solution in production.|
| [Directives](#directives-recomendations) | Lists the directives and best recommendations for the framework.|
| [Final Thoughts](#final-thoughts) | Details experience descriptions, objectives, and suggestions derived from solution implementation and usage experience. Includes LLM Model Comparison Examples (Gemini 3.5 Flash (High) and Claude Sonnet 4.6 (Thinking)). |

## Usage Flow Details 

Teams integrate the framework into their existing requirements workflow, typically before development handoff. The framework acts as a virtual QA analyst that reviews requirements collaboratively with the team, this could be integrated with team external ticketing or documentation platform through MCP, example: 

>The following are suggestions, but are outside the current scope of this framework's development.

**Custom integrations**
The user can create custom integrations to connect the framework with other tools and platforms, such as:
- **Jira**: Create, update, and track issues.
- **Notion**: Create, update, and track pages.
- **Azure DevOps**: Create, update, and track work items.
- **Slack**: Send notifications and alerts.
- **Teams**: Send notifications and alerts.

**Current solution access points:**
- IDEs Interface with AI Agents Embeddings
- CLI Agents 
- As a Roadmap item, a dedicated Web Interface will be added to track the runtime pipeline and results.

The solution runs the workflow using AI agents in a sequential agent chain pipeline. The workflow is orchestrated by `orchestrator-agent.md` and uses the sub-agents and their skills for each refinement activity. This design allows easy addition of new agents and skills in the future, but even though sub-agent logic is isolated, the sequential chain creates coupling between them, such that changes in one agent's processing and output generation can impact the next.


>[Back to Top](#index)
---

## User Setup Responsibilities & Configuration Notes

### Context Injection and System Constants

The project uses 2 important artifacts considered as constants for reasoning and persistent contextual memory. These must be adapted to the real project context, for example:

|Artifact| Description|Location|
|---|---|---|
| [`risk_standard`](../agents/risk-evaluator-qa-strategy-agent/skills/risk-evaluator/reference/reference_risk_standard.md) file | Synthetic example of Risk matrix (Business Impact and Technical complexity), which must be updated according to the organization's real risk matrix.| ./agents/risk-evaluator-qa-strategy-agent/skills/risk-evaluator/reference/reference_risk_standard.md|
| [`project_context_manifesto`](../project-context/project_context_manifesto.md) file | Synthetic example of project context, which must be updated according to the organization's real project context.| ./project-context/project_context_manifesto.md|

**Artifacts Setup**
You must take the 2 artifacts mentioned above and edit them according to your project's real details:

**1. Project Context** 
`./project-context/project_context_manifesto.md`

Currently system use a sytethic context manifesto, but the idea is :
- Edit in `project-context/project_context_manifesto.md` this file and add your project context and business rules, to make the system contextually aware of your project.
- Or create a new file `context-manifesto-user-guidance` that will, in case you need request guidance and the system will help you to create this file

| Condition|   System  Action |
|---|---|
|Missing `context-manifesto-user-guidance` | The orchestrator triggers a guided process to help the user create the file |

**2. Risk Standard** 
Location: `./agents/risk-evaluator-qa-strategy-agent/skills/risk-evaluator/reference/reference_risk_standard.md`

This file contains the Risk Evaluation standard used by the Risk Evaluator agent. It is a reference file that the agent uses to evaluate the risks of the requirements.
Currently the refrence point to:
- Business Impact Matrix (Scale 1-5), represents business impact details
   - It is recommended to keep the scale to avoid changes in other solution parts such as the script `risk_calculator.py`.
   - Edit only the description, impacts, etc. Avoid editing scale values.

- Technical Complexity Matrix (Scale 1-5), represents technological stack details.
   - It is recommended to keep the scale to avoid changes in other solution parts such as the script `risk_calculator.py`.
   - Edit only the technological criteria with your project details.
   - If you need to use a different risk scale, you should consider making the proper adjustments to the script `risk_calculator.py`.

>For more details of this setup needs see the file [implementation_risks.md](implementation_risks.md), on risk R2, R3 and R9. 

>[Back to Top](#index)

### Hook Configuration.

Currently the framework uses a dedicated `agent.settings.json` file to configure the `PreToolUse` Hook, but if you already have a dedicated custom agent setting file for your project, you can copy the `PreToolUse` Hook configuration into your project's agent setting file, preserving the exact hook object and script path/command.

>[Back to Top](#index)
---

## Post Deploy Monitoring and Metrics

After you use the solution, you must monitor it in production to identify patterns, and real outcomes  and benefits to your organization, and also help you to understand how to improve the solution and best practices as *improvement opportunities for solution*, remember this is agnostic solution so you must adapt the metrics to your project reality.

**Recomended metrics as Key Preformance Indicators (KPI):**

| KPI (%) | Description |
|---|---|
| **Requirements Quality Improvement** | Percentage reduction in ambiguities, inconsistencies, and missing acceptance criteria identified after requirements refinement.
| **Requirements Rework Time Reduction** | Percentage decrease in requirement modifications requested after development begins.
| **Requirement Defect Leakage** | Percentage reduction of defects traced back to incomplete or incorrect requirements during testing or production.
| **Requirements Review Time Efficiency** | Reduction in the time required to complete requirements analysis and review while maintaining quality standards.
| **Requirements Accuracy & Completeness Score** | Percentage of requirements meeting predefined quality criteria (clarity, consistency, traceability, testability, and completeness).
| **AI-Assisted Refinement Adoption Rate** | Percentage of project requirements refined using the AI-assisted process.
| **Human Validation Acceptance Rate** | Percentage of AI-generated refinement artifacts accepted with no or only minor modifications.
| **Requirements Traceability Coverage** | Percentage of functional and non-functional requirements successfully traced to acceptance criteria, test cases, and downstream SDLC artifacts.
| **Downstream Defect Reduction** | Reduction in defects discovered during development, testing, or production that originate from requirement deficiencies.|
| **Compliance Accomplished** | Percentage of requirements meeting predefined compliance rules and restrictions (for the solution processing itself and for the business/project requirements under analysis) |
| **Continuous SDLC Improvement Index** | Trend metric comparing baseline and post-adoption values across requirement quality, rework, defect leakage, and review efficiency to evaluate sustained process improvement over multiple project iterations. |
| **Performance of the Solution** | Resource consumption, response time, etc. |


>[Back to Top](#index)
---
## Directives Recommendations

The solution was measure in production using the KPI mentionated before, which helped the team that use it to identify patterns and best practices to use the solution and improve the quality of the generated artifacts.

From that perspective the fallowing **Directives** were documented as practice recomendations:

| Directive #| **Directive** | Contextual Insight |
|---|---|---|
| D1 | **System Behavior Context and the 10 Rules Acceptance** | Provides a fundamental understanding of the system's expected behaviors and the ten core rules that govern its operation. It serves as a baseline reference for evaluating the accuracy and completeness of the generated artifacts. **Relevance:** Ensures that the analysis aligns with the system's defined behavior and helps identify deviations or inconsistencies. | 
| D2 | **The 10 golden Rules of LLMs for Software Engineering** | Outlines ten essential guidelines for using Large Language Models in software engineering tasks. It emphasizes best practices for prompt engineering, context management, and evaluation. **Relevance:** Promotes effective and reliable use of LLMs, minimizing hallucinations and maximizing the quality of AI-generated outputs. |
| D3 | **One session by runtime** | To avoid the risk of context contamination or false positives/negatives, it is strongly recommended to perform the refinements in isolated sessions; this means one requirement refinement workflow per session, for new requirement refinement, open a new chat session. This ensures that each skill is assessed in isolation, without interference from other evaluations. | 
| D4 | **System Analysis, Refinement and Acceptance Criteria Generation Flow** | Details a structured approach to system analysis, requirement refinement, and acceptance criteria generation. It provides a step-by-step guide for the requirements analysis process. **Relevance:** Ensures a systematic and thorough approach to requirement analysis, leading to high-quality acceptance criteria. | 
| D5 | **Risk Evaluation and Test Strategy Formulation Flow** | Describes how to evaluate risks associated with requirements and formulate appropriate test strategies. It outlines the risk assessment process and test planning. **Relevance:** Supports risk-based decision-making and helps prioritize testing efforts based on identified risks. | 
| D6 | **Validation of LLMs Using Control Artifacts with LLMs** | Addresses the challenge of validating AI-generated outputs by using control artifacts and other LLMs. It provides methods for ensuring the quality and accuracy of LLM-generated content. **Relevance:** Enhances the reliability of the system by implementing robust validation mechanisms for LLM outputs. | 
| D7 | **Context Propagation in Agentic LLM Solutions** | Discusses the critical aspect of maintaining context across different agents in an LLM-based solution. It covers strategies for context management and information sharing. **Relevance:** Ensures consistent and context-aware behavior across the agentic system, preventing information loss and improving overall performance. | 
| D8 | **Non-Functional Requirements Elicitation and Evaluation** | Focuses on identifying and assessing non-functional requirements (NFRs). It provides guidance on eliciting and evaluating NFRs to ensure comprehensive requirement coverage. **Relevance:** Highlights the importance of NFRs in software quality and provides methods for their effective elicitation and evaluation. | 
| D9 | **Security-Oriented Requirement Analysis** | Addresses security considerations in requirement analysis. It provides a security-focused approach to reviewing requirements and identifying potential vulnerabilities. **Relevance:** Ensures that security is considered early in the development process, following the shift-left security principle. | 
| D10 | **Requirement Quality Assessment Framework** | Defines a comprehensive framework for assessing the quality of requirements. It includes metrics and guidelines for evaluating requirement quality. **Relevance:** Provides a structured approach to requirement quality assessment, ensuring that requirements meet defined standards. | 
| D11 | **Artifact Management and Storage Strategy** | Outlines a strategy for managing and storing artifacts generated during the requirements analysis process. It covers organization, versioning, and access control of artifacts. **Relevance:** Supports efficient artifact management and retrieval, ensuring that the right information is available at the right time. | 
| D12 | **User Feedback Integration and Continuous Improvement** | Addresses the importance of incorporating user feedback into the system. It provides methods for collecting, analyzing, and acting on user feedback. **Relevance:** Enables continuous improvement of the system based on user feedback and real-world usage patterns. | 
| D13 | **Performance Optimization and Resource Management** | Focuses on optimizing the performance of the LLM-based solution. It covers strategies for resource management and performance tuning. **Relevance:** Ensures efficient resource utilization and optimal performance of the system. | 
| D14 | **Error Handling and Exception Management** | Addresses error handling and exception management within the system. It provides guidelines for identifying, handling, and recovering from errors. **Relevance:** Enhances the robustness and reliability of the system by implementing effective error handling mechanisms. | 
| D15 | **Monitoring, Logging, and Observability** | Focuses on monitoring, logging, and observability of the system. It covers strategies for tracking system performance and identifying issues. **Relevance:** Supports proactive issue detection and resolution through comprehensive monitoring and logging. | 
| D16 | **Scalability and Maintainability** | Addresses scalability and maintainability considerations for the LLM-based solution. It provides guidance on designing for scalability and maintainability. **Relevance:** Ensures that the system can scale to meet growing demands and remain maintainable over time. | 
| D17 | **Documentation and Knowledge Base Management** | Covers documentation and knowledge base management for the system. It includes guidelines for creating, maintaining, and organizing documentation. **Relevance:** Supports knowledge sharing and enables users to effectively use and understand the system. | 
| D18 | **Security Compliance and Data Privacy** | Addresses security compliance and data privacy requirements. It ensures that the system complies with relevant security standards and privacy regulations. **Relevance:** Protects sensitive information and ensures compliance with legal and regulatory requirements. | 
| D19 | **Integration with Existing Workflows** | Focuses on integrating the solution with existing team workflows and tools. It provides guidance on seamless integration with existing processes. **Relevance:** Enhances user adoption and efficiency by ensuring that the solution fits well within existing workflows. | 


> The directives are grouped by logical similarity to avoid redundancy, but as the solution evolves, this grouping may be subject to change. Always refer to the latest version for the most accurate information.


### Quick Reference: Directives Checklist

For a concise overview of all 19 directives, use this checklist during your implementation and testing phases:

```
[ ] D1: System Behavior Context and 10 Rules Acceptance
[ ] D2: 10 Golden Rules of LLMs for Software Engineering
[ ] D3: One session by runtime
[ ] D4: System Analysis, Refinement and Acceptance Criteria Generation Flow
[ ] D5: Risk Evaluation and Test Strategy Formulation Flow
[ ] D6: Validation of LLMs Using Control Artifacts with LLMs
[ ] D7: Context Propagation in Agentic LLM Solutions
[ ] D8: Non-Functional Requirements Elicitation and Evaluation
[ ] D9: Security-Oriented Requirement Analysis
[ ] D10: Requirement Quality Assessment Framework
[ ] D11: Artifact Management and Storage Strategy
[ ] D12: User Feedback Integration and Continuous Improvement
[ ] D13: Performance Optimization and Resource Management
[ ] D14: Error Handling and Exception Management
[ ] D15: Monitoring, Logging, and Observability
[ ] D16: Scalability and Maintainability
[ ] D17: Documentation and Knowledge Base Management
[ ] D18: Security Compliance and Data Privacy
[ ] D19: Integration with Existing Workflows
```

>[Back to Top](#index)
---

## Final Thoughts

The solution was evaluated during 6 months using the metrics defined in the section **Post Deploy Monitoring and Metrics** and the results were very good. The solution was able to reduce the time spent on requirement analysis and improve the quality of the generated artifacts. 

The following are practical suggestions based on real experience:

- If your organization already has a mature and effective requirements refinement process, use this solution to complement and optimize existing practices rather than replacing established methodologies.
- Use AI-assisted requirements refinement based on structured reasoning and Retrieval-Augmented Generation (RAG) to improve analysis quality, consistency, and contextual accuracy over general-purpose LLM prompting.
- Treat this solution as a decision-support capability. Final ownership of requirements and progression to subsequent SDLC phases remains the responsibility of the engineering team.
- AI-generated outputs must not replace professional judgment. All generated artifacts should undergo human review and validation before adoption.
- Configure the solution according to your project's domain, architecture, standards, terminology, and organizational constraints to maximize relevance and accuracy.
- Benchmark the solution across multiple LLMs and select the model that provides the best balance of accuracy, completeness, consistency, cost, and compliance with organizational requirements.
- Maintain a consistent LLM model and version during benchmarking and production use. Although the workflow is deterministic, output quality may vary due to differences in model architectures and reasoning capabilities.
- Token consumption, execution time, and resource utilization are model-dependent characteristics rather than properties of the solution itself. These metrics are primarily influenced by the underlying LLM architecture and inference implementation.

### Model Comparisons

The next is an example of execution items results across 2 requirements examples with approximately the same complexity and size:

**Resource Utilization (Execution Metrics)**

|LLM Model and Version |input_tokens|output_tokens | total_tokens |processing_time (seconds) | tools_called | total_ram_used(MB)|processing_observed_behavior| 
|-----| -------|----|-----|------|------|------|----|
| Gemini 3.5 Flash (High) | 4500| 2000 | 6500| 9.0 | 5 | 145|
| Claude Sonnet 4.6 (Thinking) | 9270| 4090 | 13360| 17.3| 15| 153 | 

**Execution Behavior and Comparison**

| Proccessing Behavior and Comparison Item | Gemini 3.5 Flash (High) | Claude Sonnet 4.6 (Thinking) |
|-----|-------|----|
| **Adherence to Structural Constraints and Rules** | Failed the strict rule constraint requiring a minimum of 11 scenarios, generating only 5 basic scenarios. Omitted the "Validation Refinement Questions" section entirely. Wrote the Gherkin scenarios as inline sentences separated by commas rather than the traditional multi-line format, missing structural nuance. | Strictly followed the rule to generate a minimum of 11 BDD scenarios. It effectively categorized them by Happy Paths (HP), Alternative Flows/Boundary Conditions (AC), and Error Scenarios (ES). Included a detailed section for "Validation Refinement Questions", fulfilling optional/advanced constraints outlined in the framework. |
| **Depth of Analysis (NFRs and QA Strategy)** | Provided solid but surface-level NFRs and QA testing strategies. Correctly identified the `A03:2021-Injection` risk and mapped it well, but the detail in the E2E and API testing recommendations was relatively standard.| Showed a much deeper semantic understanding of the project context, generating highly detailed validation rules (NFRs) encompassing Accessibility, Usability, Reliability, and UX specifically tailored to the payment workflow. Recommended an extensive 7-level QA strategy based heavily on the specific OWASP matches and NFRs identified. |
| **Resource Utilization (Execution Metrics)** | Very fast and lightweight (9.0s and 6,500 total tokens).<br>- However, the speed and low tool count (5 tools) came at the cost of failing to meet the complex quantitative constraints (like the 11 scenarios).| Used significantly more tokens (13,360 total vs 6,500 for Gemini).<br>- Was slower (17.3s vs 9.0s).<br>- Used heavily iterated tool calling (15 tools vs 5), suggesting a more iterative reasoning and fixing loop process to verify schemas and outputs against the provided standards.|
| **Execution Behavior** | The agent was executing the pipeline in order since the orchestrator instructions input to workflow output and. <br>- The agent only infom the final message as expected and not the intermediate steps information| The agent first explore and read all the documents across the complete framework and then start the analysis and generation pipeline.<br>The output message was detailed and the agent show his internal reasoning steps and the outcome by eacxh steps from the pipeline, and at the end provide more detail than was conditionated as expected|

**Conclusion**

**Claude Sonnet 4.6** demonstrated superior alignment with strict constraints, schema validation, and deep reasoning capabilities, resulting in a higher-quality, fully compliant artifact. **Gemini 3.5 Flash** performed faster and cheaper but operated more like a standard summarizer, struggling to enforce rigorous framework rules and numerical constraints.
As important observation was check that both model execute first the hooks scripts.

See Gemini 3.5 Flash (High) ilustrative example in:
- [User Chat Message](images/gemini_3_5.png) 
- [Final Report in JSON](images/gemini_3_5_final_report.png)

See Claude Sonnet 4.6 (Thinking) ilustrative example in:
- [User Chat Message First Part](images/claude_4_6_1.png) 
- [User Chat Message Second Part](images/claude_4_6_2.png) 
- [Final Report in JSON](images/claude_4_6_final_report.png)


>[Back to Top](#index)


 
