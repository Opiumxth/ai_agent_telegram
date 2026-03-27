"""
Cliente para llamar al LLM.
Usa el SDK de OpenAI, que es compatible con cualquier proveedor
que implemente la misma interfaz (Groq, OpenRouter, NVIDIA, etc).
Solo se necesita cambiar LLM_BASE_URL y LLM_MODEL en el .env.
"""

import logging
from openai import AsyncOpenAI
from config.settings import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

logger = logging.getLogger(__name__)

# Instancia global del cliente, se reutiliza en cada llamada
_client = AsyncOpenAI(
    api_key=LLM_API_KEY or "placeholder",
    base_url=LLM_BASE_URL,
)


async def ask_llm(messages: list[dict]) -> str:
    """
    Envía una lista de mensajes (con formato OpenAI) al LLM y retorna
    la respuesta como texto.

    Recibe el historial completo (system + user + assistant) para que
    el modelo tenga contexto de toda la conversación.

    Si no hay API key configurada, retorna un mensaje de aviso en vez
    de intentar la llamada.
    """
    if not LLM_API_KEY:
        return (
            "El bot aún no tiene un LLM configurado. "
            "Agrega tu LLM_API_KEY en el archivo .env y reiníciame."
        )

    try:
        kwargs = {
            "model": LLM_MODEL,
            "messages": messages,
        }

        # Los modelos Nemotron de NVIDIA requieren parámetros extra
        # para habilitar el modo de razonamiento
        if "nemotron" in LLM_MODEL.lower():
            kwargs["extra_body"] = {
                "chat_template_kwargs": {"enable_thinking": True},
                "reasoning_budget": 8192,
            }
            kwargs["max_tokens"] = 8192

        response = await _client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or "Respuesta vacía del modelo."

    except Exception as e:
        logger.error("Error al llamar al LLM: %s", e)
        raise