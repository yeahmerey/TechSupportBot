from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State  
from aiogram.fsm.context import FSMContext
from asyncpg import Pool  
from database import add_user_email , save_issue

import keyboards.keyboard as kb

router = Router()  

class UserStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_issue = State()   

@router.message(CommandStart()) 
async def start(message: Message, state: FSMContext):
    await message.answer('Salem, e-mail engiz:')
    await state.update_data(telegram_username=message.from_user.username)
    await state.set_state(UserStates.waiting_for_email)  

@router.message(UserStates.waiting_for_email) 
async def process_email(message: Message, state: FSMContext, db: Pool):
    data = await state.get_data()
    telegram_username = data["telegram_username"]
    email = message.text   
    await add_user_email(db, telegram_username, email)
    await state.update_data(email=email)  
    await message.answer("Problemandy ait: ")
    await state.set_state(UserStates.waiting_for_issue)  

@router.message(UserStates.waiting_for_issue) 
async def process_issue(message: Message, state: FSMContext, db: Pool):
    user_data = await state.get_data()
    telegram_username = user_data["telegram_username"]
    issue_text = message.text  
    await save_issue(db, telegram_username, issue_text)
    await message.answer("Senin jalobyn saqtaldy")
    await state.clear()