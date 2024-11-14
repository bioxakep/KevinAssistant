import subprocess
import sys
import time
import webbrowser
from ollama_bot import OllamaBot
from utils import kill_process_by_name, humanize_time
from voices import VoiceRecognizer, VoiceGenerator, VoiceRecorder
from faces import FaceDetector, key_pressed
from config import voice_config, faces_config
from collections import deque, Counter
from utils import read_labels


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


def run_kevin_video():
    face_detect_param = 5
    user_leave_timeout = 5
    current_user_id = 0
    user_coming_time = -1
    user_leave_time = -1
    users = read_labels()
    ollama_mode = False

    # Инициализация модулей
    vgr = VoiceGenerator(voice=VoiceGenerator.VOICE_RU_MALE)
    vcr = VoiceRecorder()
    vrz = VoiceRecognizer(model_path=voice_config.small_ru_model)
    fd = FaceDetector(camera_number=faces_config.camera_number, detect_interval=1)
    olm = OllamaBot()
    cam_users_list = deque(maxlen=face_detect_param)
    while len(cam_users_list) < face_detect_param:
        cam_user_id = fd.face_monitoring()
        cam_users_list.appendleft(cam_user_id)
    vgr.say_text("Добро пожаловать, Кевин готов к работе.")
    while True:
        if key_pressed('q'):
            break
        # Получаем аудиозапись команды
        command_audio = vcr.get_audio_command(timeout=0.2)
        # Преобразуем команду в текст
        command_text = vrz.recognize_from_micro(command_audio)
        # Получаем номер пользователя с камеры
        cam_user_id = fd.face_monitoring(show=False)
        # Добавляем пользователя в окно анализа
        cam_users_list.appendleft(cam_user_id)
        # Подсчитываем статистику с камеры
        counter = Counter(cam_users_list)
        # Получаем топ-пользователя
        new_user_id, new_user_count = counter.most_common(1)[0]
        # print("Current:", current_user_id, "New:", new_user_id, new_user_count)
        current_time = time.perf_counter()
        if current_user_id > 0 and new_user_id == 0 and new_user_count > face_detect_param // 2:
            # Если текущий пользователь отошел от компьютера и топ-пользователь стал нулевым
            if user_leave_time < 0:
                # И при этом мы только что это заметили
                user_leave_time = current_time
            elif current_time - user_leave_time > user_leave_timeout:
                # время отсутствия превышает timeout
                user_name = users[str(current_user_id)]
                # Вычисляем время пребывания пользователя за компьютером
                time_at_work = user_leave_time - user_coming_time
                time_at_work_humanize = humanize_time(time_at_work)
                vgr.say_text(f'До свидания, {user_name}, вы пробыли за компьютером {time_at_work_humanize}')
                print(f'До свидания, {user_name}, вы пробыли за компьютером {time_at_work_humanize}')
                user_coming_time = -1
                user_leave_time = -1
                current_user_id = new_user_id

        if 0 < new_user_id != current_user_id and new_user_count > face_detect_param // 2:
            # Если пользователь появился за компьютером и его обнаружили
            current_user_id = new_user_id
            user_name = users[str(current_user_id)]
            vgr.say_text(f'Привет, {user_name}')
            print(f'Привет, {user_name}')
            user_coming_time = current_time
        cam_users_list.pop()

        user_name = users.get(str(current_user_id), None)
        if len(command_text) > 4:
            if user_name is None:
                vgr.say_text("Извините, я вас не узнаю, представьтесь")
                continue
            if ollama_mode:
                response = olm.ask(command_text)
                print('Ответ бота: ', response)
                vgr.say_text(response)
                ollama_mode = False
                continue
            print('Запрос: ', command_text)
            if 'открой ютюб' in command_text:
                vgr.say_text(f"Выполняю, {user_name}")
                webbrowser.open('https://www.youtube.com/')
            elif 'закрой сафари' in command_text:
                vgr.say_text(f"Выполняю, {user_name}")
                kill_process_by_name(name='Safari')
            elif 'ответь на вопрос' in command_text:
                vgr.say_text("Задавайте свой вопрос")
                ollama_mode = True
            elif 'отдохни' in command_text:
                vgr.say_text(f"До свидания, {user_name}")
                break
    # Выход из программы
    fd.stop_monitoring()


if __name__ == '__main__':
    # run_kevin()
    # subprocess.call(['open', '-a', 'Safari', '-n'])
    run_kevin_video()
