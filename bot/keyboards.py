from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from lexicon import BUTTONS

def start_keyboard():
    """Клавиатура при старте бота."""
    button_1 = InlineKeyboardButton(
        text=BUTTONS["Геолокация"],
        callback_data="geo"
    )
    button_2 = InlineKeyboardButton(
        text=BUTTONS["Тэги"],
        callback_data="tag"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1],
                         [button_2],
                          ])
    return keyboard

def geo_keyboard(documents):
    """Клавиатура инлайн-кнопок  для получения запроса geo_title."""
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if documents:
        print(documents)
        for z in documents:
            button = z.get('geo_title', '!')
            buttons.append(InlineKeyboardButton(
                text=f"{button}",
                callback_data=f"{button}"))
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()


def tag_keyboard(documents, data):
    """Клавиатура инлайн-кнопок  для получения запроса geo_title."""
    kb_builder = InlineKeyboardBuilder()
    buttons: set[InlineKeyboardButton] = set()
    if documents:
        print(documents)
        for z in documents:
            button = z.get('tag', {}).get('name', None)
            print(button)
            buttons.add(InlineKeyboardButton(
                text=f"{button}",
                callback_data=f"{button},{data}"))
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()