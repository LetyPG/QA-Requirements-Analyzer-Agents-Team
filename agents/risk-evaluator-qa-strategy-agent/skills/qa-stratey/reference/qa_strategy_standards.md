# QA Strategy Standards- Risk-Based Testing (RBT) Methodology

This document defines the decision matrix for selecting test levels and automation candidates based on risk and NFRs.
It fallows teh Best Industry Practices for QA Strategy and Risk-Based Testing (RBT) methodology.

## Risk-Based Testing (RBT) Methodology

The Risk-Based Testing (RBT) methodology is a systematic approach to software testing that focuses on identifying and prioritizing testing efforts based on the level of risk associated with different parts of the software. This approach ensures that the most critical functionalities are tested thoroughly, while less critical functionalities are tested to a lesser extent, optimizing testing resources and improving overall testing efficiency.

### **Source**: INTERNATIONAL STANDARDs
1. ISO/IEC/IEEE 29119 Software and systems engineering—Software testing, 
2. ISTQB Software Testing Foundation syllabus

>Extracts from ISO/IEC/IEEE 29119-1 and ISTQB Software Testing Foundation syllabus

It is impossible to test a software system exhaustively, thus testing is a sampling activity. A variety of testing
concepts (e.g. practices, techniques and types) exist to aid in choosing an appropriate sample to test and
these are discussed and outlined in this standard. A key premise of this standard is the idea of performing the
optimal testing within the given constraints and context using a risk-based approach.

- This is achieved by identifying the relative value of different strategies for testing, in terms of the risks they
mitigate for the stakeholders of the completed system, and for the stakeholders developing the system.
- Carrying out risk-based testing ensures that the risks with the highest priority are paid the highest attention
during testing. 

**Risk Categorization**
Risks can be categorized in a number of ways. For instance, risks can be identified in terms of:
- Not satisfying regulatory and/or legal requirements
- Failing to meet contractual obligations
- Related to unsuccessful progress and completion of the project (project risks)
- A work product not achieving its expected behaviour (product risks).

When performing risk-based testing, risk analysis is used to identify and score risks, so that the perceived
risks in the delivered system (and to the development of this system) can be scored, prioritized and
categorized and subsequently mitigated. 

**Using Risk-Based Testing in the Test Management processes** 

The categorised risk profile (the identified set of risks and their scores) is used to determine what testing
should be performed on the project – this is described in the test strategy, which will be use as input for part of the test plan.

**For instance, the risk scores can be used to determine the rigour of testing** (e.g. test sub-processes, test
design techniques, test completion criteria). 

- The prioritization of risks may be used to determine the test
schedule (testing associated with higher priority risks is typically addressed earlier). 
- The type of risk can be used to decide the most appropriate forms of testing to perform. For instance, if there is a perceived risk in the interfaces between components, then integration testing may be deemed necessary, and if there is a
perceived risk that users may find the application difficult to use, then usability testing may be deemed mnecessary.

**Using Risk-Based Testing in the Dynamic Testing processes**

The risk profile is used to provide guidance to all the dynamic testing processes:
- In the test design process the product risks are used to inform the tester which test design techniques are most appropriate to apply. 
- It can also be used to guide how much test analysis occurs during the test design process, with higher risk areas
receiving more effort than low risk areas. 
- Risk can also be used to prioritise the feature sets and, once they are derived, the test conditions and the test cases.
- Dynamic test execution is a risk mitigation activity. Running test cases mitigates risk because if the test passes then the likelihood of the risk occurring is normally lower – and so the risk score is reduced. 
- Similarly, if the test fails, the risk may increase. The process of test incident reporting would then be used to determine if
the failed test case had resulted in an issue or if it required further investigation. 

---

## 1. Test Levels Selection by Risk

This is a general matrix guidance to conduct the QA Strategy based on **Risk-Based Testing (RBT)** methodology and the Risk score calculated by the `risk-evaluator` skill.

| Risk (Score) | Required Test Levels | Justification of ROI |
| :--- | :--- | :--- |
| **Critical (>= 4.5)** | Unit, API Contract, DB Testing, Security (DAST), E2E UI. | Protection of transactional flows and sensitive data. |
| **High (3.5 - 4.4)** | Unit, API Integration, E2E UI (Happy Path), Performance (Load). | Ensure stability in high-conversion flows. |
| **Medium (2.5 - 3.4)** | Unit, API Functional, Sanity UI. | Balance between coverage and delivery speed. |
| **Low (< 2.5)** | Unit, Manual Exploratory. | Minimize script maintenance in low-impact areas. |

## 2. Mapping Matrix by NFR (Non-Functional Requirements)

If Agent A detects one of these NFRs, the corresponding test type must be included regardless of the risk score:

* **NFR Security:** Include `Security Testing` mandatory.
* **NFR Performance:** Include `Performance Testing` mandatory.
* **NFR UX/Accessibility:** Include `Accessibility Testing (WCAG)` mandatory.

## 3. Automation Criteria

A functionality is **Automation Candidate: True** if:

* The risk is >= 3.5 (High/Critical).
* Or if it is a recurrent regression flow defined in the Manifesto.

**Rationale:**



