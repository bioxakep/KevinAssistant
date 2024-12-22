import os.path
import subprocess

from ollama import Client
from config import ollama_config


class OllamaBot:
	SMALL_MODEL = 'llama3.2:1b'
	SMART_MODEL = 'llama3.1:8b'

	def __init__(self, bin_path: str, model=None):
		if not os.path.exists(bin_path):
			raise FileNotFoundError(bin_path)
		self.__bin_path: str = bin_path
		self.__models_list = list()
		p = subprocess.Popen([self.__bin_path, 'list'], stdout=subprocess.PIPE)
		line = p.stdout.readline().decode('utf-8')
		while len(line) > 0:
			if ':' in line:
				self.__models_list.append(line.split(' ')[0])
			line = p.stdout.readline().decode('utf-8')
		self.__current_model = self.__models_list[0]
		self.__ollama_service = subprocess.Popen([bin_path, 'serve'], stdout=subprocess.PIPE)
		self.__client = Client()

	def __del__(self):
		self.__ollama_service.kill()

	def ask(self, query_text: str, model=None):
		message = {'role': 'user', 'content': query_text}
		response = self.__client.chat(model=model or self.__current_model, messages=[message])
		return response['message']['content']

	def select_model(self, model_name: str):
		if model_name not in self.__models_list:
			raise ValueError(f'Модель {model_name} не найдена')
		self.__current_model = model_name

	@property
	def models(self):
		return self.__models_list


if __name__ == '__main__':
	bot = OllamaBot(ollama_config.binary_path)
	csv_file = ('Дата и время;Телефон;Контакт\n' + '2020-01-01;+7(495)123-45-67;+7(495)123-42-67\n' * 1000000)
	res = bot.ask(query_text="Сколько соединений и со сколькими абонентами описано в следующем табличном файле?: " + csv_file, model=bot.SMART_MODEL)
	print(res)
