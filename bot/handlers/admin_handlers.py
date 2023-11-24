import os

from aiogram import types
from dotenv import load_dotenv

from bot.keyboards.admin_keyboards import *
from aiogram.filters import Command
from aiogram import F, Router
from bot.lexicon.lexicon_ru import LEXICON_RU
from bot.models.methods import check_user_request_count, get_users
from bot.config_data.config import load_config
config = load_config()
#Инициализируем роутер уровня модуля
router: Router = Router()


#@router.message(Command(commands=['admin']), F.from_user.id == 263016509)
@router.message(Command(commands=['admin']), F.from_user.id.in_(config.tg_bot.admin_ids))
async def admin_menu(message: types.Message) -> None:
    await message.answer(text=LEXICON_RU['admin_menu'], reply_markup=get_admin_menu_kb())


@router.callback_query(lambda callback_query: callback_query.data == 'admin_response', F.from_user.id.in_(config.tg_bot.admin_ids))
async def admin_check_request(callback: types.CallbackQuery) -> None:
    count_request = await check_user_request_count(callback)
    await callback.message.answer(text=f"У вас осталось запросов к ChatGPT: {count_request}", reply_markup=get_admin_menu_kb())
    await callback.answer()


@router.callback_query(lambda callback_query: callback_query.data == 'admin_users', F.from_user.id.in_(config.tg_bot.admin_ids))
async def admin_get_users(callback: types.CallbackQuery) -> None:
    count_users, all_users = await get_users()
    await callback.message.answer(text=f"Пользователей: {count_users}")
    all_users_dict = ""
    for i in range(0, count_users):
        all_users_dict += f"{i+1}) id{all_users[i][0]}({all_users[i][1]}), Рега: {all_users[i][2][0:10]} Запросов: {all_users[i][3]}\n"
    await callback.message.answer(text=f"{all_users_dict}", reply_markup=get_admin_menu_kb())
    await callback.answer()
