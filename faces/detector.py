# Function to recognize faces
import os
import time

import cv2
from config import faces_config
from utils import read_labels


def watch_faces():
	pass


def detect_faces():
	"""
	Метод для распознавания лиц с камеры
	:return:
	"""
	cap = cv2.VideoCapture(faces_config.camera_number)
	haar_path: str = os.path.join(faces_config.assets_path, str(faces_config.haarcascade_file_name))
	fc = cv2.CascadeClassifier(haar_path)
	recognizer = cv2.face.LBPHFaceRecognizer.create()
	model_file_path: str = os.path.join(faces_config.assets_path, str(faces_config.face_model_file_name))
	recognizer.read(model_file_path)
	users_ids = read_labels()
	# if name is not None:
	# 	users_ids = {k: v for k, v in users_ids.items() if name in v}
	while True:
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = fc.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))
		for (x, y, w, h) in faces:
			user_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
			if confidence < 50:
				cv2.putText(frame, users_ids[str(user_id)], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.imshow('Recognize Faces', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	# Release the camera and close windows
	cap.release()
	cv2.destroyAllWindows()


def detect_face_for_login(name: str, timeout: int = 10) -> bool:
	"""
	Метод для распознавания лица конкретного пользователя
	:param name: Имя пользователя в системе распознавания
	:param timeout: Время, отведенное на распознавание
	:return: Факт распознавания лица
	"""
	users_ids = read_labels()
	if name not in users_ids.values():
		print(f'Пользователя с именем {name} не найдено.')
		return False
	user_id_list = list(map(int, [k for k, v in users_ids.items() if name in v]))
	cap = cv2.VideoCapture(faces_config.camera_number)
	haar_path: str = os.path.join(faces_config.assets_path, str(faces_config.haarcascade_file_name))
	fc = cv2.CascadeClassifier(haar_path)
	recognizer = cv2.face.LBPHFaceRecognizer.create()
	model_file_path: str = os.path.join(faces_config.assets_path, str(faces_config.face_model_file_name))
	recognizer.read(model_file_path)
	start_recognize = time.perf_counter()
	print('Ожидание лица пользователя...')
	countdown = time.perf_counter() - start_recognize
	while countdown < timeout:
		countdown = time.perf_counter() - start_recognize
		print(f'\rОжидание лица пользователя...({int(timeout - countdown)})', end='')
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = fc.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))
		for (x, y, w, h) in faces:
			user_id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
			if confidence < 50 and user_id in user_id_list:
				cap.release()
				cv2.destroyAllWindows()
				print('Пользователь распознан')
				return True
		cv2.imshow('Recognize Faces', frame)
	# Release the camera and close windows
	cap.release()
	cv2.destroyAllWindows()
	print('Таймаут.')
