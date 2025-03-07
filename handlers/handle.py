from aiogram import F, Router
from aiogram.filters import CommandStart , Command
from aiogram.types import Message 

import keyboards.keyboard as kb ; 

router = Router()

@router.message(CommandStart())
async def cmd_start(message : Message) :
    await message.reply(f'Hello , {message.from_user.first_name}',
                        reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message:Message):
    await message.answer('This command name is help')

@router.message(F.text == 'How are you?')
async def how_are_you(message: Message):
    await message.answer('OK!', reply_markup=kb.about_us)
