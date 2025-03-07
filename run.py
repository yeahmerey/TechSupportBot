import asyncio
import logging

from aiogram import Bot , Dispatcher
from config import API_TOKEN
from handlers.handle import router

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try : 
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
