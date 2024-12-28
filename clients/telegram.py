import requests
from telegram import Bot


class Telegram:
    BOT_TOKEN = "7549329958:AAHt3TcOfHYD3UGv8OWm2Tv6331JiEL6ImY"
    CHANNEL_ID = (
        "-1002154946315"  # Or use the channel's numeric ID (e.g., -1001234567890)
    )
    @classmethod
    def send_message_to_channel(cls, message):
        """
        Sends a message to the Telegram channel.
        :param message: The message to send.
        """
        try:
            # bot = Bot(token=cls.BOT_TOKEN)
            # bot.send_message(chat_id=cls.CHANNEL_ID, text=message)
            url = f"https://api.telegram.org/bot{cls.BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": cls.CHANNEL_ID,
                "text": message
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"An error occurred: {e}")
