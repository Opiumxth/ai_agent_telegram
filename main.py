"""
Punto de entrada del bot de Telegram.
Configura el logging, registra los handlers de comandos y mensajes,
y arranca el polling para recibir actualizaciones.
"""

import logging
import sys
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from config.settings import TELEGRAM_TOKEN
from src.handlers import (
    start,
    help_command,
    reset,
    handle_message,
    error_handler,
)

# Configurar logging para toda la aplicación
logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    stream=sys.stdout,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Función principal que inicializa el bot.
    Construye la aplicación de Telegram, registra todos los handlers
    (comandos y mensajes de texto) y arranca el polling.
    """
    logger.info("Iniciando AI_Agent_Basic...")

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .concurrent_updates(True)
        .build()
    )

    # Registrar comandos y handler de mensajes de texto
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info("Bot listo. Esperando mensajes (Ctrl+C para detener)...")
    app.run_polling(
        allowed_updates=["message"],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()