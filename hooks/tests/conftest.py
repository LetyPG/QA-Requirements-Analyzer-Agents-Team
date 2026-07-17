"""
Inserts the project root into sys.path 
so that: `from hooks.hook_contract import ...`
and `from hooks.security_language import ...` 
resolve correctly regardless of the directory pytest is invoked from.
"""

import sys
from pathlib import Path

# Project root = two levels up from this conftest (hooks/tests/conftest.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
