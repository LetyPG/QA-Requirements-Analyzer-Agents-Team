"""
PreToolUse Hook — Entrypoint

Orchestrates the two-phase validation pipeline before any tool is used:
    Phase 1  — Security Gate      (fail-closed): blocks unsafe files and injected prompts.
    Phase 2  — Language Detector  (enrichment):  injects a language rule into the context.

All logic lives in dedicated modules:
    hooks/security_gate.py      — file, MIME, size, and prompt-injection checks
    hooks/language_detector.py  — offline language detection via lingua
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from hooks.hook_contract import HookContext, HookResult
from hooks.language_detector import build_language_result
from hooks.security_gate import (
    _check_prompt_injection,
    _generate_trace_id,
    run_security_gate,
)

# stdin parsing helpers

def _resolve_file_paths(tool_input: dict) -> list[str]:
    """
    Extract file paths referenced in the tool's input arguments.

    Scans all string values in the tool_input dict for path-like strings
    (values starting with '/' or './' or containing a file extension).
    """
    paths: list[str] = []
    for value in tool_input.values():
        if isinstance(value, str):
            candidate = value.strip()
            if (
                candidate.startswith(("/", "./", "../"))
                or (len(candidate) < 512 and "." in Path(candidate).name)
            ):
                paths.append(candidate)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    paths.append(item.strip())
    return paths


def _parse_stdin() -> tuple[dict, list[str]]:
    """
    Read and parse the JSON payload from stdin (Claude PreToolUse protocol).

    The runtime passes a JSON object with at minimum:
        { "tool_name": "...", "tool_input": { ... } }

    Returns:
        (raw_payload, list_of_file_paths)
    """
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return ({}, [])
        payload = json.loads(raw)
        tool_input = payload.get("tool_input", {})
        file_paths = _resolve_file_paths(tool_input)
        return (payload, file_paths)
    except json.JSONDecodeError:
        return ({}, [])


def _extract_user_prompt(payload: dict) -> str:
    """
    Extract the user-facing text for language detection.

    Prefers the 'prompt' or 'query' keys in tool_input; falls back to
    searching for any string value longer than 20 chars.
    """
    tool_input = payload.get("tool_input", {})
    for key in ("prompt", "query", "content", "text", "user_prompt"):
        val = tool_input.get(key, "")
        if isinstance(val, str) and len(val.strip()) > 10:
            return val.strip()

    candidates = [
        v for v in tool_input.values()
        if isinstance(v, str) and len(v.strip()) > 20
    ]
    if candidates:
        return max(candidates, key=len)

    return ""


# Entrypoint
def main() -> None:
    """
    PreToolUse hook entrypoint.

    Reads tool input from stdin, runs security gate and language detection,
    and emits a HookResult as JSON to stdout.

    Exit code is always 0 — a non-zero exit would crash the agent runtime.
    """
    payload, input_files = _parse_stdin()
    user_prompt = _extract_user_prompt(payload)

    context = HookContext(
        user_prompt=user_prompt,
        input_files=input_files,
    )

    trace_id = _generate_trace_id()

    # --- Phase 1: Security Gate (fail-closed) ---
    block_result = run_security_gate(context)
    if block_result is not None:
        block_result.trace_id = trace_id
        print(json.dumps(block_result.to_dict(), ensure_ascii=False))
        sys.exit(0)

    # --- Phase 1.5: Prompt Injection Gate (fail-closed) ---
    prompt_reason, extracted = _check_prompt_injection(user_prompt)
    if prompt_reason:
        prompt_block = HookResult(
            execute_workflow=False,
            trace_id=trace_id,
            risk_level="high",
            block_reason=prompt_reason,
        )
        print(json.dumps(prompt_block.to_dict(), ensure_ascii=False))
        sys.exit(0)

    # Inject sanitized prompt back into context for language detection
    if extracted and "sanitized_prompt" in extracted:
        context.user_prompt = extracted["sanitized_prompt"]

    # --- Phase 2: Language Detection (enrichment) ---
    allow_result = build_language_result(context, trace_id)
    print(json.dumps(allow_result.to_dict(), ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()