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

async def check_student(pool , email):
    async with pool.acquire() as conn : 
        result = await conn.fetchval("SELECT id FROM students WHERE email = $1", email)
        return result is not None
    
async def get_user_email(pool , telegram_username):
    async with pool.acquire() as conn :
        return await conn.fetchval("SELECT email FROM users WHERE telegram_username = $1", telegram_username)

async def add_user_email(pool, telegram_username, email):
    async with pool.acquire() as conn:
        return await conn.execute(
            """
            INSERT INTO users(telegram_username, email) 
            VALUES ($1, $2) 
            ON CONFLICT (telegram_username) 
            DO UPDATE SET email = $2
            """,
            telegram_username, email
        )

async def save_issue(pool, telegram_username, email, message, is_suggestion=False):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO issues(telegram_username, email, message, is_suggestion) 
            VALUES ($1, $2, $3, $4)
            """,
            telegram_username, email, message, is_suggestion
        )


async def get_issues_by_email(pool, telegram_username, is_suggestion=False):
    async with pool.acquire() as conn:
        return await conn.fetch(
            """
            SELECT message, time FROM issues 
            WHERE telegram_username = $1 AND is_suggestion = $2
            ORDER BY time DESC
            """, 
            telegram_username, is_suggestion
        )