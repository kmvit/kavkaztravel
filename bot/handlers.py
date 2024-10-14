from utils import data_tours, fetch_tours
from lexicon import LEXICON
from aiogram import Router
from aiogram.types import CallbackQuery

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import geo_keyboard, tag_keyboard

from aiogram import Router, types
import os
from dotenv import load_dotenv
load_dotenv()
router = Router()
user_router = Router()


URL = os.environ.get("URL")
URL_GEO = f'{URL}api/geo/'
URL_TOUR = f'{URL}api/tour/'
class Data(StatesGroup):
    """Машина состояний для реализации сценариев диалогов с пользователем."""

    geo = State()
    tag = State()


@user_router.message(Command('start'))
async def process_start_command(message: types.Message, state: FSMContext):
    """
    Функция срабатывает на команду /start/
    Возвращает клавиатуру с кнопками, где указана геолокация тура.
    """
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
    """ 
    Функция вызывается при нажатии кнопки пользователем на клавиатуре выбора геолокации тура.
    Возвращает клавиатуру выбора тэгов, присутствующих  для турор выбранной геолокации.
    """
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
            text=LEXICON["tag"],
            reply_markup=tag_keyboard(tags, callback.data))
    except Exception as err:
        print(f"{err}")
        await state.clear()
      

@user_router.callback_query(Data.tag)
async def get_tours_db(callback: CallbackQuery, state: FSMContext):
    """
    Функция вызывается при нажатии кнопки на клавиатуре выбора тэгов тура.
    Возвращает перечень туров по выбранному тэгу и геолокации.
    """
    try:
        tag, geo = callback.data.split(",")
        URL = f'{URL_TOUR}?geo={geo}&tag={tag}'
        tours = await fetch_tours(URL)
        if not tours:
            await callback.message.answer(
                    LEXICON["Нет информации"],
                )
            return
        await callback.message.answer(
                     data_tours(tours))
    except Exception as err:
        print(f"{err}")
    finally:
        await state.clear()