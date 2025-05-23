import os
import random
import time
import io
import save_apod
import save_epic
from spacex import fetch_spacex_last_launch
from glob import glob
from PIL import Image
from dotenv import load_dotenv
from telegram import Bot
from urllib3.exceptions import HTTPError


def load_environment():
    load_dotenv()
    return {
        'BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'CHAT_ID': os.getenv('TELEGRAM_CHAT_ID')
    }


def initialize_bot(token):
    return Bot(token=token)


def get_supported_extensions():
    return ['*.jpg', '*.jpeg', '*.png', '*.gif']


def find_images_with_extension(directory, extension):
    return glob(os.path.join(directory, '**', extension), recursive=True)


def get_all_image_paths(directory="images"):
    image_extensions = get_supported_extensions()
    images = []

    for ext in image_extensions:
        images.extend(find_images_with_extension(directory, ext))

    return images


def get_file_size_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)


def compress_image(image_path, quality=85):
    with Image.open(image_path) as img:
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        return output


def handle_compression(image_path, max_size_mb=10, quality=85):
    file_size = get_file_size_mb(image_path)

    if file_size <= max_size_mb:
        return open(image_path, 'rb')

    try:
        compressed = compress_image(image_path, quality)
        new_size = len(compressed.getvalue()) / (1024 * 1024)
        print(f"Сжато: {file_size:.1f}МБ → {new_size:.1f}МБ")
        return compressed
    except Exception as e:
        print(f"Ошибка сжатия {image_path}: {e}")
        return open(image_path, 'rb')


def send_photo_to_telegram(bot, chat_id, photo, caption):
    bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=caption
    )


def close_photo_resource(photo):
    if hasattr(photo, 'close'):
        photo.close()


def publish_single_image(bot, chat_id, image_path, interval_hours):
    try:
        photo = handle_compression(image_path)
        caption = f"🌌 {os.path.basename(image_path)}"

        send_photo_to_telegram(bot, chat_id, photo, caption)
        print(f"Отправлено: {image_path}")

        close_photo_resource(photo)
        time.sleep(interval_hours * 3600)
    except Exception as e:
        print(f"Ошибка отправки {image_path}: {e}")
        time.sleep(60)


def publish_images(bot, chat_id, interval_hours):
    image_paths = get_all_image_paths()

    if not image_paths:
        print("Нет изображений для публикации!🌌 ")
        return

    while True:
        random.shuffle(image_paths)
        for image_path in image_paths:
            publish_single_image(bot, chat_id, image_path, interval_hours)


def main():
    config = load_environment()
    bot = initialize_bot(config['BOT_TOKEN'])
    
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    save_apod.save_apod()
    save_epic.save_EPIC()
    fetch_spacex_last_launch(images_dir)

    PUBLISH_INTERVAL_HOURS = 4

    print(f"🤖 Бот: {bot.get_me()}")
    print(f"🚀 Бот запущен. Интервал: {PUBLISH_INTERVAL_HOURS} ч")

    publish_images(bot, config['CHAT_ID'], PUBLISH_INTERVAL_HOURS)


if __name__ == "__main__":
    main()