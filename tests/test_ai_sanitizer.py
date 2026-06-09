"""Tests del sanitizador anti-artefactos IA."""

from app.apa7.ai_sanitizer import sanitize_plain_text


def test_removes_emojis():
    text = "Introducción ✅ al tema 🎓 con emojis."
    cleaned, stats = sanitize_plain_text(text)
    assert "✅" not in cleaned
    assert "🎓" not in cleaned
    assert stats.emojis_removed >= 2
    assert "Introducción" in cleaned


def test_removes_zero_width_and_tags():
    zwsp = "\u200b"
    tag = "\U000E0020"
    text = f"Hola{zwsp}mundo{tag}."
    cleaned, stats = sanitize_plain_text(text)
    assert "\u200b" not in cleaned
    assert tag not in cleaned
    assert stats.invisible_chars_removed >= 1
    assert stats.unicode_tags_removed >= 1
    assert cleaned == "Holamundo."


def test_removes_decorative_symbols():
    text = "Resultado correcto ✔ y error ✘"
    cleaned, stats = sanitize_plain_text(text)
    assert "✔" not in cleaned
    assert "✘" not in cleaned
    assert stats.total_chars_removed >= 2


def test_normalizes_special_spaces():
    text = "Palabra\u00a0con\u2009espacio"
    cleaned, _ = sanitize_plain_text(text)
    assert "\u00a0" not in cleaned
    assert "\u2009" not in cleaned
