from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
from handlers import user_router
import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = (os.environ.get("BOT_TOKEN")
     
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(user_router)
if __name__ == "__main__":
    print(100)
    dp.run_polling(bot)
