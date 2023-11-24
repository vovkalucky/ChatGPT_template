from dataclasses import dataclass
from environs import Env


@dataclass
class OpenaiConfig:
    organization_id: str         # id компании
    api_key: str
    assistant_id: str


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота
    group_id: int         # id группы в которой будет работать бот
    bot_username: str     # username бота
    admin_username: str   # username админа для связи (зашит в инлайн кнопке)


@dataclass
class Config:
    tg_bot: TgBot
    open_ai: OpenaiConfig

def load_config(path: str | None = None) -> Config:
    # Создаем экземпляр класса Env
    env: Env = Env()
    # Добавляем в переменные окружения данные, прочитанные из файла .env
    env.read_env()
    # Создаем экземпляр класса Config и наполняем его данными из переменных окружения
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            group_id=env('GROUP_ID'),
            bot_username=env('BOT_USERNAME'),
            admin_username=env('ADMIN_USERNAME')
        ),
        open_ai=OpenaiConfig(
            organization_id=env('OPEN_AI_ORGANIZATION_ID'),
            api_key=env('OPENAI_API_KEY'),
            assistant_id=env('ASSISTANT_ID'),
        )
    )


# Выводим значения полей экземпляра класса Config на печать,
# чтобы убедиться, что все данные, получаемые из переменных окружения, доступны
# config = load_config()
# print('BOT_TOKEN:', config.tg_bot.token)
# print('ADMIN_IDS:', config.tg_bot.admin_ids)
# print('GROUP_ID:', config.tg_bot.group_id)
# print('BOT_USERNAME:', config.tg_bot.bot_username)
# print('ADMIN_USERNAME:', config.tg_bot.admin_username)
# print()
# print('OPEN_AI_ORGANIZATION_ID:', config.open_ai.organization_id)
# print('OPENAI_API_KEY:', config.open_ai.api_key)
# print('ASSISTANT_ID:', config.open_ai.assistant_id)
