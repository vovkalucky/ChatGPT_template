import asyncio
from aiogram import types
from aiogram import F
from aiogram import Bot
from bot.keyboards.user_keyboards import get_gpt_true_false_kb
from aiogram import Router
from bot.lexicon.lexicon_ru import LEXICON_RU
from bot.external_services.chatgpt4 import connect_client, add_message_to_thread, run_assistant, wait_run_assistant, \
    response_gpt
from bot.models.methods import minus_request_count, check_user_request_count
from bot.external_services.chatgpt4 import recognise_voice
import logging

# Создайте логгер для этого модуля или хэндлера
logger = logging.getLogger(__name__)

#работа с машиной состояний
from bot.states.states import UseGPT
from aiogram.fsm.context import FSMContext


# Инициализируем роутер уровня модуля
router: Router = Router()


@router.message(F.voice, UseGPT.state1_user_request)
async def send_voice_message(message: types.Voice, bot: Bot, state: FSMContext) -> None:
    message_wait: types.Message = await message.answer("⌛ Перевожу ваш запрос в текст...")
    await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."
    client = await connect_client()
    voice = message.voice
    file_id = voice.file_id

    # Получение информации о файле голосового сообщения
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    text_from_voice = await recognise_voice(client, file_path)
    await state.update_data(message_voice=text_from_voice)
    await message_wait.edit_text(text=f"<b>Ваш запрос:</b> \n\n{text_from_voice} \n\nВерно?", reply_markup=get_gpt_true_false_kb())


@router.callback_query(lambda callback_query: callback_query.data == 'yes', UseGPT.state1_user_request)
async def send_text_from_voice_message(message: types.CallbackQuery, state: FSMContext) -> None:
    print(message)
    data = await state.get_data()
    client = data['client_key']
    assistant = data['assistant_key']
    thread = data['thread_key']
    content = data['message_voice']
    print(content)
    await add_message_to_thread(client, thread, content)
    run = await run_assistant(client, thread, assistant)
    waiting_message: types.Message = await message.message.answer(text=LEXICON_RU['loading_model'])
    #await bot.send_chat_action(message.chat.id, 'typing')  # Эффект набора сообщения "Печатает..."
    try:
        result = await asyncio.wait_for(wait_run_assistant(client, thread, run), timeout=80)
        request_count = await check_user_request_count(message)
        if request_count > 0:
            if result == 'completed':
                answer_gpt = response_gpt(client, thread)
                await minus_request_count(message)
                message_answer = await waiting_message.edit_text(await answer_gpt)
                logger.info(
                    f"GPT дал ответ пользователю {message.from_user.username}(id={message.from_user.id}): {message_answer.text}")
        else:
            await message.waiting_message.edit_text(text=LEXICON_RU['response_null'])
    except asyncio.TimeoutError:
        # Обработка случая, когда статус не изменился в течение timeout (сек)
        await message.message.answer(text=LEXICON_RU['no_response'])


@router.callback_query(lambda callback_query: callback_query.data == 'no', UseGPT.state1_user_request)
async def voice_message_repeat(message: types.CallbackQuery) -> None:
    await message.message.answer(text=LEXICON_RU['repeat_voice_message'])

