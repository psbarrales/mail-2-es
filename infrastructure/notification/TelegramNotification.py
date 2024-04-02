from domain.repositories.INotificationServicePort import INotificationServicePort
from dotenv import load_dotenv
import os
import telegram
import asyncio

load_dotenv()


class TelegramNotification(INotificationServicePort):
    def send_notification(self, message: str):
        bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
        asyncio.run(
            bot.send_message(chat_id=os.getenv("TELEGRAM_CHATID"), text=message)
        )
