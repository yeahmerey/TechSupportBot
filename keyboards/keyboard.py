from aiogram.types import (ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardButton , InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder , InlineKeyboardBuilder


welcome = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="My applications📜"), KeyboardButton(text="My suggestions📝")], 
        [KeyboardButton(text="Report a bug🐞"), KeyboardButton(text="Make a suggestion💎")],
        [KeyboardButton(text="About me🦺")]
    ], 
    resize_keyboard=True ,
    input_field_placeholder="Select one :"
)
