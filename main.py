import asyncio
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from aiogram import Bot, Dispatcher
from bot.handlers import user_handlers, admin_handlers, group_handlers, dalle_handlers, \
    voice_handlers, other_handlers, translate_handlers
from bot.keyboards.set_menu import set_main_menu
from aiogram.fsm.storage.memory import MemoryStorage
#from bot.models.methods import db_start
from bot.config_data.config import load_config


#async def on_startup():
    #await db_start()
    #pass


async def main() -> None:
    # Создаем экземпляр логгера
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Создаем handler
    handler = TimedRotatingFileHandler(f'logs/bot_logs.log', when='D', backupCount=4)
    #handler.setLevel(logging.INFO)

    # Настройка формата сообщений
    # formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    # handler.setFormatter(formatter)

    # Добавляем handler к логгеру
    logger.addHandler(handler)


    # Инициализируем логгер
    #logger = logging.getLogger(__name__)


    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        #filename='logs/bot_logs.log',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_routers(group_handlers.router, user_handlers.router, voice_handlers.router,
                       dalle_handlers.router, admin_handlers.router, other_handlers.router, translate_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    # Регистрация функции, которая сработает при запуске бота
    #dp.startup.register(on_startup)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as _ex:
        print(f'There is exception - {_ex}')


# Запускаем поллинг
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stop bot")
