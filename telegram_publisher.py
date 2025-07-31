import io
import os
import random
import time
from glob import glob

from dotenv import load_dotenv
from PIL import Image
from telegram import Bot
from urllib3.exceptions import HTTPError


PUBLISH_INTERVAL_HOURS = 4
SUPPORTED_EXTENSIONS = ['*.jpg', '*.jpeg', '*.png', '*.gif']
IMAGES_DIR = "images"
MAX_IMAGE_SIZE_MB = 10
DEFAULT_COMPRESSION_QUALITY = 85

def compress_image(image_path, quality=DEFAULT_COMPRESSION_QUALITY):
    with Image.open(image_path) as img:
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        return output

def handle_compression(image_path, max_size_mb=MAX_IMAGE_SIZE_MB, quality=DEFAULT_COMPRESSION_QUALITY):
    file_size = os.path.getsize(image_path) / (1024 * 1024)
    
    if file_size <= max_size_mb:
        with open(image_path, 'rb') as file:
            return file.read()

    try:
        compressed = compress_image(image_path, quality)
        new_size = len(compressed.getvalue()) / (1024 * 1024)
        print(f"Сжато: {file_size:.1f}МБ → {new_size:.1f}МБ")
        return compressed.getvalue()
    except (IOError, OSError, Image.DecompressionBombError) as e:
        print(f"Ошибка сжатия {image_path}: {e}")
        with open(image_path, 'rb') as file:
            return file.read()

def send_photo_to_telegram(bot, chat_id, photo_data, caption):
    with io.BytesIO(photo_data) as photo_stream:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo_stream,
            caption=caption
        )

def publish_single_image(bot, chat_id, image_path, interval_hours):
    try:
        photo_data = handle_compression(image_path)
        caption = f"🌌 {os.path.basename(image_path)}"
        
        send_photo_to_telegram(bot, chat_id, photo_data, caption)
        print(f"Отправлено: {image_path}")
        
        time.sleep(interval_hours * 3600)
    except (IOError, OSError) as e:
        print(f"Ошибка работы с файлом {image_path}: {e}")
        time.sleep(60)


def publish_images(bot, chat_id, interval_hours):
    images = []
    for ext in SUPPORTED_EXTENSIONS:
        images.extend(glob(os.path.join('images', '**', ext), recursive=True))
    
    if not images:
        print("Нет изображений для публикации! 🌌")
        return

    while True:
        random.shuffle(images)
        for image_path in images:
            publish_single_image(bot, chat_id, image_path, interval_hours)


def main():
    load_dotenv()
    config = {
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID')
    }
    
    bot = Bot(token=config['bot_token'])
    os.makedirs(IMAGES_DIR, exist_ok=True)

    print(f"🤖 Бот: {bot.get_me()}")
    print(f"🚀 Бот запущен. Интервал: {PUBLISH_INTERVAL_HOURS} ч")

    publish_images(bot, config['chat_id'], PUBLISH_INTERVAL_HOURS)


if __name__ == "__main__":
    main()