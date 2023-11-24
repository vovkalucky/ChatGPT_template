# -*- coding: utf-8 -*-
import asyncio
from aiogram import types
import os
from aiogram import Bot
from aiogram import Router
from bot.lexicon.lexicon_ru import LEXICON_RU
from chatgpt4 import connect_client, create_assistant, create_thread, add_message_to_thread, run_assistant, \
    response_gpt, clear_context, wait_run_assistant
from bot.models.methods import minus_request_count, check_user_request_count, sql_add_user, sql_group_add_user
from bot.filters.chat_type import ChatTypeFilter
import logging
from bot.config_data.config import load_config
config = load_config()

# Создайте логгер для этого модуля или хэндлера
logger = logging.getLogger(__name__)

router: Router = Router()

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str, str]] = {}


#@router.message(chat_id=os.getenv("GROUP_ID"))
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]))
async def group_message(message: types.Message, bot: Bot) -> None:
    #print(message.from_user.id)
    if config.tg_bot.bot_username in message.text:
        print(message)
        await sql_group_add_user(message)
        logger.info(
            f"Пользователь {message.from_user.username}(id={message.from_user.id}) спрашивает: {message.text}")
        await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."

        client = await connect_client()
        assistant = await create_assistant()
        thread = await create_thread(client)
        content = message.text

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
                await message.answer(text=LEXICON_RU['response_null'])
        except asyncio.TimeoutError:
            # Обработка случая, когда статус не изменился в течение timeout (сек)
            await waiting_message.answer(text=LEXICON_RU['no_response'])