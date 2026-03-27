# AI_Agent_Basic — CLAUDE.md

## Normas del Código y Documentación

- **Cero Emojis:** Está estrictamente prohibido el uso de emojis en cualquier parte de este proyecto. Esto incluye el código fuente, comentarios, archivos markdown, prompts del sistema y logs (salidas de consola).

## Propósito del proyecto

Bot de Telegram de nivel básico para el curso de Agentes de IA del IEEE Computer Society PUCP.
Conecta Telegram con un LLM (compatible con la API de OpenAI) para mantener conversaciones con memoria por chat.

## Estructura del proyecto

```
AI_Agent_Basic/
├── config/
│   ├── system_prompt.txt   ← EDITAR AQUÍ para cambiar personalidad del bot
│   └── settings.py         ← Carga .env y system_prompt.txt
├── src/
│   ├── llm_client.py       ← Llama al LLM (async, OpenAI-compatible)
│   └── handlers.py         ← Handlers de Telegram (/start, /help, /reset, mensajes)
├── docs/
│   ├── CLAUDE.md           ← Este archivo (contexto para IA)
│   └── README.md           ← Guía para desarrolladores
├── main.py                 ← Punto de entrada
├── requirements.txt
├── .env.example            ← Template de variables de entorno
└── .env                    ← Secretos reales (NO commitear)
```

## Variables de entorno clave

| Variable | Descripción |
|---|---|
| `TELEGRAM_TOKEN` | Token del bot de Telegram (BotFather) |
| `LLM_API_KEY` | API Key del proveedor LLM |
| `LLM_BASE_URL` | URL base de la API (OpenAI-compatible) |
| `LLM_MODEL` | Nombre del modelo a usar |
| `MAX_HISTORY` | Máximo de mensajes en memoria por chat |

## Flujo de datos

```
Usuario (Telegram) → handlers.py → llm_client.py → LLM API → handlers.py → Usuario
```

## Cómo cambiar la personalidad del bot

1. Editar `config/system_prompt.txt` (texto plano, sin código)
2. Guardar el archivo
3. Reiniciar el bot (`python main.py`)

## Patrones usados

- **python-telegram-bot v21** con `asyncio` nativo
- **Memoria conversacional** en memoria (dict por `chat_id`)
- **LLM abstraction** en `llm_client.py` — swappable sin tocar handlers
- **Settings centralizados** en `config/settings.py`

## Relación con AI_Agent_Intermediate

El nivel intermedio extiende este agente con:
- RAG (Retrieval Augmented Generation)
- Herramientas/Tools calling
- Persistencia de memoria (base de datos)
- Webhooks en lugar de polling
