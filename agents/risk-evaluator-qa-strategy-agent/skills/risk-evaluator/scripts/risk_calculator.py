import sys
import json

# Spec Reference: reference/reference_risk_standard.md 
# This script receives the already-adjusted values, and it does NOT apply OWASP
# adjustments internally.
IMPACT_WEIGHT: float = 0.7
COMPLEXITY_WEIGHT: float = 0.3
SCALE_MIN: float = 1.0
SCALE_MAX: float = 5.0

# Ordered highest → lowest. Calibrated to the [1.0, 5.0] output range.
# OCP: to add a new severity level, append a tuple here — no logic changes needed.
SEVERITY_THRESHOLDS: list[tuple[float, str]] = [
    (4.5, "Critical"),
    (3.5, "High"),
    (2.5, "Medium"),
    (1.0, "Low"),
]


# ── Private helpers (SRP) ─────────────────────────────────────────────────────

def _validate_input(value: float, name: str) -> None:
    """
    Enforce 1-5 scale boundaries defined in the ShopSwift Risk Standard.
    Raises ValueError with a traceable message if the value is out of range.
    """
    if not (SCALE_MIN <= value <= SCALE_MAX):
        raise ValueError(
            f"'{name}' must be between {SCALE_MIN} and {SCALE_MAX}, got {value}. "
            "See reference/reference_risk_standard.md §1–§2."
        )


def _compute_score(impact: float, complexity: float) -> float:
    """Apply formula: Risk_Score = (Impact × 70%) + (Complexity × 30%)."""
    return round((impact * IMPACT_WEIGHT) + (complexity * COMPLEXITY_WEIGHT), 2)


def _classify(score: float) -> str:
    """
    Map a numeric score to a severity label via the SEVERITY_THRESHOLDS table.
    Iterates highest → lowest so the first match wins.
    """
    for threshold, level in SEVERITY_THRESHOLDS:
        if score >= threshold:
            return level
    return "Low"  # fallback — unreachable when validation passes (score >= 1.0)


# ── Public API ────────────────────────────────────────────────────────────────

def calculate_risk(impact: float, complexity: float) -> dict:
    """
    Compute risk score and severity level for a ShopSwift requirement.

    Args:
        impact:     Business impact score (1-5), per §1 of the Risk Standard.
                    ROI floor rules (§4) must be applied by the calling agent.
        complexity: Technical complexity score (1-5), per §2 of the Risk Standard.
                    OWASP +1/+2 adjustments (3, 5) must be applied by the
                    calling agent BEFORE this call.

    Returns:
        dict with:
            raw_score      (float) rounded to 2 decimal places
            severity_level (str)  Low | Medium | High | Critical
            status         (str)  success
    """
    _validate_input(impact, "impact")
    _validate_input(complexity, "complexity")
    score = _compute_score(impact, complexity)
    level = _classify(score)
    return {"raw_score": score, "severity_level": level, "status": "success"}


# ── CLI entry point ───────────────────────────────────────────────────────────
# Usage: python risk_calculator.py <impact> <complexity>
# Example: python risk_calculator.py 5 4   → {"raw_score": 4.7, "severity_level": "Critical", "status": "success"}

if __name__ == "__main__":
    try:
        imp  = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
        comp = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
        print(json.dumps(calculate_risk(imp, comp)))
    except ValueError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
    except (IndexError, TypeError) as e:
        print(json.dumps({"status": "error", "message": f"Invalid CLI arguments: {e}"}))