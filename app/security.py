"""Autenticación interna para endpoints de procesamiento."""

from __future__ import annotations

from fastapi import Header, HTTPException

from app.config import get_settings


def require_internal_api_key(
    x_internal_api_key: str | None = Header(default=None, alias='X-Internal-Api-Key'),
) -> None:
    expected = get_settings()['api_key']
    if not expected:
        return
    if not x_internal_api_key or x_internal_api_key != expected:
        raise HTTPException(status_code=401, detail='API key inválida')
