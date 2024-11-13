import os
from typing import Dict
from config import app_config
import json


def read_labels() -> Dict:
	labels_path: str = os.path.join(
		str(app_config.assets_path), str(app_config.labels_file_name)
	)
	if not os.path.exists(labels_path):
		raise FileNotFoundError(f"Labels file not found at {labels_path}")
	data: Dict = json.load(open(labels_path))
	return data


def save_labels(data: Dict) -> None:
	labels_path: str = os.path.join(
		str(app_config.assets_path), str(app_config.labels_file_name)
	)

	with open(labels_path, "w") as f:
		json.dump(data, f)
