"""
Security Gate
Deterministic, fail-closed validation of file inputs and prompt format.
Runs before any tool is invoked by the orchestrator.
Policy: default-deny. Unknown extensions are BLOCKED, not allowed.
Override: pass allowed_extensions via HookContext.extensions at runtime.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

try:
    import magic  # type: ignore[import-untyped]  # python-magic: optional, graceful degradation
    _MAGIC_AVAILABLE = True
except ImportError:
    _MAGIC_AVAILABLE = False

from hooks.hook_contract import HookContext, HookExtensions, HookResult

# Policy constants
# See README.md  within `hooks` directory for rationale behind each category.

BLOCKED_EXTENSIONS: frozenset[str] = frozenset({
    # Executables & system binaries
    ".exe", ".dll", ".so", ".bat", ".cmd", ".ps1", ".sh",
    # Scripts (including .py — blocked by default; override via extensions)
    ".js", ".vbs", ".py",
    # Binary / packaged
    ".bin", ".apk", ".jar",
    # Office macros
    ".docm", ".xlsm",
})

BLOCKED_MIME_PREFIXES: tuple[str, ...] = (
    "application/x-executable",
    "application/x-sharedlib",
    "application/x-dosexec",
    "application/x-msdownload",
    "application/x-sh",
    "application/x-python",
    "application/java-archive",
    "application/vnd.ms-office",
    "application/zip",
    "application/x-zip",
)

MAX_FILE_SIZE_MB: int = 10
MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024


# Shared trace utility

def _generate_trace_id() -> str:
    """Generate a UUID4 trace ID for audit trail linkage."""
    return str(uuid.uuid4())


# File validation helpers

def _effective_blocked_extensions(extensions: HookExtensions | None) -> frozenset[str]:
    """Return the active deny-list, minus any caller-granted overrides."""
    if extensions and extensions.allowed_extensions:
        overrides = frozenset(ext.lower() for ext in extensions.allowed_extensions)
        return BLOCKED_EXTENSIONS - overrides
    return BLOCKED_EXTENSIONS


def _check_extension(filepath: str, blocked: frozenset[str]) -> str | None:
    """
    Return a block reason if ANY suffix in the file path is blocked.
    Uses pathlib.Path.suffixes to catch compound extensions like .pdf.exe.
    """
    suffixes = [s.lower() for s in Path(filepath).suffixes]
    for suffix in suffixes:
        if suffix in blocked:
            return (
                f"Blocked file extension detected: '{suffix}' in '{Path(filepath).name}'. "
                f"Executable and script files are not permitted as input."
            )
    return None


def _check_mime_type(filepath: str) -> str | None:
    """
    Return a block reason if the MIME type of the file is on the deny-list.
    Falls back gracefully if python-magic is not installed.
    """
    if not _MAGIC_AVAILABLE:
        return None  # Skip MIME check; rely on extension check only

    try:
        p = Path(filepath)
        if not p.exists() or not p.is_file():
            return None  # File does not exist yet — skip MIME check
        mime = magic.from_file(str(p), mime=True)
        if mime and any(mime.startswith(prefix) for prefix in BLOCKED_MIME_PREFIXES):
            return (
                f"Blocked MIME type detected: '{mime}' for file '{p.name}'. "
                f"This file type is not permitted as input."
            )
    except Exception:  # noqa: BLE001,S110 — MIME errors must never crash the hook runtime
        pass  # Graceful degradation: MIME check skipped, extension check still applies
    return None


def _check_file_size(filepath: str, max_bytes: int) -> str | None:
    """Return a block reason if the file exceeds the size limit."""
    try:
        p = Path(filepath)
        if p.exists() and p.is_file():
            size = p.stat().st_size
            if size > max_bytes:
                size_mb = size / (1024 * 1024)
                limit_mb = max_bytes / (1024 * 1024)
                return (
                    f"File '{p.name}' exceeds the maximum allowed size "
                    f"({size_mb:.1f} MB > {limit_mb:.0f} MB limit). "
                    f"Reduce file size or split into smaller inputs."
                )
    except Exception:  # noqa: BLE001,S110 — size-check errors must never crash the hook runtime
        pass
    return None

# Prompt injection guard

def _check_prompt_injection(prompt: str) -> tuple[str | None, dict | None]:
    """
    Validates the prompt against the strict IEEE format regex.
    Returns (block_reason, extracted_components_dict).
    """
    if not prompt or not prompt.strip():
        return "Prompt is empty or missing. A valid IEEE requirement is required.", None

    pattern = re.compile(
        r"^(?:Run\s+)?(RF-[a-zA-Z0-9\-]+):\s*(.*?)\.?\s*(?:US\[|User Story:\s*)(.*?)(?:\])?\.?$",
        re.IGNORECASE | re.DOTALL
    )

    match = pattern.match(prompt.strip())
    if not match:
        return (
            (
                "Prompt Injection Protection: Input does not strictly adhere to the expected IEEE format or contains extraneous content. "
                "Format required: Run RF-[ID]: [action]. US[[user story]] OR User Story: [user story]."
            ),
            None,
        )

    extracted = {
        "rf_id": match.group(1).strip(),
        "action": match.group(2).strip(),
        "user_story": match.group(3).strip(),
    }

    sanitized_prompt = (
        f"{extracted['rf_id']}: {extracted['action']}. "
        f"US[{extracted['user_story']}]."
    )
    extracted["sanitized_prompt"] = sanitized_prompt

    return None, extracted


# Security gate pipeline

def run_security_gate(context: HookContext) -> HookResult | None:
    """
    Execute the security validation sequence (fail-closed).

    Returns a blocking HookResult if any check fails, or None if all pass.
    Sequence:
        1. Extension check (all suffixes, catches compound extensions)
        2. MIME type check  (requires python-magic + libmagic)
        3. File size check  (10 MB default)
    """
    trace_id = _generate_trace_id()
    blocked_ext = _effective_blocked_extensions(
        context.extensions if context.extensions else None
    )
    max_bytes = MAX_FILE_SIZE_BYTES
    if context.runtime_config:
        limit_mb = context.runtime_config.get("max_file_size_mb", MAX_FILE_SIZE_MB)
        max_bytes = int(limit_mb) * 1024 * 1024

    for filepath in context.input_files:
        reason = _check_extension(filepath, blocked_ext)
        if reason:
            return HookResult(
                execute_workflow=False,
                trace_id=trace_id,
                risk_level="high",
                block_reason=reason,
            )

        reason = _check_mime_type(filepath)
        if reason:
            return HookResult(
                execute_workflow=False,
                trace_id=trace_id,
                risk_level="high",
                block_reason=reason,
            )

        reason = _check_file_size(filepath, max_bytes)
        if reason:
            return HookResult(
                execute_workflow=False,
                trace_id=trace_id,
                risk_level="medium",
                block_reason=reason,
            )

    return None  # All checks passed
