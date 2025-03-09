import asyncio
import logging , os 

from dotenv import load_dotenv
from aiogram import Bot , Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.handle import router
from database import connect_db
from middleware import DatabaseMiddleware


load_dotenv()
bot = Bot(token=os.getenv('API_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher()

async def main():
    db_pool = await connect_db()

    dp.message.middleware(DatabaseMiddleware(db_pool))
    dp.include_router(router)
    
    try : 
        await dp.start_polling(bot)
    finally :
        await db_pool.close()

if __name__ == "__main__":
    try : 
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
