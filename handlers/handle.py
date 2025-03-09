from aiogram import F, Router
from aiogram.filters import CommandStart , Command
from aiogram.types import Message , CallbackQuery
from aiogram.fsm.state import StatesGroup, State 
from aiogram.fsm.context import FSMContext

import keyboards.keyboard as kb ; 

router = Router()

class Reg(StatesGroup):
    name = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message : Message) :
    await message.reply(f'Hello , {message.from_user.first_name}',
                        reply_markup=kb.second)

@router.message(Command('help'))
async def get_help(message:Message):
    await message.answer('This command name is help')

@router.message(F.text == 'How are you?')
async def how_are_you(message: Message):
    await message.answer('OK!', reply_markup=kb.about_us)

@router.callback_query(F.data == 'catalog')
async def catalog(callback : CallbackQuery):
    await callback.answer('You choose catalog', show_alert=True)
    await callback.message.answer('Hello')

@router.callback_query(F.data == 'basket')
async def basket(callback : CallbackQuery):
    await callback.answer('You choose basket') 
    await callback.message.edit_text('Hello', reply_markup=await kb.inline_cars())

    #edit-text to edit-caption if image

@router.message(Command('reg'))
async def reg_first_step(message : Message, state : FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите ваше имя:')

@router.message(Reg.name)
async def reg_second_step(message : Message , state : FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона')

@router.message(Reg.number)
async def reg_third_step(message : Message , state : FSMContext):
    await state.update_data(number = message.text)
    data = await state.get_data()
    await message.answer(f'Salem , Reg ushin rahmet : \nName:{data["name"]}\nNumber:{data["number"]}')
    await state.clear()

    