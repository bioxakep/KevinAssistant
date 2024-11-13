import subprocess
import sys
import time
import webbrowser
import psutil
import webrtcvad
from ollama_bot import OllamaBot
from voices import VoiceRecognizer, VoiceGenerator, VoiceRecorder
from config import voice_config


def kill_process_by_name(name: str):
    for process in psutil.process_iter():
        if process.name() == name:
            process.kill()


def run_kevin():
    # vad = webrtcvad.Vad()
    # vad.set_mode(3)
    ollama_mode = False
    smart_bot = OllamaBot()
    vcr = VoiceRecorder()
    vrz = VoiceRecognizer(model_path=voice_config.small_ru_model)
    vgr = VoiceGenerator(voice=VoiceGenerator.VOICE_RU_MALE)
    time.sleep(2)
    vgr.say_text("Привет. Чем помочь?")
    print('Привет. Чем помочь?')
    while True:
        command_text = ''
        while len(command_text) < 2:
            command_audio = vcr.get_audio_command()
            command_text = vrz.recognize_from_micro(command_audio)
        print('Запрос: ', command_text)
        time.sleep(2)
        if ollama_mode:
            response = smart_bot.ask(command_text)
            print('Ответ бота: ', response)
            vgr.say_text(response)
            ollama_mode = False
            continue
        if any([a in command_text for a in ['отдыхай', 'спасибо', 'ничего']]):
            vgr.say_text('Если что-то нужно, я рядом')
            sys.exit(0)
        elif 'кевин слушай' in command_text:
            vgr.say_text("Да, босс, какие будут указания?")
        elif 'ответь на вопрос' in command_text:
            vgr.say_text("Задавайте свой вопрос")
            ollama_mode = True
        elif 'открой ютюб' in command_text:
            webbrowser.open('https://www.youtube.com/')
        elif 'закрой сафари' in command_text:
            kill_process_by_name(name='Safari')
        elif 'открой терминал' in command_text:
            subprocess.call(['open', '-a', 'Terminal'])
        elif 'закрой терминал' in command_text:
            kill_process_by_name(name='Terminal')


if __name__ == '__main__':
    run_kevin()
    # subprocess.call(['open', '-a', 'Safari', '-n'])
