import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def connect_db():
    return await asyncpg.create_pool(
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME'),
        host = os.getenv('DB_HOST'),
        port = os.getenv('DB_PORT')
    )

async def add_user_email(pool, telegram_username, email):
    async with pool.acquire() as conn:
        return await conn.execute(  # Make sure to use 'await' here
            "INSERT INTO users(telegram_username, email) VALUES ($1, $2) ON CONFLICT (telegram_username) DO NOTHING",
            telegram_username, email
        )
async def save_issue(pool , telegram_username , message):
    async with pool.acquire() as conn : 
        await conn.execute(
            "INSERT INTO issues(telegram_username , message) VALUES ($1, $2)",
            telegram_username , message
        )
