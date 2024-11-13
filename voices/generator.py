import asyncio
import os
import pyttsx3
from datetime import datetime
from pydub import AudioSegment
from config import voice_config


class VoiceGenerator:
	VOICE_RU_MALE = 'com.apple.voice.enhanced.ru-RU.Yuri'
	VOICE_RU_FEMALE = 'com.apple.voice.enhanced.ru-RU.Milena'

	def __init__(self, voice: str | None = None, sex: str = 'Female', age: int | None = None):
		self.__engine = pyttsx3.init()
		self.__engine.setProperty('rate', 190)
		self.__engine.setProperty('volume', 1.0)
		self.__voices = list(map(lambda x: x.id, self.__engine.getProperty('voices')))
		if voice is not None and voice in self.__voices:
			self.__engine.setProperty('voice', voice)
		else:
			self.__engine.setProperty('voice', VoiceGenerator.VOICE_RU_FEMALE)

	def say_text(self, text: str):
		# self.__engine.stop()
		# self.__engine.startLoop(False)
		self.__engine.say(text)
		self.__engine.runAndWait()
		# self.__engine.endLoop()

	def text_to_audio_file(self, text: str):
		file_name: str = 'FROM_TEXT_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.wav'
		temp_audio_file_path: str = os.path.join(voice_config.audio_files, file_name)
		self.__engine.save_to_file(text=text, filename=temp_audio_file_path)
		self.__engine.runAndWait()
		audio_file = AudioSegment.from_file(temp_audio_file_path)
		print(audio_file.channels, audio_file.duration_seconds)
		ogg_file_path: str = temp_audio_file_path.replace('.wav', '.ogg')
		audio_file.export(out_f=ogg_file_path, format='ogg', codec='libopus')
		del audio_file
		os.remove(temp_audio_file_path)
		return ogg_file_path

	def get_voices(self, synthesis: bool = False):
		if not synthesis:
			return self.__voices
		return list(filter(lambda x: 'synthesis' in x, self.__voices))

	def set_voice(self, voice_id: str):
		if voice_id not in self.get_voices():
			return False
		self.__engine.setProperty('voice', voice_id)
		self.say_text("Новый голос установлен")


if __name__ == '__main__':
	voice_generator = VoiceGenerator()
	voice_generator.say_text("Hello")
