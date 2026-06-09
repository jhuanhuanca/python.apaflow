"""Resolución de configuración APA personalizada (Pro) vs defaults."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from app.apa7.constants import FONT_NAME, FONT_SIZE_PT, MARGIN_INCH


@dataclass
class ApaRuntimeSettings:
    margin_top: float = MARGIN_INCH
    margin_bottom: float = MARGIN_INCH
    margin_left: float = MARGIN_INCH
    margin_right: float = MARGIN_INCH
    line_spacing: float = 2.0
    font_name: str = FONT_NAME
    font_size_pt: int = FONT_SIZE_PT
    page_number_position: str = "header_top_right"
    title_case: str = "title"
    heading_levels: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: dict[str, Any] | None) -> ApaRuntimeSettings:
        if not payload:
            return cls()

        margins = payload.get("margins_in") or {}
        return cls(
            margin_top=float(margins.get("top", MARGIN_INCH)),
            margin_bottom=float(margins.get("bottom", MARGIN_INCH)),
            margin_left=float(margins.get("left", MARGIN_INCH)),
            margin_right=float(margins.get("right", MARGIN_INCH)),
            line_spacing=float(payload.get("line_spacing", 2.0)),
            font_name=str(payload.get("font", FONT_NAME)),
            font_size_pt=int(payload.get("font_size_pt", FONT_SIZE_PT)),
            page_number_position=str(payload.get("page_number_position", "header_top_right")),
            title_case=str(payload.get("title_case", "title")),
            heading_levels=dict(payload.get("heading_levels") or {}),
        )

    @classmethod
    def parse_json(cls, raw: str | None) -> ApaRuntimeSettings:
        if not raw or not raw.strip():
            return cls()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return cls()
        if not isinstance(data, dict):
            return cls()
        return cls.from_payload(data)

    def to_dict(self) -> dict[str, Any]:
        return {
            "margins_in": {
                "top": self.margin_top,
                "bottom": self.margin_bottom,
                "left": self.margin_left,
                "right": self.margin_right,
            },
            "line_spacing": self.line_spacing,
            "font": self.font_name,
            "font_size_pt": self.font_size_pt,
            "page_number_position": self.page_number_position,
            "title_case": self.title_case,
            "heading_levels": self.heading_levels,
        }
