"""
Inserts the project root into sys.path
so that: `from hooks.hook_contract import ...`
and `from hooks.security_language import ...`
resolve correctly regardless of the directory pytest is invoked from.
"""

import sys
from pathlib import Path

# pyrefly: ignore [missing-import]
import pytest

# Project root = two levels up from this conftest (tests/hooks/conftest.py)
# tests/hooks/conftest.py → tests/hooks/ (0) → tests/ (1) → repo root (2)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers to avoid PytestUnknownMarkWarning."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration-level (invokes hook as a subprocess).",
    )
