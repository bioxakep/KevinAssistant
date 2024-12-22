import subprocess
import time
import webbrowser

import rumps

from config import voice_config, ollama_config
from main_kevin import kill_process_by_name
from ollama_bot import OllamaBot
from voices import VoiceRecorder, VoiceRecognizer, VoiceGenerator


class KevinApp(rumps.App):
	def __init__(self):
		super(KevinApp, self).__init__("KevinApp")
		kevin_item = rumps.MenuItem(title="Run Kevin", callback=self.run_kevin, icon="assets/micro.png")
		self.menu = [kevin_item, "Option 2", "Option 3"]
		self.icon = "assets/kevin.png"
		self.__smart_bot = OllamaBot(ollama_config.binary_path)
		self.__vcr = VoiceRecorder()
		self.__vrz = VoiceRecognizer(model_path=voice_config.small_ru_model)
		self.__vgr = VoiceGenerator(voice=VoiceGenerator.VOICE_RU_MALE)
		self.__ollama_mode = False

	def run_kevin(self, data):
		print('Running Kevin')
		vg = VoiceGenerator(voice=VoiceGenerator.VOICE_RU_MALE)
		vg.say_text("Привет. Чем помочь?")
		time.sleep(1)
		while True:
			command_text = ''
			while len(command_text) < 2:
				command_audio = self.__vcr.get_audio_command()
				command_text = self.__vrz.recognize_from_micro(command_audio)
			print('Запрос: ', command_text)
			time.sleep(2)
			self.run_command(command_text)

	def run_command(self, command_text: str):
		if self.__ollama_mode:
			response = self.__smart_bot.ask(command_text)
			# print('Ответ бота: ', response)
			self.__vgr.say_text(response)
			self.__ollama_mode = False
			return
		if any([a in command_text for a in ['отдыхай', 'спасибо', 'ничего']]):
			self.__vgr.say_text('Если что-то нужно, я рядом')
			return
		elif 'кевин слушай' in command_text:
			self.__vgr.say_text("Да, босс, какие будут указания?")
		elif 'ответь на вопрос' in command_text:
			self.__vgr.say_text("Задавайте свой вопрос")
			self.__ollama_mode = True
		elif 'открой ютюб' in command_text:
			webbrowser.open('https://www.youtube.com/')
		elif 'закрой сафари' in command_text:
			kill_process_by_name(name='Safari')
		elif 'открой терминал' in command_text:
			subprocess.call(['open', '-a', 'Terminal'])
		elif 'закрой терминал' in command_text:
			kill_process_by_name(name='Terminal')

	@rumps.clicked("Option 2")
	def on_option2(self, _):
		rumps.notification(title="Option 2", subtitle="Clicked", message="You clicked option 2")

	@rumps.clicked("Option 3")
	def on_option3(self, _):
		rumps.notification(title="Option 3", subtitle="Clicked", message="You clicked option 3")


if __name__ == "__main__":
	app = KevinApp()
	app.run()
