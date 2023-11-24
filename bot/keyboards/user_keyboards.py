from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.lexicon.lexicon_ru import LEXICON_RU
import os
from bot.config_data.config import load_config
config = load_config()

def get_main_kb() -> InlineKeyboardMarkup:
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Создаем объекты инлайн-кнопок
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['gpt'],
        callback_data='gpt')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text=LEXICON_RU['about'],
        callback_data='about')
    # Добавляем кнопки в клавиатуру методом add
    keyboard.add(url_button_1).add(url_button_2)
    keyboard.adjust(1)  # делает строки по 1 кнопке
    return keyboard.as_markup()


def get_about_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text=LEXICON_RU['back'],
        callback_data="back")
    )
    return keyboard.as_markup()


def get_context_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text=LEXICON_RU['gpt'],
        callback_data="gpt")
    )
    keyboard.add(InlineKeyboardButton(
        text=LEXICON_RU['admin_contact'],
        url=f"https://t.me/{config.tg_bot.admin_username}")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def get_gpt_true_false_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text=LEXICON_RU['yes'],
        callback_data="yes")
    )
    keyboard.add(InlineKeyboardButton(
        text=LEXICON_RU['no'],
        callback_data="no")
    )
    keyboard.adjust(1)
    return keyboard.as_markup()
