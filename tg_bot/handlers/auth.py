from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

auth_router = Router()


class AuthState(StatesGroup):
    auth_without_phone = State()
    auth_with_phone = State()


@auth_router.message(F.text.lower() == "без предоставления номера")
async def auth_without_phone(message: types.Message, state: FSMContext):
    await state.set_state(AuthState.auth_without_phone)
    await message.reply(f"Твой ID {message.from_user.id}. Обратись с этим к администратору.",
                        reply_markup=types.ReplyKeyboardRemove())


@auth_router.message(F.contact)
async def auth_with_phone(message: types.Message, state: FSMContext):
    user_phone = message.contact.phone_number
    user_id = message.contact.user_id
    await state.set_state(AuthState.auth_with_phone)
    await state.set_data({'user_phone': user_phone})
    await message.reply(f"Теперь ты в теме с номером {message.contact.phone_number}",
                        reply_markup=types.ReplyKeyboardRemove())
