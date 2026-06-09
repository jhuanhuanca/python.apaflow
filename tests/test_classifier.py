"""Tests del clasificador APA 7."""

from app.apa7.classifier import ParagraphClassifier


def test_references_section_flow():
    clf = ParagraphClassifier()
    assert clf.classify("Referencias") == "refs_heading"
    assert clf.classify("García, J. (2021). Título del libro. Editorial.") == "reference_entry"
    assert clf.classify("Otra referencia.") == "reference_entry"


def test_heading_levels():
    clf = ParagraphClassifier()
    assert clf.classify("INTRODUCCIÓN") == "h1"
    assert clf.classify("1. Marco teórico") == "h2"
    assert clf.classify("1.1 Antecedentes") == "h3"


def test_block_quote():
    clf = ParagraphClassifier()
    long_text = "palabra " * 45
    assert clf.classify(f'"{long_text.strip()}"') == "block_quote"


def test_table_caption():
    clf = ParagraphClassifier()
    assert clf.classify("Tabla 1. Resultados del análisis") == "table_caption"
