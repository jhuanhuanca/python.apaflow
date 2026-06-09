"""
Microservicio FastAPI: formateo APA 7 para documentos .docx.

- Márgenes 2,54 cm, Times New Roman 12, interlineado doble, sangría 0,5".
- Títulos niveles 1–5, referencias con sangría francesa, citas largas en bloque.
- Tablas con tipografía APA; TOC si no existe; paginación configurable.
"""

from __future__ import annotations

import base64

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.apa7 import format_docx_apa7
from app.apa7.engine import report_to_json
from app.apa7.settings import ApaRuntimeSettings
from app.config import get_settings
from app.intelligence.routes import router as intelligence_router
from app.security import require_internal_api_key

load_dotenv()

settings = get_settings()

app = FastAPI(
    title="Tesis Formatter AI — APA7",
    version="2.3.0",
    description="Motor APA 7 para .docx. Sanitiza artefactos IA + settings Pro + informe X-Apa-Report.",
)

if settings['cors_origins']:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings['cors_origins'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

app.include_router(intelligence_router)


@app.on_event('startup')
def validate_production_config() -> None:
    if settings['is_production'] and not settings['api_key']:
        raise RuntimeError(
            'AI_SERVICE_API_KEY es obligatorio cuando AI_ENV=production. '
            'Copia deploy/env/ai.production.env.example → ai-service-python/.env',
        )


@app.get("/health")
def health():
    return {"ok": True, "service": "ai-service-python", "apa_version": "7", "engine": "2.3.0"}


@app.post("/process-document")
async def process_document(
    file: UploadFile = File(...),
    apa_settings: str | None = Form(default=None),
    _: None = Depends(require_internal_api_key),
):
    if not file.filename or not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .docx")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Archivo vacío")

    settings = ApaRuntimeSettings.parse_json(apa_settings)

    try:
        processed, report = format_docx_apa7(raw, apa_settings=settings)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=422, detail=f"No se pudo procesar el DOCX: {exc}") from exc

    report_b64 = base64.b64encode(report_to_json(report).encode("utf-8")).decode("ascii")

    return Response(
        content=processed,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f'attachment; filename="apa7_{file.filename}"',
            "X-Apa-Report": report_b64,
            "X-Apa-Engine": "2.3.0",
        },
    )
