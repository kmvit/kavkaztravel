

import aiohttp

URL = 'http://localhost:8000/api//'


async def fetch_tours(API_URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            return await response.json()  # Возвращаем JSON-ответ
        
