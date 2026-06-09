"""Constantes APA 7 (edición estudiantil / manuscrito)."""

from __future__ import annotations

import re

FONT_NAME = "Times New Roman"
FONT_SIZE_PT = 12
TABLE_FONT_SIZE_PT = 11

MARGIN_INCH = 1.0
FIRST_LINE_INDENT_INCH = 0.5
HANGING_INDENT_INCH = 0.5
BLOCK_QUOTE_INDENT_INCH = 0.5
HEADING_INDENT_INCH = 0.5

BLOCK_QUOTE_MIN_WORDS = 40

REF_SECTION_PATTERN = re.compile(
    r"^(referencias|references|bibliograf[ií]a)\s*$",
    re.IGNORECASE,
)

TABLE_CAPTION_PATTERN = re.compile(
    r"^(tabla|table)\s+(\d+)\.?\s*(.*)$",
    re.IGNORECASE,
)

FIGURE_CAPTION_PATTERN = re.compile(
    r"^(figura|figure)\s+(\d+)\.?\s*(.*)$",
    re.IGNORECASE,
)

HEADING2_PATTERN = re.compile(r"^\d+\.\s+\S")
HEADING3_PATTERN = re.compile(r"^\d+\.\d+\.?\s+\S")
HEADING4_PATTERN = re.compile(r"^[A-ZÁÉÍÓÚÑ][^.]{1,60}\.\s+\S", re.UNICODE)
