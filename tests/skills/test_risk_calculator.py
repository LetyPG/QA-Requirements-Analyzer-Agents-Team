"""
Unit tests for risk_calculator.py
Location: tests/skills/test_risk_calculator.py
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

# Load target script dynamically (handles hyphens in path)
_SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "agents"
    / "risk-evaluator-qa-strategy-agent"
    / "skills"
    / "risk-evaluator"
    / "scripts"
    / "risk_calculator.py"
)

_spec = importlib.util.spec_from_file_location("risk_calculator", _SCRIPT_PATH)
assert _spec is not None and _spec.loader is not None
rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rc)


class TestInputValidation:
    @pytest.mark.parametrize("valid_val", [1.0, 2.5, 3.0, 5.0])
    def test_valid_boundaries_pass(self, valid_val: float) -> None:
        rc._validate_input(valid_val, "impact")

    @pytest.mark.parametrize("invalid_val", [0.9, 0.0, -1.0, 5.1, 10.0])
    def test_invalid_boundaries_raise_value_error(self, invalid_val: float) -> None:
        with pytest.raises(ValueError, match="must be between 1.0 and 5.0"):
            rc._validate_input(invalid_val, "impact")


class TestScoreComputation:
    @pytest.mark.parametrize(
        ("impact", "complexity", "expected_score"),
        [
            (1.0, 1.0, 1.00),
            (5.0, 5.0, 5.00),
            (5.0, 1.0, 3.80),
            (3.0, 4.0, 3.30),
            (4.0, 5.0, 4.30),
        ],
    )
    def test_weighted_formula_precision(
        self, impact: float, complexity: float, expected_score: float
    ) -> None:
        assert rc._compute_score(impact, complexity) == expected_score


class TestSeverityClassification:
    @pytest.mark.parametrize(
        ("score", "expected_severity"),
        [
            (5.00, "Critical"),
            (4.50, "Critical"),
            (4.49, "High"),
            (3.50, "High"),
            (3.49, "Medium"),
            (2.50, "Medium"),
            (2.49, "Low"),
            (1.00, "Low"),
        ],
    )
    def test_threshold_classification(
        self, score: float, expected_severity: str
    ) -> None:
        assert rc._classify(score) == expected_severity


class TestPublicAPIContract:
    def test_calculate_risk_returns_valid_schema(self) -> None:
        res = rc.calculate_risk(5.0, 4.0)
        assert res == {
            "raw_score": 4.70,
            "severity_level": "Critical",
            "status": "success",
        }

    def test_calculate_risk_propagates_validation_error(self) -> None:
        with pytest.raises(ValueError):
            rc.calculate_risk(6.0, 3.0)


class TestCLIIntegration:
    def test_cli_successful_output(self) -> None:
        res = subprocess.run(
            [sys.executable, str(_SCRIPT_PATH), "5", "4"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert res.returncode == 0
        data = json.loads(res.stdout.strip())
        assert data["status"] == "success"
        assert data["raw_score"] == 4.7

    def test_cli_error_output_on_invalid_arg(self) -> None:
        res = subprocess.run(
            [sys.executable, str(_SCRIPT_PATH), "invalid", "3"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert res.returncode == 0
        data = json.loads(res.stdout.strip())
        assert data["status"] == "error"
