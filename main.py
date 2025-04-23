import requests
from urllib3.exceptions import HTTPError
import dotenv
import os
from save_apod import save_apod
from save_epic import save_EPIC
from spacex import fetch_spacex_last_launch
import urllib3
import ptbot
import telegram
import random
from glob import glob
import time
from PIL import Image
import io

bot = telegram.Bot(token='7036452912:AAEFRVX2SCkXPr4HvT41LB4oUq7d7lJ1jrc')
chat_id = "-1002572466444"

 

API_URL = 'https://api.spacexdata.com/v5/launches/'
response = requests.get(API_URL)
response.raise_for_status()
image_urls = []


PUBLISH_INTERVAL_HOURS = 4 # Здесь устанавливаем интервал публикации в часах (можно изменить на любое значение)
MAX_IMAGE_SIZE_MB = 10         # Максимальный размер фото (МБ)
IMAGE_QUALITY = 85             # Качество сжатия (1-100)

def get_image_paths(directory="images"):
    """Находит все изображения в папке и подпапках, включая EPIC"""
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif']
    images = []
    
    for ext in image_extensions:
        images.extend(glob(os.path.join(directory, '**', ext), recursive=True))
    
    return images

def compress_if_needed(image_path):
    """Сжимает изображение если оно больше MAX_IMAGE_SIZE_MB"""
    file_size = os.path.getsize(image_path) / (1024 * 1024)  # Размер в МБ
    
    if file_size <= MAX_IMAGE_SIZE_MB:
        return open(image_path, 'rb')
    
    try:
        with Image.open(image_path) as img:
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=IMAGE_QUALITY, optimize=True)
            new_size = len(output.getvalue()) / (1024 * 1024)
            print(f"Сжато: {file_size:.1f}МБ → {new_size:.1f}МБ")
            
            return output
    except Exception as e:
        print(f"Ошибка сжатия {image_path}: {e}")
        return open(image_path, 'rb')

def publish_images():
    """Основной цикл публикации фото"""
    image_paths = get_image_paths()
    
    if not image_paths:
        print("Нет изображений для публикации!🌌 ")
        return
    
    interval_seconds = PUBLISH_INTERVAL_HOURS * 3600
    
    while True:
        random.shuffle(image_paths)  # Перемешиваем массив
        
        for image_path in image_paths:
            try:
                # Подготовка фото
                photo = compress_if_needed(image_path)
                
                # Отправка
                bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=f"🌌 {os.path.basename(image_path)}"
                )
                print(f"Отправлено: {image_path}")
                
                # Закрываем файл/буфер
                if hasattr(photo, 'close'):
                    photo.close()
                
                time.sleep(interval_seconds)
                
            except Exception as e:
                print(f"Ошибка отправки {image_path}: {e}")
                time.sleep(60)  # Пауза при ошибке


def main():


    dotenv.load_dotenv()
    fetch_spacex_last_launch("images")
    save_apod()
    save_EPIC()
    updates = bot.get_updates()
    print(bot.get_me())
    print(f"🚀 Бот запущен. Интервал: {PUBLISH_INTERVAL_HOURS} ч")
    print(f"🤖 Бот: {bot.get_me()}")
    publish_images()




if __name__ == "__main__":
    main()