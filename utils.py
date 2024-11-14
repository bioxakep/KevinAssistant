import os
import subprocess
from typing import Dict

import psutil

from config import faces_config
import json


def kill_process_by_name(name: str):
	for process in psutil.process_iter():
		if process.name() == name:
			process.kill()


def humanize_time(time_at_work):
	days = time_at_work // 86400
	hours = (time_at_work - days * 86400) // 3600
	minutes = (time_at_work - days * 86400 - hours * 3600) // 60
	seconds = time_at_work - days * 86400 - hours * 3600 - minutes * 60
	human_time = f'{int(seconds)} секунд' if seconds > 0 else ''
	human_time = (f'{int(minutes)} минут' if minutes > 0 else '') + human_time
	human_time = (f'{int(hours)} часов' if hours > 0 else '') + human_time
	human_time = (f'{int(days)} дней' if days > 0 else '') + human_time
	if len(human_time) > 0:
		return human_time
	else:
		return 'Мало времени'


def check_audio_playing_status():
	res = subprocess.check_output(["pmset", "-g"]).decode()
	res = res[res.find("\n sleep"):].replace("\n", "", 1)
	res = res[:res.find("\n")]
	res = res[res.find("(") + 1: res.find(")")]
	print(res)
	result = res.count(",")
	print(result > 3)


def read_labels() -> Dict:
	labels_path: str = os.path.join(
		str(faces_config.assets_path), str(faces_config.labels_file_name)
	)
	if not os.path.exists(labels_path):
		raise FileNotFoundError(f"Labels file not found at {labels_path}")
	data: Dict = json.load(open(labels_path))
	return data


def save_labels(data: Dict) -> None:
	labels_path: str = os.path.join(
		str(faces_config.assets_path), str(faces_config.labels_file_name)
	)

	with open(labels_path, "w") as f:
		json.dump(data, f)


if __name__ == '__main__':
	check_audio_playing_status()
