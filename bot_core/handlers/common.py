from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from bot_core.kbrds import auth_kb

common_router = Router()


@common_router.message(Command("start"))  # /start
async def cmd_start(message: types.Message):
    await message.answer("Бот умеет преобразовывать текст в речь и обратно. "
                         "Ткните /help для получения подробной информации.")
    # await message.answer("Привет! Зарегистрируемся?", reply_markup=auth_kb.get_auth_kb())


@common_router.message(Command("help"))  # /start
async def cmd_help(message: types.Message):
    await message.answer("/voice [ТЕКСТ] - преобразует текст в речь, в ответ вы получите аудиофайл.\n"
                         "/text - команда для преобразования аудиозаписи в текст.")


@common_router.message(Command("id"))  # /id
async def cmd_id(message: types.Message):
    await message.answer(f"Привет! Твой ID: {message.from_user.id}")


@common_router.message(F.text)
async def user_text(message: types.Message):
    await message.reply("Не понял Вас.")


@common_router.message(F.sticker)
async def cmd_stickers(message: types.Message):
    await message.reply("Зачем слать мне стикеры?")


@common_router.message(F.photo)
async def cmd_photo(message: types.Message):
    await message.reply("Зачем слать мне фото?")


@common_router.message(F.animation)
async def cmd_animation(message: types.Message):
    await message.reply("Зачем слать мне анимации всякие?")
