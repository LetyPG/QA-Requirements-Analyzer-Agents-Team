# Non-Functional Requirements (NFR) Analysis Reference

## Purpose

This reference defines the reasoning process for identifying, validating, and deriving Non-Functional Requirements (NFRs) during software requirements refinement.

Its objective is to ensure that every functional requirement is evaluated not only for its business behavior but also for the architectural qualities required to deliver a secure, reliable, performant, and maintainable software solution.

This reference combines guidance extracted from the IEEE 830 Software Requirements Specification standard with practical security analysis principles inspired by Threat Modeling.

The resulting NFRs must always be:

- traceable to the functional requirement;
- supported by project standards or architectural context;
- free of unsupported assumptions;
- expressed as verifiable quality requirements.

## Analysis Workflow

Perform the following activities sequentially.

| Step | Activity | Description |
| --- | --- |-------|
| 1 | Functional Requirement/Behavior Review  |  Analyze the functional behavior. |
| 2 | Architectural Concerns Identification   | Identify architectural concerns introduced by that behavior. |
| 3 | Evaluate Applicable NFR Categories   | Determine which NFR categories are applicable. |
| 4 | Security Review  | Perform a dedicated security analysis. |
| 5 | Project Standards Validation   | Validate candidate NFRs against project standards. |
| 6 | Evidence-Supported NFRs Derivation   |  Derive evidence-supported NFRs. |
| 7 | Coverage Validation   |  Verify coverage and traceability. |

---
## 1. Functional Requirement/Behavior Review
Begin by understanding the functional behavior. Identify:
- the actor
- the system behavior
- the affected assets
- processed information
- system interactions
- external integrations

Do not derive NFRs before understanding what the requirement actually does.

---
## 2. Architectural Concerns Identification
Determine which architectural qualities are introduced by the functional behavior.Examples include:
- protecting sensitive information
- handling concurrent requests
- ensuring service availability
- supporting external integrations
- preserving auditability
- maintaining usability
- ensuring regulatory compliance

Architectural concerns become candidates for NFR analysis.

---
## 3. Evaluate Applicable NFR Categories
Not every requirement requires every category.
Evaluate each category independently.

|Category | Description | Examples/Notes| 
| --- | --- |-------|
|**External Interfaces** | Evaluate whether the requirement introduces posible Interfaces| User Interfaces, Hardware Interfaces, Software Interfaces, Communication Interfaces (APIs, protocols, messaging) |
|**Performance** | Evaluate whether the behavior introduces measurable performance expectations.| response time; throughput; concurrent users; processing capacity; scalability. | 
|**Reliability** | Evaluate whether the feature requires trust factors| fault tolerance; recovery behavior; operational resilience; data consistency. |
|**Availability** | Evaluate whether uptime or service continuity requirements exist.| continuous availability; service recovery; operational continuity. | 
|**Security**| Evaluate whether the feature requires security measures| authentication; authorization; data protection; input validation; communication security; auditability; compliance.<br>**Note**: Every requirement should be evaluated for potential security implications. Security analysis is mandatory because security requirements are frequently implicit during functional refinement and are often omitted unless deliberately explored. The objective is not to discover vulnerabilities but to identify the security capabilities required to protect the system's assets, users, and business processes. | 
|**Maintainability** | Evaluate whether maintainability expectations should be preserved. | logging; diagnostics; monitoring; operational support. |
|**Portability** | Determine whether deployment or execution portability is relevant. | operating systems; cloud environments; platform compatibility. | 
|**Usability** | Evaluate usability and accessibility requirements. | accessibility; clarity; navigation; user feedback; error messages. |
|**Compliance and Other Requirements** | Determine whether additional obligations exist. | regulatory compliance; organizational policies; industry standards; mandatory governance requirements.|

---

## 4. Security Review

**Security should be treated as a first-class analysis activity** rather than a simple checklist item.

Many functional requirements implicitly introduce security expectations that must be refined into explicit requirements.
Every analysis must anssurance the CIA Triad principles: Confidentiality, Integrity and Availability.

### Security Analysis Questions applied to the functional requirement

Review every requirement using the following security questions.

**1. Authentication** - Does the feature require verifying user identity? Examples: login; session establishment; credential validation.

**2. Authorization** - Does the feature restrict actions based on permissions or roles? Determine whether authorization rules should exist.

**3. Sensitive Data** - Does the requirement process, store, display, or transmit sensitive information?
Examples:
- personal information;
- financial information;
- authentication credentials;
- confidential business data.

Determine whether protection mechanisms are required.

**4. Input Validation** - Can user-controlled input influence the system? Determine whether validation, sanitization, or integrity verification requirements should exist.

**5. Data Protection** - Does information require protection while:
- stored;
- transmitted;
- processed.

Evaluate whether encryption or other protection mechanisms are required by project standards.

**6. Communication Security** - Does the requirement communicate with:
- APIs;
- external services;
- third-party platforms;
- distributed systems.

Evaluate whether secure communication requirements apply.

**7. Auditability** - Should the action be traceable? Examples:
- security events;
- financial operations;
- administrative actions;
- configuration changes.

Evaluate whether logging or audit requirements are applicable.

**8. Compliance** - Determine whether the feature is subject to:
- legal requirements;
- contractual obligations;
- organizational security policies;
- industry regulations.


---

## 5. Project Standards Validation

Candidate NFRs must never be generated solely from inference.

**Every derived requirement Must be validated against the available Project Context.**

Examples of supporting evidence include:

- architectural standards;
- security policies;
- performance baselines;
- compliance requirements;
- organizational guidelines.

Reject any candidate that cannot be supported by project evidence.

---

## 6. Evidence-Supported NFRs Derivation

Convert validated architectural concerns into clear and verifiable requirements.

Derived NFRs should:

- describe observable system qualities;
- remain implementation independent;
- preserve traceability;
- be objectively testable.

Prefer statements such as:

- The system shall encrypt payment information during transmission.
- The system shall complete payment processing within the defined performance threshold.
- The system shall record authentication failures in the audit log.

Avoid unsupported implementation decisions.

---

## 7. Final Coverage Validation

Before completing the analysis verify that:

- every architectural concern was evaluated;
- every applicable NFR category was considered;
- security analysis was completed;
- every derived NFR has supporting evidence;
- unsupported assumptions were rejected;
- non-applicable categories are explicitly marked as N/A.

---
## Analysis Principles

| Frecuency | Conditions Principles |
| ----------| ------------------|
| Always | - begin with the functional behavior;<br>- derive architectural concerns before proposing NFRs;<br>- validate every candidate against project standards;<br>- preserve complete traceability;<br>- treat security as a mandatory refinement activity;<br>- prefer evidence over assumptions. |
| Never | - invent project policies;<br>- invent performance thresholds;<br>- invent compliance requirements;<br>- invent encryption algorithms;<br>- invent availability targets;<br>- derive requirements without supporting evidence. |

### Expected Outcome

A successful analysis produces a set of non-functional requirements that:

- are directly traceable to the functional requirement;
- align with IEEE software quality attributes;
- incorporate explicit security reasoning;
- are supported by project standards;
- improve requirements refinement by making implicit architectural expectations explicit before implementation begins.