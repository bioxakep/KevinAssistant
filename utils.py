import os
from typing import Dict

import psutil

from config import faces_config
import json


def kill_process_by_name(name: str):
	for process in psutil.process_iter():
		if process.name() == name:
			process.kill()


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
