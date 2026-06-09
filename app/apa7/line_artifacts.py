"""
Elimina líneas horizontales decorativas típicas de exportaciones ChatGPT / Copilot.

Patrones habituales en OOXML:
- Párrafos vacíos con w:pBdr (borde inferior/superior)
- Formas w:drawing (líneas vectoriales finas y anchas)
- Párrafos solo con guiones/underscores (---, ___, ───)
"""

from __future__ import annotations

import re
from typing import Iterator

from docx.document import Document
from docx.oxml.ns import qn
from docx.table import Table

from app.apa7.ai_sanitizer import SanitizeStats

_SEPARATOR_TEXT_RE = re.compile(
    r"^[\s\-–—_=~·•─━│┃┄┅┈┉╌╍╴╶╸▀▄█▁▂▃▅▆▇]{2,}$",
    re.UNICODE,
)

_MAX_LINE_HEIGHT_EMU = 80000
_MIN_LINE_WIDTH_EMU = 200000


def _iter_paragraph_elements(container) -> Iterator:
    if isinstance(container, Document):
        parent_el = container.element.body
    elif isinstance(container, Table):
        parent_el = container._tbl
    else:
        parent_el = container._element

    for p in parent_el.iter(qn("w:p")):
        yield p


def _paragraph_visible_text(p_el) -> str:
    parts: list[str] = []
    for node in p_el.iter(qn("w:t")):
        if node.text:
            parts.append(node.text)
    return "".join(parts).strip()


def _paragraph_has_border(p_el) -> bool:
    p_pr = p_el.find(qn("w:pPr"))
    if p_pr is None:
        return False
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        return False
    for edge in ("top", "bottom", "left", "right", "between"):
        if p_bdr.find(qn(f"w:{edge}")) is not None:
            return True
    return False


def _remove_paragraph_border(p_el) -> bool:
    p_pr = p_el.find(qn("w:pPr"))
    if p_pr is None:
        return False
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        return False
    p_pr.remove(p_bdr)
    return True


def _paragraph_has_drawings(p_el) -> bool:
    return bool(p_el.findall(".//" + qn("w:drawing")) or p_el.findall(".//" + qn("w:pict")))


def _drawing_is_horizontal_line(drawing_el) -> bool:
    for prst in drawing_el.iter(qn("a:prstGeom")):
        preset = (prst.get("prst") or "").lower()
        if preset in {"line", "straightconnector1", "bentconnector2", "bentconnector3"}:
            return True

    for tag in (qn("wp:inline"), qn("wp:anchor")):
        for container in drawing_el.findall(f".//{tag}"):
            extent = container.find(qn("wp:extent"))
            if extent is None:
                continue
            try:
                cx = int(extent.get("cx", 0))
                cy = int(extent.get("cy", 0))
            except (TypeError, ValueError):
                continue
            if cy <= _MAX_LINE_HEIGHT_EMU and cx >= _MIN_LINE_WIDTH_EMU:
                return True
    return False


def _remove_horizontal_drawings(p_el, stats: SanitizeStats) -> None:
    for drawing in list(p_el.findall(".//" + qn("w:drawing"))):
        if not _drawing_is_horizontal_line(drawing):
            continue
        parent = drawing.getparent()
        if parent is not None:
            parent.remove(drawing)
            stats.ai_horizontal_lines_removed += 1

    for pict in list(p_el.findall(".//" + qn("w:pict"))):
        parent = pict.getparent()
        if parent is not None:
            parent.remove(pict)
            stats.ai_horizontal_lines_removed += 1


def _should_delete_paragraph(p_el) -> bool:
    text = _paragraph_visible_text(p_el)

    if text and _SEPARATOR_TEXT_RE.match(text):
        return True

    if not text and _paragraph_has_border(p_el):
        return True

    if not text and _paragraph_has_drawings(p_el):
        return True

    if len(text) <= 1 and _paragraph_has_border(p_el):
        return True

    return False


def _clean_single_paragraph(p_el, stats: SanitizeStats) -> None:
    if _should_delete_paragraph(p_el):
        parent = p_el.getparent()
        if parent is not None:
            parent.remove(p_el)
            stats.decorative_paragraphs_removed += 1
        return

    text = _paragraph_visible_text(p_el)
    _remove_horizontal_drawings(p_el, stats)

    if not _paragraph_visible_text(p_el) and _paragraph_has_border(p_el):
        parent = p_el.getparent()
        if parent is not None:
            parent.remove(p_el)
            stats.decorative_paragraphs_removed += 1
        return

    if text and _remove_paragraph_border(p_el):
        stats.paragraph_borders_removed += 1


def _clean_container_paragraphs(container, stats: SanitizeStats) -> None:
    for _ in range(3):
        if isinstance(container, Document):
            current = list(_iter_paragraph_elements(container))
        elif isinstance(container, Table):
            current = list(_iter_paragraph_elements(container))
        else:
            current = list(container._element.iter(qn("w:p")))
        if not current:
            break
        before = len(current)
        for p_el in list(current):
            _clean_single_paragraph(p_el, stats)
        if isinstance(container, Document):
            after = len(list(_iter_paragraph_elements(container)))
        elif isinstance(container, Table):
            after = len(list(_iter_paragraph_elements(container)))
        else:
            after = len(list(container._element.iter(qn("w:p"))))
        if after >= before:
            break


def remove_chatgpt_horizontal_lines(doc: Document, stats: SanitizeStats) -> None:
    """Elimina líneas/separadores decorativos de IA en todo el documento."""
    _clean_container_paragraphs(doc, stats)

    for table in doc.tables:
        _clean_container_paragraphs(table, stats)

    for section in doc.sections:
        for header_footer in (section.header, section.footer):
            _clean_container_paragraphs(header_footer, stats)
