from domain.repositories.IBotServicePort import IBotServicePort
from domain.entities.ChatMessage import ChatMessage
from dotenv import load_dotenv
from typing import Any
import asyncio
import os
import logging
from utils.thread_task import thread_task
from telegram import Update
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


class TelegramBot(IBotServicePort):
    application: Application

    def init(self, func: Any):
        self.application = (
            Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
        )

        self.application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, self.create_message_handle(func)
            )
        )

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def create_message_handle(self, func: Any):
        async def message_handler(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
        ):
            response: ChatMessage = func(update.message.text)
            await update.message.reply_text(response.message)

        return message_handler
