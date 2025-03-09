from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from asyncpg import Pool

class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, pool: Pool):
        super().__init__()
        self.pool = pool
        
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data["db"] = self.pool
        return await handler(event, data)