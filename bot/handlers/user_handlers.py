import asyncio
from aiogram import types
from aiogram import F
import os
import time
from aiogram import Bot

from bot.filters.check_subscription import SubChecker
from bot.keyboards.user_keyboards import get_main_kb, get_about_kb, get_context_kb, get_gpt_true_false_kb
from aiogram.types import CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram import Router
from bot.lexicon.lexicon_ru import LEXICON_RU
from chatgpt4 import connect_client, create_assistant, create_thread, add_message_to_thread, run_assistant, \
    response_gpt, clear_context, wait_run_assistant
from bot.models.methods import minus_request_count, check_user_request_count, sql_add_user

import logging
#работа с машиной состояний
from bot.states.states import UseGPT
from aiogram.fsm.context import FSMContext

# Создайте логгер для этого модуля или хэндлера
logger = logging.getLogger(__name__)


# Инициализируем роутер уровня модуля
router: Router = Router()

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str, str]] = {}


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(Command(commands=['start']))
async def process_start_command(message: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    await sql_add_user(message)
    await state.clear()
    client = await connect_client()
    assistant = await create_assistant()
    thread = await create_thread(client)
    await state.update_data(client_key=client, assistant_key=assistant, thread_key=thread)
    data = await state.get_data()
    #print(f"update_data: {data}")
    # Добавляем в "базу данных" анкету пользователя по ключу id пользователя
    user_dict[message.from_user.id] = await state.get_data()

    await message.answer(text=LEXICON_RU['gpt_start_dialog'])
    await state.set_state(UseGPT.state1_user_request)


@router.message(Command(commands=['cancel']), UseGPT.state1_user_request)
async def context_clear(message: types.Message, state: FSMContext) -> None:
    print('Мы в очистке контекста')
    client = user_dict[message.from_user.id]['client_key']
    thread = user_dict[message.from_user.id]['thread_key']
    await clear_context(client, thread)
    await state.clear()
    await message.answer(text=LEXICON_RU['/cancel'])


@router.message(F.text, UseGPT.state1_user_request, SubChecker())
async def send_message(message: types.Message, bot: Bot) -> None:
    logger.info(f"Пользователь {message.from_user.username}(id={message.from_user.id}) спрашивает: {message.text}")
    await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."
    client = user_dict[message.from_user.id]['client_key']
    assistant = user_dict[message.from_user.id]['assistant_key']
    thread = user_dict[message.from_user.id]['thread_key']
    content = message.text
    #print(content)
    await add_message_to_thread(client, thread, content)
    run = await run_assistant(client, thread, assistant)
    waiting_message: types.Message = await message.answer(text=LEXICON_RU['loading_model'])
    try:
        result = await asyncio.wait_for(wait_run_assistant(client, thread, run), timeout=80)
        request_count = await check_user_request_count(message)
        if request_count > 0:
            if result == 'completed':
                answer_gpt = response_gpt(client, thread)
                await minus_request_count(message)
                message_answer = await waiting_message.edit_text(await answer_gpt)
                logger.info(f"GPT дал ответ пользователю {message.from_user.username}(id={message.from_user.id}): {message_answer.text}")
        else:
            await waiting_message.edit_text(text=LEXICON_RU['response_null'])
    except asyncio.TimeoutError:
    # Обработка случая, когда статус не изменился в течение timeout (сек)
        await waiting_message.edit_text(text=LEXICON_RU['no_response'])







