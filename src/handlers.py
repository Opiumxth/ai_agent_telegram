"""
Handlers de Telegram: comandos (/start, /help, /reset) y mensajes de texto.
Gestiona la memoria conversacional y la persistencia en disco.
"""

import json
import logging
from pathlib import Path
from collections import defaultdict
from telegram import Update
from telegram.ext import ContextTypes
from config.settings import SYSTEM_PROMPT, MAX_HISTORY
from src.llm_client import ask_llm

logger = logging.getLogger(__name__)

# Historial en memoria: { chat_id: [{"role": "...", "content": "..."}, ...] }
conversation_history: dict[int, list[dict]] = defaultdict(list)

# Carpeta donde se persisten las conversaciones como JSON
BASE_DIR = Path(__file__).resolve().parent.parent
CONVERSACIONES_DIR = BASE_DIR / "conversaciones"
CONVERSACIONES_DIR.mkdir(exist_ok=True)


def _get_messages(chat_id: int) -> list[dict]:
    """
    Construye la lista completa de mensajes para enviar al LLM.
    Antepone el system prompt al historial del usuario para que el modelo
    siempre tenga contexto de su rol.
    """
    return [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history[chat_id]


def _save_history(chat_id: int) -> None:
    """
    Guarda el historial de un chat como archivo JSON en la carpeta conversaciones/.
    Cada usuario tiene su propio archivo identificado por su chat_id.
    """
    filepath = CONVERSACIONES_DIR / f"{chat_id}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(conversation_history[chat_id], f, ensure_ascii=False, indent=2)


def _add_message(chat_id: int, role: str, content: str) -> None:
    """
    Agrega un mensaje al historial de un chat.
    - Ignora mensajes vacíos para evitar errores en el LLM.
    - Recorta el historial si supera el límite (MAX_HISTORY pares user/assistant).
    - Persiste el historial en disco después de cada mensaje.
    """
    if not content:
        return

    conversation_history[chat_id].append({"role": role, "content": content})

    # MAX_HISTORY cuenta pares, así que el límite real es el doble
    if len(conversation_history[chat_id]) > MAX_HISTORY * 2:
        conversation_history[chat_id] = conversation_history[chat_id][-MAX_HISTORY * 2:]

    _save_history(chat_id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler del comando /start.
    Saluda al usuario por su nombre y le indica cómo empezar a usar el bot.
    """
    user = update.effective_user
    welcome = (
        f"¡Hola, {user.first_name}! Soy el asistente de IA del IEEE CS PUCP.\n\n"
        "Puedo ayudarte con preguntas, dudas o simplemente charlar. "
        "Solo escríbeme lo que necesites.\n\n"
        "Usa /help para ver los comandos disponibles."
    )
    await update.message.reply_text(welcome)
    logger.info("Usuario %s inició el bot.", user.id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler del comando /help.
    Muestra al usuario la lista de comandos disponibles del bot.
    """
    help_text = (
        "Comandos disponibles:\n\n"
        "/start — Mensaje de bienvenida\n"
        "/help  — Muestra esta ayuda\n"
        "/reset — Borra el historial de conversación\n\n"
        "O simplemente escríbeme y responderé usando IA."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler del comando /reset.
    Borra todo el historial de conversación del usuario, permitiéndole
    empezar una conversación nueva sin contexto previo.
    """
    chat_id = update.effective_chat.id
    conversation_history[chat_id].clear()
    await update.message.reply_text("Historial borrado. ¡Empecemos de nuevo!")
    logger.info("Historial reseteado para chat %s.", chat_id)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler principal de mensajes de texto.
    Recibe el mensaje del usuario, lo agrega al historial, consulta al LLM
    con todo el contexto acumulado y envía la respuesta de vuelta.
    Si el LLM falla, remueve el mensaje del historial para no dejar
    el contexto en un estado inconsistente.
    """
    chat_id = update.effective_chat.id
    user_text = update.message.text

    # Mostrar "escribiendo..." mientras el LLM procesa
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    _add_message(chat_id, "user", user_text)

    try:
        response_text = await ask_llm(_get_messages(chat_id))
    except Exception as e:
        logger.error("Error en LLM para chat %s: %s", chat_id, e)
        # Si falla, quitar el último mensaje para no contaminar el historial
        conversation_history[chat_id].pop()
        await update.message.reply_text(
            "Tuve un problema al procesar tu mensaje. Inténtalo de nuevo."
        )
        return

    _add_message(chat_id, "assistant", response_text)
    await update.message.reply_text(response_text)
    logger.info("Respondido a chat %s (%d chars).", chat_id, len(response_text))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler global de errores.
    Captura cualquier excepción no manejada por los demás handlers
    para que el bot no se caiga y quede registrado en los logs.
    """
    logger.error("Error inesperado: %s", context.error, exc_info=context.error)
