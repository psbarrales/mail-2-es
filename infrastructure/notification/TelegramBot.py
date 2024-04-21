from domain.repositories.IBotServicePort import IBotServicePort
from domain.repositories.INotificationServicePort import INotificationServicePort
from domain.entities.ChatMessage import ChatMessage
from utils.singleton import Singleton
from dotenv import load_dotenv
from typing import Any
import os
import logging
import asyncio
from telegram import Update, Bot
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


class TelegramBot(IBotServicePort, INotificationServicePort, metaclass=Singleton):
    application: Application = None
    token: str
    is_initialized = False

    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.application = Application.builder().token(token=self.token).build()

    def init(self):
        # Inicia el bot para recibir mensajes
        if self.is_initialized:
            return
        self.is_initialized = True
        self.application.run_polling()

    def on_message(self, callback):
        # Registra un manejador de mensajes que usa el callback proporcionado
        message_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.create_message_handle(callback)
        )
        self.application.add_handler(message_handler)

    def on_command(self, command_name, callback):
        # Registra un manejador de mensajes que usa el callback proporcionado
        command_handler = CommandHandler(
            command_name,
            self.create_command_handle(command_name, callback),
        )
        self.application.add_handler(command_handler)

    def create_message_handle(self, callback: Any):
        async def message_handler(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
        ):
            response: ChatMessage = callback(update.message.text)
            await update.message.reply_text(response.message)

        return message_handler

    def create_command_handle(self, command_name, callback: Any):
        async def command_handler(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
        ):
            command_prefix = f"/{command_name} "
            text = update.message.text
            if text.startswith(command_prefix):
                # Elimina el comando y un espacio adicional
                argument_text = text[len(command_prefix) :]
            elif text == f"/{command_name}":
                # Si el comando está solo sin argumentos adicionales
                argument_text = ""
            else:
                # En caso de que el comando esté seguido directamente de otro texto sin espacio
                argument_text = (
                    text[len(command_name) :]
                    if text.startswith(f"/{command_name}")
                    else text
                )
            response: ChatMessage = callback(argument_text)
            await update.message.reply_text(response.message)

        return command_handler

    def send_notification(self, message: str):
        bot = Bot(token=self.token)
        asyncio.run(
            bot.send_message(chat_id=os.getenv("TELEGRAM_CHATID"), text=message)
        )
