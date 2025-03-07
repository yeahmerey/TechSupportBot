from aiogram.types import (ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardButton , InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder , InlineKeyboardBuilder

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="My applications"), KeyboardButton(text="Частые вопросы(FAQ)")], 
        [KeyboardButton(text="Report a bug")],
        [KeyboardButton(text="About Us")]
    ],
    resize_keyboard=True, 
    input_field_placeholder='Select one : ')

settings = InlineKeyboardMarkup(inline_keyboard = [[
    InlineKeyboardButton(text="Youtube", url="https://youtube.com/@sudoteach")]
    ])

about_us = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Email" , url="mailto:yeahmerey@mail.ru?subject=Hello&body=I%20like%20your%20work%20and%20have%20a%20suggestion")],
    [InlineKeyboardButton(text="Telegram" , url="https://t.me/yeahmerey")],
    [InlineKeyboardButton(text="GitHub" , url="https://github.com/yeahmerey")]
])
