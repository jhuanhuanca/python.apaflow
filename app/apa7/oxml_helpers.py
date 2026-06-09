"""Utilidades OOXML (campos Word, fuentes)."""

from __future__ import annotations

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

from app.apa7.constants import FONT_NAME, FONT_SIZE_PT


def set_run_font(
    run,
    *,
    bold: bool | None = None,
    italic: bool | None = None,
    size_pt: int = FONT_SIZE_PT,
    font_name: str = FONT_NAME,
) -> None:
    """Times New Roman (o fuente personalizada) en ascii/hAnsi/cs/eastAsia."""
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic

    r_pr = run._element.get_or_add_rPr()
    for existing in r_pr.findall(qn("w:rFonts")):
        r_pr.remove(existing)
    r_fonts = OxmlElement("w:rFonts")
    r_fonts.set(qn("w:ascii"), font_name)
    r_fonts.set(qn("w:hAnsi"), font_name)
    r_fonts.set(qn("w:cs"), font_name)
    r_fonts.set(qn("w:eastAsia"), font_name)
    r_pr.append(r_fonts)


def clear_paragraph_runs(paragraph) -> None:
    for run in list(paragraph.runs):
        run._element.getparent().remove(run._element)


def add_field_run(paragraph, instr: str, *, placeholder: str = "1") -> None:
    """Inserta un campo Word (PAGE, TOC, etc.)."""
    run = paragraph.add_run()
    r = run._r

    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")

    instr_el = OxmlElement("w:instrText")
    instr_el.set(qn("xml:space"), "preserve")
    instr_el.text = instr

    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")

    text_el = OxmlElement("w:t")
    text_el.text = placeholder

    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")

    r.append(fld_begin)
    r.append(instr_el)
    r.append(fld_sep)
    r.append(text_el)
    r.append(fld_end)


def document_has_toc_field(doc) -> bool:
    body = doc.element.body
    for instr in body.iter(qn("w:instrText")):
        if instr.text and "TOC" in instr.text.upper():
            return True
    return False
