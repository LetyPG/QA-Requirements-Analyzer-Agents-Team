# Test cases for Proof of Concept (PoC) of the qa-requirements-analyzer-agents-team

I this file vyou wil find to input scenarios used on the PoC, to request the requeriments analysis process of these scenarios, you will find two scenarios with the following characteristics:

1. **Simple Scenario**: A simple scenario that validates the basic functionality of the system.
2. **Complex Scenario**: A complex scenario that validates the advanced functionality of the system.

**How to use this scenarios calles a *trigger*?**
You just opne a session chat with your agent on cLI or IDE agent, always within the current project workspace, and use simple prompt to instruct the execution and copy paste belows text, just changing the requirement with the trigger you want to use:

```txt
Analyze the following requirement: {trigger_requirement}
```

---

## Trigger 1: "Smoke" Test- Simple Scenario

**Requirement:**
>Copy and paste this entire block into the chat.

```txt
RF-CAT-01: "The system must allow filtering products by category and price."
User Story:
As a customer, I want to filter search results,
to find products that fit my budget.
```

**Validation Objectives:**

- Validate that the handoff flow works,
- Verify that the Orchestrator reads the Manifest and that the Performance Skill is activated correctly.

**Expected Behavior:**

- **Functional Analysis:** It is a standard flow but requires clear Gherkin logic.
- **NFR:** It will activate the **Performance** baseline (latency < 200ms) as it is a catalog query.
- **Risk:** It should result in a **Medium** risk, allowing validation that Agent B is not "exaggerating" all risks to Critical.

---

## Trigger 2: High Complexity Case

**Requirement:**
>Copy and paste this entire block into the chat.

```txt
RF-PAY-05: "The system must process the order payment using credit cards securely."
User Story:
As a customer, I want to pay for my shopping cart,
to receive my order at home.
```

**Validation Objectives:**
Showcase the maximum potential of the AI:

- Identifies security risks,
- Money flows and
- The need for complex integration tests.

**Test Case Rationale:**
This scenario allows you to validate:

1. **Security:** It will immediately activate the **PII and Payments** "Red Flags" from `risk_standards.md`.
2. **Architecture:** It involves the backend (FastAPI), the database (PostgreSQL) and the integration with third parties (Stripe/PayPal).
3. **Critical Risk:** The `risk_calculator.py` should return a high score, forcing Agent B to recommend: **Security Testing, API Contract Testing and DB Testing**.
4. **Value Handoff:** You will see how the final JSON marks `automation_candidate: true` due to the criticality of the flow.

---
