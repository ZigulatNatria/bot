from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
"""
Кнопки клавиатуры 
"""
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Курс$"),
            KeyboardButton(text="История"),
        ],
        [
            KeyboardButton(text="Подписка")
        ]
    ],
    resize_keyboard=True
)