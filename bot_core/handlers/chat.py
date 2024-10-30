import io
import os.path
import datetime
import aiogram
from aiogram.filters import Command, StateFilter
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from ollama_bot import OllamaBot
from voice_engines import VoiceRecognizer, VoiceGenerator
from config import voice_config

chat_router = Router()


class ChatStates(StatesGroup):
	recognize_text = State()


@chat_router.message(StateFilter(ChatStates.recognize_text), F.content_type == "voice")
async def catch_audio_from_auth_user(message: types.Message, state: FSMContext):
	# Сохранить в файл, прочитать распознаванием, вывести текст.
	voice_file_info = await message.bot.get_file(message.voice.file_id)
	voice_ogg = io.BytesIO()
	await message.bot.download_file(voice_file_info.file_path, voice_ogg)
	file_prefix = str(message.from_user.id) + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	file_name = file_prefix + '_' + voice_file_info.file_path.split('/')[1].replace('.oga', '.ogg')
	voice_ogg_path = os.path.join(voice_config.audio_files, file_name)
	with open(voice_ogg_path, 'wb') as out_voice_file:
		out_voice_file.write(voice_ogg.read())
	voice_recognizer = VoiceRecognizer(model_path=voice_config.small_ru_model)
	recognized_text = voice_recognizer.recognize_from_tg(voice_ogg_path)
	smart_bot = OllamaBot()
	response = smart_bot.ask(recognized_text)
	voice_factory = VoiceGenerator()
	voice_file_path = voice_factory.text_to_audio_file(text=response)
	await message.bot.send_chat_action(message.from_user.id, aiogram.enums.ChatAction.UPLOAD_VOICE)
	await message.reply_audio(audio=FSInputFile(path=voice_file_path))
	await message.reply(text=response)
	await state.clear()


@chat_router.message(StateFilter(ChatStates.recognize_text))
async def catch_audio_from_auth_user(message: types.Message, state: FSMContext):
	smart_bot = OllamaBot()
	try:
		response = smart_bot.ask(message.text)
	except:
		response = 'Бот не запущен'
	voice_factory = VoiceGenerator()
	voice_file_path = voice_factory.text_to_audio_file(text=response)
	await message.bot.send_chat_action(message.from_user.id, aiogram.enums.ChatAction.UPLOAD_VOICE)
	await message.reply_audio(audio=FSInputFile(path=voice_file_path))
	await message.reply(text=response)
	await state.clear()


@chat_router.message(Command("ask"))
async def start_recognize_text(message: types.Message, state: FSMContext):
	await state.set_state(ChatStates.recognize_text)
	await message.reply(text='Отправьте боту голосовое с вопросом или задайте его текстом')
