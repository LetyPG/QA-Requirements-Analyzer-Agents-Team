"""
Stable Hook Interface Contract
Single source of truth for the interface between any hook and any orchestrator.
This file defines ONLY data structures, no logic, no side-effects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional


# ---------------------------------------------------------------------------
# Optional extensions is a backward-compatible additions to HookContext.
# New fields can be added here without breaking existing hook implementations.
# ---------------------------------------------------------------------------

@dataclass
class HookExtensions:
    # Optional policy overrides passed from agent.settings.json at runtime.

    allowed_extensions: List[str] = field(default_factory=list)
    blocked_patterns: List[str] = field(default_factory=list)

# ---------------------------------------------------------------------------
# HookContext is a stable input structure.
# The orchestrator builds this and passes it to every hook.
# ---------------------------------------------------------------------------

@dataclass
class HookContext:
    # Input to every hook invocation.
    user_prompt: str
    input_files: List[str]
    runtime_config: Optional[dict] = None
    extensions: Optional[HookExtensions] = None


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
    risk_level: Optional[Literal["low", "medium", "high"]] = None
    block_reason: Optional[str] = None

    # --- Language enrichment (when execute_workflow is True) ---
    language: Optional[str] = None
    confidence: Optional[float] = None
    language_rule: Optional[str] = None
    sanitized_context: Optional[dict] = None

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
