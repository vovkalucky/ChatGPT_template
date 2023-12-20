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

from bot.models.methods import check_user_request_count, minus_request_count
#работа с машиной состояний
from bot.states.states import UseDalle
from aiogram.fsm.context import FSMContext

# Создайте логгер для этого модуля или хэндлера
logger = logging.getLogger(__name__)


# Инициализируем роутер уровня модуля
router: Router = Router()


# @router.message(Command(commands=['dalle']))
# @router.callback_query(lambda callback_query: callback_query.data == 'dalle')
# async def create_image_start(message: types.Message, state: FSMContext) -> None:
#     await message.answer(text=LEXICON_RU['create_image'])
#     await state.set_state(UseDalle.state_dalle_user_request)


@router.message(F.text, UseDalle.state_dalle_user_request) #, SubChecker()
async def create_image_handler(message: types.Message, bot: Bot) -> None:
    waiting_message: types.Message = await message.answer(text=LEXICON_RU['loading_model'])

    await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."
    try:
        request_count = await check_user_request_count(message)
        if request_count > 0:
            await minus_request_count(message)

            #waiting_message: types.Message = await message.answer(text=LEXICON_RU['loading_model'])
            image_url = await create_image(message.text)
            await bot.send_photo(message.chat.id, image_url)
            await waiting_message.delete()
            # logger.info(f"GPT дал ответ пользователю {message.from_user.username}(id={message.from_user.id}): {message_answer.text}")
        else:
            await waiting_message.edit_text(text=LEXICON_RU['response_null'])
    except asyncio.TimeoutError:
        # Обработка случая, когда статус не изменился в течение timeout (сек)
        await waiting_message.edit_text(text=LEXICON_RU['no_response'])


    await message.answer(text=LEXICON_RU['create_image_cancel'])


@router.message(Command(commands=['start']), UseDalle.state_dalle_user_request)
async def create_image_clear_context(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text=LEXICON_RU['gpt_start_dialog'])