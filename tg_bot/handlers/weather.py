from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from tg_bot.kbrds import auth_kb

weather_router = Router()


@weather_router.message(Command("weather_voice"))  # /weather voice
async def weather_voice(message: types.Message):
    await message.answer("Бот умеет преобразовывать текст в речь и обратно. "
                         "Ткните /help для получения подробной информации.")
