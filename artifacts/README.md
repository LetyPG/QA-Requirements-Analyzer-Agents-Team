# System Artifacts & Quality Gate Reports

This directory is dedicated to store **Internal system validation reports, process metrics, and failure logs** it is used exclusibely by the `orchestrator-agent` as a quality gate skill `artifact-validator-fixing-loop` to track system evaluation metadata, quality check reults and execution failure audits. 

---

## Directory Structure

```text
artifacts/
├── validation-report/   # Internal schema & completeness validation results
└── logs/                # System execution failure logs & workflow diagnostics
```

---

## Subfolder Overview

### 1. `validation-report/`
Contains the Quality Gate audit reports created during output validation:
- **`artifact_validation_success_report_{RF_ID}_{timestamp}.json`**: Generated when sub-agent outputs meet all schema, content, and security rules.
- **`artifact_validation_failure_report_{RF_ID}_{timestamp}.json`**: Generated when validation fails or content gaps are identified.

### 2. `logs/`
Contains workflow execution diagnostics used during error recovery and fixing loop control:
- **`failure_log_workflow_{RF_ID}_{timestamp}.json`**: Records resource usage (token consumption, processing duration, RAM usage) and error classification details to prevent infinite retries.

---

## Guidance for Users

- **Troubleshooting:** If a requirement analysis process finishes with a failure status, check `artifacts/validation-report/` to view the specific validation errors or missing sections.
- **System Governance:** These files are managed automatically by the Orchestrator Agent to ensure system compliance and auditability.
