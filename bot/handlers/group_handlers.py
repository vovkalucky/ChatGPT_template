# -*- coding: utf-8 -*-
import asyncio
from aiogram import types
from aiogram import Bot
from aiogram import Router
from bot.filters.group_filter_bot_id import check_bot_id
from bot.lexicon.lexicon_ru import LEXICON_RU
from bot.external_services.chatgpt4 import OpenaiSession
from bot.models.methods import minus_request_count, check_user_request_count, sql_group_add_user
from bot.filters.chat_type import ChatTypeFilter
import logging
from aiogram import F
from bot.config_data.config import load_config
from aiogram.filters import Command
#работа с машиной состояний
from aiogram.fsm.context import FSMContext

config = load_config()

# Создайте логгер для этого модуля или хэндлера
logger = logging.getLogger(__name__)

router: Router = Router()


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command(commands=['cancel']))
async def context_clear_in_group(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    if 'group_session' in data:
        session: OpenaiSession = data['session']
        await session.clear_context()
    await message.answer(text=LEXICON_RU['/cancel'])


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), F.text.startswith(config.tg_bot.bot_username))
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), check_bot_id)
async def group_message(message: types.Message, bot: Bot, state: FSMContext) -> None:
    #Добавляем пользователя в базу данных
    await sql_group_add_user(message)
    logger.info(f"Пользователь {message.from_user.username}(id={message.from_user.id}) спрашивает: {message.text}")
    content = message.text
    data = await state.get_data()
    if 'group_session' not in data:
        session = OpenaiSession()
        await state.update_data(group_session=session)
        data = await state.get_data()
    session: OpenaiSession = data['group_session']
    print(f"Data после: {data}")
    await session.add_message_to_thread(content)
    await session.run_assistant()
    # except PermissionDeniedError:
    #     print('Доступ к сайту openai ограничен! Нужно включить VPN')
    waiting_message: types.Message = await message.answer(text=LEXICON_RU['loading_model'])
    await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."
    try:
        result = await session.wait_run_assistant()
        request_count = await check_user_request_count(message)
        if request_count > 0:
            if result == 'completed':
                answer_gpt = await session.response_gpt()
                await minus_request_count(message)
                await waiting_message.delete()
                message_answer = await message.reply(answer_gpt)
                # logger.info(f"GPT дал ответ пользователю {message.from_user.username}(id={message.from_user.id}): {message_answer.text}")
        else:
            await waiting_message.edit_text(text=LEXICON_RU['response_null'])
    except asyncio.TimeoutError:
        # Обработка случая, когда статус не изменился в течение timeout (сек)
        await waiting_message.edit_text(text=LEXICON_RU['no_response'])
    #await state.set_state(UseGPT.state1_group_user_request)


