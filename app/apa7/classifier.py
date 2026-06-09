"""Clasificación de párrafos según APA 7 (estilos Word + heurísticas)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from app.apa7.constants import (
    BLOCK_QUOTE_MIN_WORDS,
    FIGURE_CAPTION_PATTERN,
    HEADING2_PATTERN,
    HEADING3_PATTERN,
    HEADING4_PATTERN,
    REF_SECTION_PATTERN,
    TABLE_CAPTION_PATTERN,
)

ParagraphKind = Literal[
    "empty",
    "body",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "refs_heading",
    "reference_entry",
    "block_quote",
    "table_caption",
    "figure_caption",
]


def _letters(text: str) -> str:
    return "".join(c for c in text if c.isalpha())


def _word_count(text: str) -> int:
    return len(re.findall(r"\w+", text, flags=re.UNICODE))


def _style_heading_level(style_name: str | None) -> int | None:
    if not style_name:
        return None
    lowered = style_name.lower()
    for level in range(1, 6):
        markers = (
            f"heading {level}",
            f"título {level}",
            f"titulo {level}",
            f"encabezado {level}",
        )
        if any(m in lowered for m in markers):
            return level
    if "title" in lowered and "subtitle" not in lowered:
        return 1
    if "toc" in lowered or "índice" in lowered or "indice" in lowered:
        return 1
    return None


def _is_all_caps_heading(text: str) -> bool:
    letters = _letters(text)
    return len(letters) > 4 and letters.isupper()


def _is_block_quote(text: str, style_name: str | None) -> bool:
    if style_name and "quote" in style_name.lower():
        return True
    words = _word_count(text)
    if words < BLOCK_QUOTE_MIN_WORDS:
        return False
    stripped = text.strip()
    return stripped.startswith(('"', "«", "“")) or stripped.startswith("-" * 3)


@dataclass
class ParagraphClassifier:
    """Mantiene estado de sección (p. ej. lista de referencias)."""

    in_references: bool = False

    def classify(self, text: str, style_name: str | None = None) -> ParagraphKind:
        t = (text or "").strip()
        if not t:
            return "empty"

        if REF_SECTION_PATTERN.match(t):
            self.in_references = True
            return "refs_heading"

        if self.in_references:
            return "reference_entry"

        style_level = _style_heading_level(style_name)
        if style_level is not None:
            return f"h{style_level}"  # type: ignore[return-value]

        if TABLE_CAPTION_PATTERN.match(t):
            return "table_caption"
        if FIGURE_CAPTION_PATTERN.match(t):
            return "figure_caption"

        if _is_block_quote(t, style_name):
            return "block_quote"

        if HEADING3_PATTERN.match(t):
            return "h3"
        if HEADING2_PATTERN.match(t):
            return "h2"
        if HEADING4_PATTERN.match(t):
            return "h4"
        if _is_all_caps_heading(t):
            return "h1"

        return "body"
