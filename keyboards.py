# keyboards.py
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types

def generate_options_keyboard(options):
    """Генерирует инлайн-клавиатуру с вариантами ответов"""
    builder = InlineKeyboardBuilder()
    
    for i, option in enumerate(options):
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"answer_{i}"
        ))
    
    builder.adjust(1)  # По одной кнопке в строке
    return builder.as_markup()

def get_main_keyboard():
    """Возвращает главную клавиатуру"""
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🎯 Начать квиз"))
    builder.add(types.KeyboardButton(text="📊 Мой прогресс"))
    builder.add(types.KeyboardButton(text="🏆 Топ игроков"))
    builder.add(types.KeyboardButton(text="ℹ️ Помощь"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)