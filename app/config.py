"""Configuración de entorno del microservicio APA."""

from __future__ import annotations

import os
from functools import lru_cache


@lru_cache
def get_settings() -> dict:
    environment = os.getenv('AI_ENV', 'local').strip().lower()
    return {
        'environment': environment,
        'host': os.getenv('AI_HOST', '127.0.0.1'),
        'port': int(os.getenv('AI_PORT', '8001')),
        'workers': int(os.getenv('AI_WORKERS', '2')),
        'api_key': os.getenv('AI_SERVICE_API_KEY', '').strip(),
        'cors_origins': [
            origin.strip()
            for origin in os.getenv('AI_CORS_ORIGINS', '').split(',')
            if origin.strip()
        ],
        'is_production': environment == 'production',
    }
