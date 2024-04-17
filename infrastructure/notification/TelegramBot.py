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
    bot: Bot = None
    application: Application = None
    dispatcher = None
    is_initialized = False

    def __init__(self):
        token = os.getenv("TELEGRAM_TOKEN")
        self.bot = Bot(token=token)
        self.application = Application.builder().token(token=token).build()

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

    def create_message_handle(self, callback: Any):
        async def message_handler(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
        ):
            response: ChatMessage = callback(update.message.text)
            await update.message.reply_text(response.message)

        return message_handler

    def send_notification(self, message: str):
        asyncio.run(
            self.bot.send_message(chat_id=os.getenv("TELEGRAM_CHATID"), text=message)
        )
