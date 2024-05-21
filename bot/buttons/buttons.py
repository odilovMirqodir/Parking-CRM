from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from api.api import GetRequests

db = GetRequests()


async def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Car Parking"),
                KeyboardButton(text="Search Car"),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


async def get_location():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Location", request_location=True),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


async def select_regions():
    buttons = []
    for region in await db.get_regions():
        button = InlineKeyboardButton(text=region['region'], callback_data=f"selectregion_{region['id']}")
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

    return keyboard
