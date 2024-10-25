import aiohttp
from lexicon import LEXICON


async def fetch_tours(API_URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            return await response.json()  # Возвращаем JSON-ответ


def data_tours(tours):
    """Функция возвращает перечень туров (название и описание)."""
    result_tours = []
    for tour in tours:
        name = tour.get("name", LEXICON["Нет информации"])
        description = tour.get("description", LEXICON["Нет информации"])
        tour_str = f"Название тура - {name}, Описание тура {description}"
        result_tours.append(tour_str)
    return "\n".join(result_tours)
