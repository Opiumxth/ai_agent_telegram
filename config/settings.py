"""
Configuración central del bot.
Carga las variables de entorno desde .env y el system prompt desde archivo.
Este es el único módulo donde se definen los parámetros, el resto del código
solo importa las constantes de aquí.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "config" / "system_prompt.txt"

# Telegram
TELEGRAM_TOKEN: str = os.environ["TELEGRAM_TOKEN"]

# LLM — compatible con cualquier API estilo OpenAI
LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Cantidad máxima de pares (user/assistant) a mantener en memoria
MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "10"))


def load_system_prompt() -> str:
    """
    Lee el system prompt desde config/system_prompt.txt.
    Este archivo define la personalidad y comportamiento del bot.
    Se puede editar libremente sin tocar código.
    """
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"No se encontró el system prompt en: {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


# Se carga una vez al importar el módulo
SYSTEM_PROMPT: str = load_system_prompt()
