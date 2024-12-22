import json
import os
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
from config import voice_config


class VoiceRecognizer:
	FREQ = 16000

	def __init__(self, model_path: str):
		""" Инициализация модели распознавания с установкой частоты дискретизации аудиопотока """
		self.__model = Model(model_path)
		self.__recognizer = KaldiRecognizer(self.__model, VoiceRecognizer.FREQ)
		# AudioSegment.converter = '/opt/homebrew/Cellar/ffmpeg/7.0_1/bin/ffmpeg'

	def recognize_ogg(self, ogg_file_path: str):
		voice_wav_path = os.path.join(
			voice_config.audio_files,
			os.path.basename(ogg_file_path.replace('.ogg', '.wav'))
		)
		audio = AudioSegment.from_ogg(ogg_file_path)
		audio = audio.set_sample_width(2).set_frame_rate(16000)
		audio.export(voice_wav_path, format="wav")
		audio = AudioSegment.from_wav(voice_wav_path)
		self.__recognizer.AcceptWaveform(audio.raw_data)
		os.remove(voice_wav_path)
		ru_res = json.loads(self.__recognizer.FinalResult())
		if 'text' in ru_res.keys():
			return f"Распознан текст: {ru_res.get('text')}"
		return "Не распознано."

	def recognize_from_micro(self, audio_data):
		# audio = AudioSegment.from_wav(wav_file_path)
		try:
			self.__recognizer.AcceptWaveform(audio_data)
		except TypeError:
			return ""
		# os.remove(voice_wav_path)
		ru_res = json.loads(self.__recognizer.FinalResult())
		if 'text' in ru_res.keys():
			return ru_res.get('text')
		return ""
