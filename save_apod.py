import os
import requests
from urllib.parse import urlparse
from PIL import Image
from save_image import save_image
from datetime import datetime


API_URL = 'https://api.spacexdata.com/v5/launches/'
response = requests.get(API_URL)
response.raise_for_status()


def get_nasa_api_url(api_token, count=30):
    return f"https://api.nasa.gov/planetary/apod?api_key={api_token}&count={count}"


def create_images_directory(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def fetch_nasa_data(nasa_url):
    try:
        response = requests.get(nasa_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def get_file_extension_from_url(image_url):
    parsed_url = urlparse(image_url)
    return os.path.splitext(parsed_url.path)[1]


def process_apod_item(item, index, file_path):
    image_url = item.get('url')
    try:
        file_extension = get_file_extension_from_url(image_url)

        if not file_extension:
            print(f"Skipping {image_url}: No file extension found")
            return

        file_name = f"nasa_apod_{index + 1}{file_extension}"
        full_file_path = os.path.join(file_path, file_name)

        save_image(image_url, full_file_path)
    except Exception as e:
        print(f"Error processing item {index}: {e}")


def save_apod():
    api_token = os.environ.get('api_token')
    nasa_url = get_nasa_api_url(api_token)
    file_path = "images"

    create_images_directory(file_path)
    image_data = fetch_nasa_data(nasa_url)

    if image_data:
        for index, item in enumerate(image_data):
            process_apod_item(item, index, file_path)
