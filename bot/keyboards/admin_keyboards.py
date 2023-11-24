from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.lexicon.lexicon_ru import LEXICON_RU
import os


def get_admin_main_kb() -> InlineKeyboardMarkup:
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Создаем объекты инлайн-кнопок
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['gpt'],
        callback_data='gpt')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['about'],
        callback_data='about')
    url_button_3: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['admin'],
        callback_data='admin')
    # Добавляем кнопки в клавиатуру методом add
    keyboard.add(url_button_1).add(url_button_2).add(url_button_3)
    keyboard.adjust(1)  # делает строки по 1 кнопке
    return keyboard.as_markup()


def get_admin_menu_kb() -> InlineKeyboardMarkup:
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Создаем объекты инлайн-кнопок
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['admin_users'],
        callback_data='admin_users')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['admin_response'],
        callback_data='admin_response')
    # Добавляем кнопки в клавиатуру методом add
    keyboard.add(url_button_1).add(url_button_2)
    keyboard.adjust(1)  # делает строки по 1 кнопке
    return keyboard.as_markup()