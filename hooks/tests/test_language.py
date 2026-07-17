from __future__ import annotations

import uuid
from unittest.mock import MagicMock, patch

import pytest

from hooks.hook_contract import HookContext
from hooks import security_language as sl

# ---------------------------------------------------------------------------
# Detect whether lingua is available in the current Python interpreter.
# Live detection tests require the real library; they are skipped (not failed)
# when running under an interpreter that has no lingua installed (e.g. the
# system Python or a venv where lingua was never added).
# Run these tests with:  hooks/.venv/bin/python -m pytest hooks/tests/ -v
# ---------------------------------------------------------------------------

try:
    # pyrefly: ignore [missing-import]
    import lingua as _lingua_check  # noqa: F401
    _LINGUA_INSTALLED = True
except ImportError:
    _LINGUA_INSTALLED = False

_NEEDS_LINGUA = pytest.mark.skipif(
    not _LINGUA_INSTALLED,
    reason=(
        "lingua-language-detector is not installed in this Python interpreter. "
        "Run tests with: hooks/.venv/bin/python -m pytest hooks/tests/ -v"
    ),
)


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _make_context(prompt: str = "", files: list[str] | None = None) -> HookContext:
    return HookContext(user_prompt=prompt, input_files=files or [])


# ===========================================================================
# 1. Language Detection — _detect_language
# ===========================================================================

class TestDetectLanguage:

    @_NEEDS_LINGUA
    def test_spanish_detected(self):
        prompt = (
            "El sistema debe permitir a los usuarios registrarse con su correo "
            "electrónico y contraseña para acceder a la plataforma."
        )
        lang, confidence = sl._detect_language(prompt)
        assert lang == "Spanish", f"Expected Spanish, got {lang}"
        assert confidence >= sl.CONFIDENCE_THRESHOLD

    @_NEEDS_LINGUA
    def test_english_detected(self):
        prompt = (
            "The system must allow users to register with their email address "
            "and password in order to access the platform features."
        )
        lang, confidence = sl._detect_language(prompt)
        assert lang == "English", f"Expected English, got {lang}"
        assert confidence >= sl.CONFIDENCE_THRESHOLD

    @_NEEDS_LINGUA
    def test_french_detected(self):
        prompt = (
            "Le système doit permettre aux utilisateurs de s'inscrire avec "
            "leur adresse e-mail et leur mot de passe pour accéder à la plateforme."
        )
        lang, confidence = sl._detect_language(prompt)
        assert lang == "French", f"Expected French, got {lang}"
        assert confidence >= sl.CONFIDENCE_THRESHOLD

    @_NEEDS_LINGUA
    def test_portuguese_detected(self):
        prompt = (
            "O sistema deve permitir que os usuários se registrem com seu "
            "endereço de e-mail e senha para acessar a plataforma."
        )
        lang, confidence = sl._detect_language(prompt)
        assert lang == "Portuguese", f"Expected Portuguese, got {lang}"
        assert confidence >= sl.CONFIDENCE_THRESHOLD

    @_NEEDS_LINGUA
    def test_german_detected(self):
        prompt = (
            "Das System muss es Benutzern ermöglichen, sich mit ihrer "
            "E-Mail-Adresse und ihrem Passwort zu registrieren."
        )
        lang, confidence = sl._detect_language(prompt)
        assert lang == "German", f"Expected German, got {lang}"
        assert confidence >= sl.CONFIDENCE_THRESHOLD

    @_NEEDS_LINGUA
    def test_italian_detected(self):
        prompt = (
            "Il sistema deve consentire agli utenti di registrarsi con il "
            "proprio indirizzo e-mail e password per accedere alla piattaforma."
        )
        lang, confidence = sl._detect_language(prompt)
        assert lang == "Italian", f"Expected Italian, got {lang}"
        assert confidence >= sl.CONFIDENCE_THRESHOLD

    def test_empty_prompt_falls_back_to_english(self):
        lang, confidence = sl._detect_language("")
        assert lang == "English"
        assert confidence == 0.0

    def test_whitespace_only_falls_back_to_english(self):
        lang, confidence = sl._detect_language("   ")
        assert lang == "English"

    def test_confidence_below_threshold_falls_back_and_preserves_score(self):
        """
        When the detector returns a confidence score below 0.75, the hook
        must fall back to English AND preserve the raw score for diagnostics.
        Uses create=True on both Language and LanguageDetectorBuilder so the
        test is fully self-contained and works regardless of whether lingua
        was successfully imported at module load time.
        """
        mock_result = MagicMock()
        mock_result.name = "SPANISH"

        mock_cv = MagicMock()
        mock_cv.language = mock_result
        mock_cv.value = 0.50  # below 0.75 threshold

        mock_detector = MagicMock()
        mock_detector.detect_language_of.return_value = mock_result
        mock_detector.compute_language_confidence_values.return_value = [mock_cv]

        with patch("hooks.security_language._LINGUA_AVAILABLE", True), \
             patch("hooks.security_language.Language", create=True), \
             patch("hooks.security_language.LanguageDetectorBuilder",
                   create=True) as MockBuilder:
            MockBuilder.from_languages.return_value \
                .with_minimum_relative_distance.return_value \
                .build.return_value = mock_detector
            lang, confidence = sl._detect_language("hola mundo")

        assert lang == "English"   # Fell back due to low confidence
        assert confidence == 0.50  # Raw score preserved for diagnostics


# ===========================================================================
# 2. Language Result Builder — build_language_result
# ===========================================================================

class TestBuildLanguageResult:

    def test_returns_execute_workflow_true(self):
        ctx = _make_context(prompt="The system must allow login.")
        result = sl.build_language_result(ctx, trace_id="test-trace")
        assert result.execute_workflow is True

    def test_language_rule_is_populated_and_non_empty(self):
        ctx = _make_context(
            prompt="El sistema debe permitir el inicio de sesión de los usuarios."
        )
        result = sl.build_language_result(ctx, trace_id="t1")
        assert result.language_rule is not None
        assert len(result.language_rule) > 0

    def test_sanitized_context_contains_prompt_and_files(self):
        ctx = _make_context(prompt="hello", files=["req.md"])
        result = sl.build_language_result(ctx, trace_id="t2")
        assert result.sanitized_context is not None
        assert result.sanitized_context["user_prompt"] == "hello"
        assert result.sanitized_context["input_files"] == ["req.md"]

    def test_trace_id_is_preserved(self):
        ctx = _make_context()
        trace = str(uuid.uuid4())
        result = sl.build_language_result(ctx, trace_id=trace)
        assert result.trace_id == trace

    def test_spanish_rule_references_spanish(self):
        ctx = _make_context(
            prompt=(
                "El sistema debe permitir registrar clientes con nombre completo "
                "y correo electrónico válido en el sistema de gestión."
            )
        )
        result = sl.build_language_result(ctx, trace_id="t3")
        if result.language == "Spanish":
            assert "Spanish" in result.language_rule
