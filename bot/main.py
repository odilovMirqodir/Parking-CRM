import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from config.config import BOT_TOKEN
from aiogram.fsm.context import FSMContext
from states.states import *
from aiogram import types
from buttons.buttons import *
from api.api import GetRequests

TOKEN = BOT_TOKEN

dp = Dispatcher()
db = GetRequests()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Quyidagilardan birini tanlang", reply_markup=await main_menu())


@dp.message(lambda message: message.text == "Car Parking")
async def registration_start(message: types.Message, state: FSMContext):
    result = await db.get_parking_is_false()
    first_inactive_parking_count = None

    for item in result:
        if not item['is_active']:
            first_inactive_parking_count = item['parking_count']
            break

    if first_inactive_parking_count is not None:
        await db.parking_id_true(first_inactive_parking_count)
        await message.answer(
            f"*Joylashingiz kerak bo'lgan joy: {first_inactive_parking_count} \n\nMashina nomini kiriting*",
            parse_mode='markdown',
            reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Form.parking_id)
        await state.update_data(parking_id=first_inactive_parking_count)
        await state.set_state(Form.car_name)
    else:
        await message.answer("Uzr, hozircha aktiv yo'q parking joyi topilmadi. Iltimos, keyinroq urinib ko'ring.")


@dp.message(Form.car_name)
async def process_parking_id(message: Message, state: FSMContext) -> None:
    await state.update_data(car_name=message.text)
    await message.answer("*Mashina Win raqamini kiriting*", parse_mode='markdown')
    await state.set_state(Form.car_number)


@dp.message(Form.car_number)
async def process_car_number(message: Message, state: FSMContext) -> None:
    if message.text.lower().startswith('x') and len(message.text) < 7:
        await state.update_data(car_number=message.text)
        data = await state.get_data()
        if 'location' in data and data['location'] is not None:
            await message.answer(f"*Regionni tanlang*", reply_markup=await select_regions())
            await state.set_state(Form.region)
        else:
            await state.set_state(Form.location)
            await message.answer("*Mashina qoyilgan locatsiyani yuboring*", parse_mode='markdown',
                                 reply_markup=await get_location())
    else:
        await message.answer(f"Iltimos Raqam X bilan boshlanib 7ta sondan iborat bolishi kerak")


@dp.message(Form.location)
async def process_location(message: Message, state: FSMContext) -> None:
    location = message.location
    await state.update_data(location=[location.latitude, location.longitude])
    await message.answer(f"*Mashina yuboriladigan region*", reply_markup=await select_regions(), parse_mode='markdown')
    await state.set_state(Form.region)


@dp.callback_query(Form.region, lambda call: call.data.startswith('selectregion_'))
async def process_region(call: types.CallbackQuery, state: FSMContext) -> None:
    region = int(call.data.split('_')[1])
    await state.update_data(region=region)
    data = await state.get_data()
    parking_id = data['parking_id']
    car_name = data['car_name']
    car_number = data['car_number']
    lat, lon = data['location'][0], data['location'][1],
    region = data['region']
    response = await db.create_car_number(parking_id, car_name, car_number, lat, lon, region)
    await state.clear()
    if response:
        await call.message.answer(f"*Mashina Parkinga joylandi*", reply_markup=await main_menu(), parse_mode='markdown')
    else:
        await call.message.answer('error')


@dp.message(lambda message: message.text == "Search Car")
async def search_car(message: types.Message, state: FSMContext):
    await message.answer("*Car number*", parse_mode='markdown', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.search_car)


@dp.message(Form.search_car)
async def serch_car(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(search_car=message.text)
    data = await state.get_data()
    car_number = data['search_car']
    car_search = await db.car_search_by_number(car_number)
    if car_number == car_search['car_id']:
        await db.parking_id_false(car_search['parking_number'])
        await db.auto_active_false(car_number)
        await state.clear()
        text = f"Parking qilingan joyi: {car_search['parking_number']}\nMashina Raqami:{car_search['car_id']}"
        await message.answer(text, parse_mode='markdown', reply_markup=await main_menu())
        await bot.send_location(message.chat.id, latitude=car_search['lat'], longitude=car_search['long'])
    else:
        await message.answer("Bunday id toplmadi")


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
