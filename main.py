import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers import user_handlers, admin_handlers, group_handlers, dalle_handlers, voice_handlers
from bot.keyboards.set_menu import set_main_menu
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from bot.models.methods import db_start
from bot.config_data.config import load_config




async def on_startup():
    await db_start()


async def main() -> None:
    # Инициализируем логгер
    logger = logging.getLogger(__name__)


    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        #filename='bot_logs.log',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    # handler = TimedRotatingFileHandler('bot_logs.log', when='M', backupCount=4)
    # logger.addHandler(handler)
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
    dp.include_routers(group_handlers.router, user_handlers.router, voice_handlers.router, dalle_handlers.router, admin_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    # собственно способ зарегистрировать функцию которая сработает при запуске бота
    dp.startup.register(on_startup)
    try:
        await dp.start_polling(bot, skip_updates=True, allowed_updates=dp.resolve_used_update_types()) #on_startup=on_startup
    except Exception as _ex:
        print(f'There is exception - {_ex}')


# Запускаем поллинг
if __name__ == '__main__':
    asyncio.run(main())
