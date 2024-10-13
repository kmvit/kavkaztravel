from utils import fetch_tours
from lexicon import LEXICON
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from aiogram.fsm.state import State, StatesGroup



from keyboards import geo_keyboard, tag_keyboard

from aiogram import Router, types

router = Router()
user_router = Router()

from aiogram.filters import Command

URL_GEO = 'http://127.0.0.1:8000/api/geo/'
URL_TOUR = 'http://127.0.0.1:8000/api/tour/'
class Data(StatesGroup):
    """Машина состояний для реализации сценариев диалогов с пользователем."""

    geo = State()
    tag = State()
    gpt = State()

    """Машина состояний для реализации сценариев диалогов с пользователем."""


@user_router.message(Command('start'))
async def process_start_command(message: types.Message, state: FSMContext):
    """Получение тем из БД."""
    print(1000)
    try:
        geos = await fetch_tours(URL_GEO)
        if not geos:
            await message.answer(
                    LEXICON["Нет информации"],
                )
            return
        await state.set_state(Data.geo)
        await message.answer(
            text=LEXICON["geo"],
            reply_markup=geo_keyboard(geos))
    except Exception as err:
        print(f"{err}")

@user_router.callback_query(Data.geo)
async def get_geo_db(callback: CallbackQuery, state: FSMContext):
    print(1000, callback.data)
    try:
        URL = f'{URL_TOUR}?geo={callback.data}'
        tags = await fetch_tours(URL)
        print(tags, 1000)
        if not tags:
            await callback.message.answer(
                    LEXICON["Нет информации"],
                )
            return
        await state.set_state(Data.tag)
        await callback.message.answer(
            text=LEXICON["geo"],
            reply_markup=tag_keyboard(tags, callback.data))
    except Exception as err:
        print(f"{err}")
        await state.clear()

@user_router.callback_query(Data.tag)
async def get_title_db(callback: CallbackQuery, state: FSMContext):
    """Получение тем из БД."""
    try:
        tag, geo = callback.data.split(",")
        URL = f'{URL_TOUR}?geo={geo}&tag={tag}'
        print(tag, geo, URL)
        tours = await fetch_tours(URL)
        if not tours:
            await callback.message.answer(
                    LEXICON["Нет информации"],
                )
            return
        print(tours)
        result_tours = []
        for tour in tours:
            name = tour.get('name', LEXICON["Нет информации"])
            description = tour.get('description', LEXICON["Нет информации"])
            tour_str = f"Название тура - {name}, Описание тура {description}"
            result_tours.append(tour_str)
        data_tours = '\n'.join(result_tours)
        print(data_tours)
        await callback.message.answer(
                     data_tours)
    except Exception as err:
        print(f"{err}")
        await state.clear()