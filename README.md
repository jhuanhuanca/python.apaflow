# AI Service Python — Motor APA 7

Microservicio **FastAPI** que formatea `.docx` según APA 7 (edición estudiantil). Laravel lo invoca en `POST /process-document`.

## Arranque

```bash
cd ai-service-python
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Comprobar: `curl http://127.0.0.1:8001/health`

## Qué formatea (motor v2)

| Regla APA 7 | Implementación |
|-------------|----------------|
| Márgenes 2,54 cm | `set_apa_page_setup` |
| Times New Roman 12 pt | `set_run_font` (ascii + hAnsi) |
| Interlineado doble (cuerpo) | `apply_body_style` |
| Sangría primera línea 0,5" | Cuerpo |
| Alineación izquierda (no justificado) | Cuerpo |
| Títulos 1–5 | Estilos Word + heurísticas |
| Referencias | Sección + sangría francesa |
| Citas largas (≥40 palabras) | Bloque indentado |
| Tablas | TNR 11, interlineado sencillo en celdas |
| Leyendas Tabla/Figura | Negrita + cursiva |
| Índice | Campo TOC si no existe |
| Paginación | Campo PAGE en **encabezado** derecho |
| **Sanitizado IA** | Emojis, caracteres invisibles, tags Unicode, avisos IA |
| **Líneas ChatGPT** | Bordes vacíos, formas horizontales, párrafos `---` / `___` |

## Informe de procesamiento

La respuesta incluye cabecera `X-Apa-Report` (JSON en base64) con conteos y advertencias.

## Tests

```bash
pip install pytest
pytest tests/ -q
```

## Estructura

```
app/
  main.py           # FastAPI
  apa7/
    constants.py    # Reglas y patrones
    classifier.py   # Tipo de párrafo
    ai_sanitizer.py # Limpieza emojis / huellas IA
    formatter.py    # Estilos
    engine.py       # Orquestación + informe
  intelligence/     # Endpoints futuros (IA)
```
