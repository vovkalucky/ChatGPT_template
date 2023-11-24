# -*- coding: utf-8 -*-
import asyncio
from aiogram import types
from aiogram import Bot
from aiogram import Router
from bot.lexicon.lexicon_ru import LEXICON_RU
from chatgpt4 import connect_client, create_assistant, create_thread, add_message_to_thread, run_assistant, \
    response_gpt, clear_context, wait_run_assistant
from bot.models.methods import minus_request_count, check_user_request_count, sql_add_user, sql_group_add_user
from bot.filters.chat_type import ChatTypeFilter
import logging
from aiogram import F
from bot.config_data.config import load_config
from aiogram.filters import Command
#работа с машиной состояний
from bot.states.states import UseGPT
from aiogram.fsm.context import FSMContext

config = load_config()

# Создайте логгер для этого модуля или хэндлера
logger = logging.getLogger(__name__)

router: Router = Router()

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str, str]] = {}


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), F.text.startswith(config.tg_bot.bot_username), UseGPT.state1_group_user_request)
async def send_message(message: types.Message, bot: Bot) -> None:
    logger.info(f"Пользователь {message.from_user.username}(id={message.from_user.id}) спрашивает в группе: {message.text}")
    client = user_dict[message.from_user.id]['client_key']
    assistant = user_dict[message.from_user.id]['assistant_key']
    thread = user_dict[message.from_user.id]['thread_key']

    content = message.text

    await add_message_to_thread(client, thread, content)
    run = await run_assistant(client, thread, assistant)
    waiting_message: types.Message = await message.answer(text=LEXICON_RU['loading_model'])
    await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."
    try:
        result = await asyncio.wait_for(wait_run_assistant(client, thread, run), timeout=80)
        request_count = await check_user_request_count(message)
        if request_count > 0:
            if result == 'completed':
                answer_gpt = response_gpt(client, thread)
                await minus_request_count(message)
                message_answer = await message.reply(await answer_gpt)
                await waiting_message.delete()
                logger.info(f"GPT в группе дал ответ пользователю {message.from_user.username}(id={message.from_user.id}): {message_answer.text}")
        else:
            await message.answer(text=LEXICON_RU['response_null'])
    except asyncio.TimeoutError:
        # Обработка случая, когда статус не изменился в течение timeout (сек)
        await waiting_message.answer(text=LEXICON_RU['no_response'])


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command(commands=['cancel']), UseGPT.state1_group_user_request)
async def context_clear(message: types.Message, state: FSMContext) -> None:
    print('Мы в очистке контекста группы')
    client = user_dict[message.from_user.id]['client_key']
    thread = user_dict[message.from_user.id]['thread_key']
    await clear_context(client, thread)
    await state.clear()
    await message.answer(text=LEXICON_RU['/cancel'])


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), F.text.startswith(config.tg_bot.bot_username))
async def group_message(message: types.Message, bot: Bot, state: FSMContext) -> None:
    #Добавляем пользователя в базу данных
    await sql_group_add_user(message)
    logger.info(
        f"Пользователь {message.from_user.username}(id={message.from_user.id}) спрашивает: {message.text}")

    client = await connect_client()
    assistant = await create_assistant()
    thread = await create_thread(client)
    await state.update_data(client_key=client, assistant_key=assistant, thread_key=thread)
    #data = await state.get_data()
    user_dict[message.from_user.id] = await state.get_data()

    client = user_dict[message.from_user.id]['client_key']
    assistant = user_dict[message.from_user.id]['assistant_key']
    thread = user_dict[message.from_user.id]['thread_key']

    content = message.text

    await add_message_to_thread(client, thread, content)
    run = await run_assistant(client, thread, assistant)
    waiting_message: types.Message = await message.answer(text=LEXICON_RU['loading_model'])
    await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."
    try:
        result = await asyncio.wait_for(wait_run_assistant(client, thread, run), timeout=80)
        request_count = await check_user_request_count(message)
        if request_count > 0:
            if result == 'completed':
                answer_gpt = response_gpt(client, thread)
                await minus_request_count(message)
                message_answer = await message.reply(await answer_gpt)
                await waiting_message.delete()
                logger.info(
                    f"GPT в группе дал ответ пользователю {message.from_user.username}(id={message.from_user.id}): {message_answer.text}")
        else:
            await message.answer(text=LEXICON_RU['response_null'])
    except asyncio.TimeoutError:
        # Обработка случая, когда статус не изменился в течение timeout (сек)
        await waiting_message.answer(text=LEXICON_RU['no_response'])
    await state.set_state(UseGPT.state1_group_user_request)


