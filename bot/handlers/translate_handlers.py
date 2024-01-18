import asyncio
from aiogram import types
from aiogram import F
from aiogram import Bot
from aiogram.filters import Command, StateFilter
from aiogram import Router

from bot.config_data.config import load_config
from bot.lexicon.lexicon_ru import LEXICON_RU
from bot.external_services.chatgpt4 import OpenaiSession
from bot.models.methods import minus_request_count, check_user_request_count
import logging
#работа с машиной состояний
from bot.states.states import UseTranslate
from aiogram.fsm.context import FSMContext
# Инициализируем роутер уровня модуля
router: Router = Router()

config = load_config()


@router.message(Command(commands=['pereskaz']))
async def process_trans_command(message: types.Message, state: FSMContext) -> None:
    await message.answer(LEXICON_RU['translate_audio'])
    await state.set_state(UseTranslate.state_start_translate)


@router.message(F.audio, UseTranslate.state_start_translate) #, SubChecker()
async def send_media_message(message: types.Message, bot: Bot, state: FSMContext) -> None:
    try:
        message_wait: types.Message = await message.answer("⌛ Перевожу аудио запрос в текст...")
        session = OpenaiSession(config.open_ai.assistant_translate_id)
        client = session.client
        audio = message.audio
        file_id = audio.file_id

        # Получение информации о файле голосового сообщения
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file_ext = audio.file_name.split('.')[-1]
        text_from_voice = await session.recognise_audio_and_voice(file_path, file_ext)
        waiting_message = await message_wait.edit_text(text=LEXICON_RU['translate_complete'])
        await session.add_message_to_thread(content=text_from_voice)
        await session.run_assistant()
        try:
            result = await asyncio.wait_for(session.wait_run_assistant(), timeout=80)
            request_count = await check_user_request_count(message)
            if request_count > 0:
                if result == 'completed':
                    answer_gpt = await session.response_gpt()
                    await minus_request_count(message)
                    message_answer = await waiting_message.edit_text(answer_gpt)
                    # logger.info(f"GPT дал ответ пользователю {message.from_user.username}(id={message.from_user.id}): {message_answer.text}")
            else:
                await waiting_message.edit_text(text=LEXICON_RU['response_null'])
        except asyncio.TimeoutError:
            # Обработка случая, когда статус не изменился в течение timeout (сек)
            await waiting_message.edit_text(text=LEXICON_RU['no_response'])
    except Exception as er:
        await message.answer(f"‼️ Произошла ошибка:\n\n {er}! \n\nВы можете повторите запрос ⏬")

