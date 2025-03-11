from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery , FSInputFile
from aiogram.fsm.state import StatesGroup, State  
from aiogram.fsm.context import FSMContext
from asyncpg import Pool  
from database import *  

from datetime import datetime
import pandas as pd 
import os
import keyboards.keyboard as kb

router = Router()  
admin = os.getenv('ADMIN_ID')
class UserStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_issue = State()   
    waiting_for_suggestion = State()

@router.message(CommandStart())
async def start(message : Message , state : FSMContext):
    await state.clear()
    await state.update_data(telegram_username=message.from_user.username)
    await message.answer("Welcome to WSP TechSupportBot🔧\n✅To proceed, please enter your email address:\n(Example: example@kbtu.kz)")
    await state.set_state(UserStates.waiting_for_email)

@router.message(UserStates.waiting_for_email) 
async def process_email(message: Message, state: FSMContext, db: Pool):
    email = message.text.strip()
    telegram_username = (await state.get_data())["telegram_username"]
    is_available_student = await check_student(db , email)
    if is_available_student : 
        
        existing_email = await get_user_email(db, telegram_username); 
        
        if existing_email and existing_email != email:
            await message.answer(f"You already have an account with email: {existing_email}\nOnly one email per Telegram account is allowed.")
            await state.clear()
            return
        await add_user_email(db , telegram_username , email )
        await state.update_data(email=email)
        
        await message.answer(
            f"Email {email} successfully registered! What would you like to do?",
            reply_markup=kb.welcome
        )
        await state.clear()
    else : 
        await message.answer("Your email address was not found, please enter it again correctly :(\n(example@kbtu.kz)")    

@router.message(F.text == "Report a bug🐞")
async def report_bug(message : Message , state : FSMContext, db : Pool):
    telegram_username = message.from_user.username

    email = await get_user_email(db , telegram_username)

    if email:
        await state.update_data(email=email)
        await message.answer("Enter your problem:")
        await state.set_state(UserStates.waiting_for_issue)
    else:
        await message.answer("Please enter your email first: (Example: example@kbtu.kz)")
        await state.update_data(telegram_username=telegram_username)
        await state.set_state(UserStates.waiting_for_email)


@router.message(F.text == "Make a suggestion💎")
async def make_suggestion(message: Message, state: FSMContext, db: Pool):
    telegram_username = message.from_user.username
    
    email = await get_user_email(db, telegram_username)
    
    if email:
        await state.update_data(email=email)
        await message.answer("Enter your suggestion:")
        await state.set_state(UserStates.waiting_for_suggestion)
    else:
        await message.answer("Please enter your email first: (Example: example@kbtu.kz)")
        await state.update_data(telegram_username=telegram_username)
        await state.set_state(UserStates.waiting_for_email)

@router.message(UserStates.waiting_for_issue)
async def process_issue(message: Message, state: FSMContext, db: Pool):
    user_data = await state.get_data()
    email = user_data["email"]

    telegram_username = message.from_user.username
    issue_text = message.text
    
    await save_issue(db, telegram_username, email, issue_text)
    await message.answer("Your bug report has been saved. Thank you for helping us improve the system!", reply_markup=kb.welcome)
    await state.clear()

@router.message(UserStates.waiting_for_suggestion)
async def process_suggestion(message: Message, state: FSMContext, db: Pool):
    user_data = await state.get_data()
    email = user_data["email"]
    telegram_username = message.from_user.username
    suggestion_text = message.text
    
    await save_issue(db, telegram_username, email, suggestion_text, is_suggestion=True)
    await message.answer("Your suggestion has been saved. Thank you for your feedback!", reply_markup=kb.welcome)
    await state.clear()

@router.message(F.text == "My applications📜")
async def select_applications(message: Message, state: FSMContext, db: Pool):
    telegram_username = message.from_user.username
    
    email = await get_user_email(db, telegram_username)
    
    if not email:
        await message.answer("Please register your email first.")
        await state.update_data(telegram_username=telegram_username)
        await state.set_state(UserStates.waiting_for_email)
        return
    
    applications = await get_issues_by_email(db, telegram_username, is_suggestion=False)
    
    if applications:
        response = "Your submitted bug reports:\n\n"
        for idx, app in enumerate(applications, start=1):
            response += f"{idx}. {app['message']} ({app['time']})\n"
        await message.answer(response)
    else:
        await message.answer("You haven't submitted any bug reports yet.")

@router.message(F.text == "My suggestions📝")
async def select_suggestions(message: Message, state: FSMContext, db: Pool):
    telegram_username = message.from_user.username
    
    email = await get_user_email(db, telegram_username)
    
    if not email:
        await message.answer("Please register your email first.")
        await state.update_data(telegram_username=telegram_username)
        await state.set_state(UserStates.waiting_for_email)
        return
    
    suggestions = await get_issues_by_email(db, telegram_username, is_suggestion=True)
    
    if suggestions:
        response = "Your submitted suggestions:\n\n"
        for idx, app in enumerate(suggestions, start=1):
            response += f"{idx}. {app['message']} ({app['time']})\n"
        await message.answer(response)
    else:
        await message.answer("You haven't submitted any suggestions yet.")

@router.message(Command('getexcel'))
@router.message(F.text.lower() == "getexcel")
async def export_excel(message: Message, db: Pool):
    
    user_id = message.from_user.id

    if user_id != int(admin):
        await message.answer("you are not admin")
        return 

    try:
        issues = await get_all_issues(db)

        if not issues:
            await message.answer("No issues found in the database.")
            return

        data = []
        for issue in issues:
            time_value = issue['time']
            if hasattr(time_value, 'tzinfo') and time_value.tzinfo is not None:
                time_value = time_value.replace(tzinfo=None)
                
            data.append({
                'id': issue['id'],
                'telegram_username': issue['telegram_username'],
                'email': issue['email'],
                'message': issue['message'],
                'is_suggestion': issue['is_suggestion'],
                'time': time_value
            })

        df = pd.DataFrame(data)
        filename = f"issues_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        df.to_excel(filename, index=False)

        file = FSInputFile(filename)
        await message.answer_document(
            document=file,
            caption="Here is the exported data from issues"
        )
        os.remove(filename)

    except Exception as e:
        await message.answer(f"Error while exporting data: {str(e)}")