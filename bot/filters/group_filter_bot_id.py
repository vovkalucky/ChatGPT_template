from aiogram.types import Message
from bot.config_data.config import load_config
config = load_config()


def check_bot_id(message: Message) -> bool:
    return message.reply_to_message and message.reply_to_message.from_user.id == int(config.tg_bot.bot_id)
