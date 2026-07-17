# Risk Classification Standard - ShopSwift

This document defines the objective criteria for assigning Impact and Complexity values, used by `risk_calculator.py`.

## 1. Business Impact Matrix (Scale 1-5)

| Level | Category | Description / Example in ShopSwift |
| :--- | :--- | :--- |
| **5** | **Critical** | - Authentication Security, Authorization, and PII Management. Ex: login, registration, password recovery, personal data management. Money flows or sensitive data. Ex: Checkout, Payment, PII Management. |
| **4** | **High** | Core functionalities that affect conversion. Ex: Shopping cart, Search engine, User registration. |
| **3** | **Medium** | Customer interaction functionalities. Ex: Wishlist, Reviews, User profile. |
| **2** | **Low** | Static or aesthetic information. Ex: FAQ, Blog, Secondary filters. |
| **1** | **Minimal** | Minor visual changes without business logic. Ex: Button colors, spacing. |

## 2. Technical Complexity Matrix (Scale 1-5)

| Level | Technical Risk | Technological Criterion |
| :--- | :--- | :--- |
| **5** | **Very High** | Third-party integrations (Stripe/PayPal), changes in the PostgreSQL DB schema. |
| **4** | **High** | Complex logic in the Backend (FastAPI), concurrency management or caching in Redis. |
| **3** | **Medium** | State logic in the Frontend (Next.js/React), complex form validations. |
| **2** | **Low** | Changes in existing visual components, simple API adjustments. |
| **1** | **Minimal** | Texts, static assets, changes in CSS (Tailwind). |

---

## 3. OWASP Top 10 Heuristics for Risk Classification

These rules allow early identification of security risks during requirements analysis. If a User Story matches any of these criteria, the technical complexity must be increased and the business impact reviewed.

| OWASP Top 10 Matches | Detect if the US mentions or implies | Indicators / Keywords | Adjustment |
| -------------------- | ----------------------------------- | ---------------------- | ------ |
| **A01 Broken Access Control** | Roles, permissions, access between users, private resources, administrative operations, multi-tenancy | administrator, authorized, permissions, access, owner, tenant | Complexity ≥4; Impact ≥4 |
| **A02 Cryptographic Failures** | Passwords, PII, tokens, financial or sensitive data | password, token, encrypt, PII, sensitive data | Complexity ≥4; Impact ≥5 |
| **A03 Injection** | Free inputs, searches, filters, dynamic queries, imports | search, filter, input, query, import, CSV | Complexity ≥4; Impact ≥3 |
| **A04 Insecure Design** | New critical flows, complex rules, incomplete or ambiguous criteria | new flow, discount, coupon, exception, lack of validation | Complexity +1; request clarifications |
| **A05 Security Misconfiguration** | Configuration, feature flags, exposed endpoints, technical integrations | configure, enable, activate, endpoint, CDN, cache | Complexity ≥4 |
| **A06 Vulnerable Components** | New dependencies, SDKs, plugins, or external services | integrate, SDK, library, dependency, plugin | Complexity +1 |
| **A07 Identification & Authentication Failures** | Login, logout, MFA, password recovery, sessions, SSO | login, authenticate, MFA, OTP, session, SSO, password | Complexity ≥5; Impact ≥5 |
| **A08 Software & Data Integrity Failures** | Webhooks, automations, synchronizations, or external data | webhook, synchronize, event, automatic, pipeline | Complexity ≥4 |
| **A09 Logging & Monitoring Failures** | Auditing, traceability, alerts, or investigation | audit, log, monitor, alert, notify | Complexity +1 |
| **A10 SSRF** | URLs entered by users or dynamic consumption of external resources | URL, download, feed, external resource, import | Complexity ≥4 |

### General Rules

- 1 OWASP match → **Complexity +1**.
- 2 or more matches → **Complexity +2** (maximum 5).
- If it involves authentication, authorization, PII, or payments → **Minimum Impact 5**.
- Record an observation when a critical functionality does not describe explicit security controls.

### Complementary OWASP Score

During the requirement analysis, also record:

| OWASP Matches | Classification                |
| ------------- | ----------------------------- |
| 0             | No security indicators        |
| 1             | Low security risk             |
| 2–3           | Medium security risk          |
| 4–5           | High security risk            |
| ≥6            | Critical security risk        |

This score is complementary to the functional and technical risk, allowing prioritization of architecture reviews, threat modeling, and security testing activities.

---

## 4. Impact-Based Prioritization Rules (ROI)

a. **Identify High-Value Business Requirements (ROI):**
    - **Examples:** Checkout, Payments, Authentication, Product Management, Catalog, Search.
    - **Rule:** If a US contains any of these keywords, its **Functional Impact must be a minimum of 5**, regardless of the automatic calculation.
    - **Complexity Adjustment:** If a high-value requirement lacks security specifications, increase technical complexity by **+1 level**.

b. **Exclude Low-Impact Requirements for Prioritization:**
    - **Examples:** "View username", "Show date", "Navigate to another page", "Basic administrative functionalities".
    - **Rule:** If a US involves only data visualization without critical interactions, its **Functional Impact can be less than 5**.
    - **Justification:** These requirements consume fewer development and QA resources, allowing efforts to be focused on real risks.

c. **Prioritize Requirements with OWASP Top 10:**
    - **Rule:** Any US matching one or more OWASP Top 10 categories must have a **high or critical priority**, even if its calculated functional impact is medium.
    - **Action:** Assign **High or Critical Security Risk** and request explicit threat modeling.

---

## 5. Blocking Rules (Red Flags)

- If a US matches **1 or more OWASP Top 10 categories**, technical complexity increases **+1 level**.
- If it matches **2 or more categories**, technical complexity increases **+2 levels** (maximum 5).
- If it involves authentication, authorization, PII, or payments, the impact must be **minimum 5**, regardless of the initial calculation.
- The explicit absence of security controls in a US must be recorded as a risk observation.

**Prioritization Summary:**

- **High Priority:** Critical business requirements + OWASP Top 10.
- **Medium Priority:** Business requirements without OWASP + moderate technical complexity.
- **Low Priority:** Low-value requirements + without OWASP + low complexity.
