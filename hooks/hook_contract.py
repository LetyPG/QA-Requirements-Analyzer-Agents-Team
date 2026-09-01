"""
Stable Hook Interface Contract
Single source of truth for the interface between any hook and any orchestrator.
This file defines ONLY data structures, no logic, no side-effects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

# ---------------------------------------------------------------------------
# Optional extensions is a backward-compatible additions to HookContext.
# New fields can be added here without breaking existing hook implementations.
# ---------------------------------------------------------------------------

@dataclass
class HookExtensions:
    # Optional policy overrides passed from agent.settings.json at runtime.

    allowed_extensions: list[str] = field(default_factory=list)
    blocked_patterns: list[str] = field(default_factory=list)

# ---------------------------------------------------------------------------
# HookContext is a stable input structure.
# The orchestrator builds this and passes it to every hook.
# ---------------------------------------------------------------------------

@dataclass
class HookContext:
    # Input to every hook invocation.
    user_prompt: str
    input_files: list[str]
    runtime_config: dict | None = None
    extensions: HookExtensions | None = None


# ---------------------------------------------------------------------------
# HookResult is stable output structure.
# Every hook MUST return a value that matches this structure.
# The orchestrator only needs to read execute_workflow to decide whether
# to proceed; all other fields are optional enrichment.
# ---------------------------------------------------------------------------

@dataclass
class HookResult:
   # --- Master gate (always required) ---
    execute_workflow: bool
    trace_id: str

    # --- Block metadata (when execute_workflow is False) ---
    risk_level: Literal["low", "medium", "high"] | None = None
    block_reason: str | None = None

    # --- Language enrichment (when execute_workflow is True) ---
    language: str | None = None
    confidence: float | None = None
    language_rule: str | None = None
    sanitized_context: dict | None = None

    def to_dict(self) -> dict:
        """Serialise to a plain dict for JSON emission to stdout."""
        return {
            "execute_workflow": self.execute_workflow,
            "trace_id": self.trace_id,
            "risk_level": self.risk_level,
            "block_reason": self.block_reason,
            "language": self.language,
            "confidence": self.confidence,
            "language_rule": self.language_rule,
            "sanitized_context": self.sanitized_context,
        }
