import subprocess

from ollama import Client


class OllamaBot:
	SMALL_MODEL = 'llama3.2:1b'
	SMART_MODEL = 'llama3.1:latest'

	def __init__(self, model=None):
		import psutil
		# for p in psutil.process_iter(['pid', 'name']):
		# 	if 'ollama' in p.info['name']:
		# 		p.kill()
		self.__ollama_service = subprocess.Popen(['/usr/local/bin/ollama', 'serve'], stdout=subprocess.PIPE)
		self.__client = Client()

	def __del__(self):
		self.__ollama_service.kill()

	def ask(self, query_text: str, model: str = None):
		message = {'role': 'user', 'content': query_text}
		response = self.__client.chat(model=self.SMART_MODEL or model, messages=[message])
		return response['message']['content']


if __name__ == '__main__':
	# run_models()
	bot = OllamaBot()
	print(bot.ask('Сколько лет Байдену?'))



