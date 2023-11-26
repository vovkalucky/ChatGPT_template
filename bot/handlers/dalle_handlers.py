import asyncio
from aiogram import types
from aiogram import F
from aiogram import Bot

from bot.filters.check_subscription import SubChecker
from aiogram.filters import Command
from aiogram import Router
from bot.lexicon.lexicon_ru import LEXICON_RU
from bot.external_services.dalle import create_image


import logging
#работа с машиной состояний
from bot.states.states import UseDalle
from aiogram.fsm.context import FSMContext

# Создайте логгер для этого модуля или хэндлера
logger = logging.getLogger(__name__)


# Инициализируем роутер уровня модуля
router: Router = Router()


@router.message(Command(commands=['image']))
async def create_image_start(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=LEXICON_RU['create_image'])
    await state.set_state(UseDalle.state_dalle_user_request)


@router.message(F.text, UseDalle.state_dalle_user_request)
async def create_image_handler(message: types.Message, bot: Bot) -> None:
    waiting_message: types.Message = await message.answer(text=LEXICON_RU['loading_model'])
    image_url = await create_image(message.text)
    await bot.send_photo(message.chat.id, image_url)
    await waiting_message.delete()
    await message.answer(text=LEXICON_RU['create_image_cancel'])


@router.message(Command(commands=['start']), UseDalle.state_dalle_user_request)
async def create_image_clear_context(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text=LEXICON_RU['gpt_start_dialog'])