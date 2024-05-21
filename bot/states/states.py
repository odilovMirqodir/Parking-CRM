from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    parking_id = State()
    car_name = State()
    car_number = State()
    location = State()
    search_car = State()
    region = State()
