from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
)


def geo_keyboard(documents):
    """Клавиатура инлайн-кнопок с кнопками геолокации туров."""
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    if documents:
        for document in documents:
            button = document.get("geo_title", "!")
            buttons.append(
                InlineKeyboardButton(text=f"{button}", callback_data=f"{button}")
            )
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()


def tag_keyboard(documents, data):
    """Клавиатура инлайн-кнопок с кнопками тэгов туров."""
    kb_builder = InlineKeyboardBuilder()
    buttons: set[InlineKeyboardButton] = set()
    if documents:
        print(documents)
        for document in documents:
            button = document.get("tag", {}).get("name", None)
            print(button)
            buttons.add(
                InlineKeyboardButton(text=f"{button}", callback_data=f"{button},{data}")
            )
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()
