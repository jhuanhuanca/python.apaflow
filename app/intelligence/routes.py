"""
Endpoints preparados para orquestación desde Laravel (APA/Vancouver/custom,
estructura, reordenado, citas, índice). Implementación completa vía colas/workers.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/v1/intelligence", tags=["intelligence"])


@router.post("/format")
async def format_document():
    """Alineación con plantillas (APA, Vancouver, custom JSON desde Laravel)."""
    return {"status": "planned", "detail": "Recibirá plantilla_id + docx; respuesta procesada."}


@router.post("/structure")
async def build_structure():
    """Generación de estructura e índice tentativo (TOC / niveles)."""
    return {"status": "planned", "detail": "Outline + secciones sugeridas."}


@router.post("/reorder")
async def reorder_content():
    """Reordenar bloques de contenido según reglas o sugerencias IA."""
    return {"status": "planned", "detail": "Mapa de párrafos → nuevo orden."}


@router.post("/citations")
async def citations_and_references():
    """Inserción / normalización de citas y lista de referencias."""
    return {"status": "planned", "detail": "Estilo según plantilla."}


@router.post("/index")
async def tentative_index():
    """Índice automático tentativo (entradas + números de página estimados)."""
    return {"status": "planned", "detail": "Integración con campos Word TOC."}
