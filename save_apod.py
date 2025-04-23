import os
from datetime import datetime
import requests
from urllib.parse import urlparse
from PIL import Image
from save_image import save_image


API_URL = 'https://api.spacexdata.com/v5/launches/'
response = requests.get(API_URL)
response.raise_for_status()


def save_apod():
    api_token = os.environ.get('api_token')

    count = 30
    nasa_url = f"https://api.nasa.gov/planetary/apod?api_key={api_token}&count={count}"
    file_path = "images"

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    try:
        response = requests.get(nasa_url)
        response.raise_for_status()
        image_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    for index, item in enumerate(image_data):
        image_url = item.get('url')

        try:
            parsed_url = urlparse(image_url)
            file_extension = os.path.splitext(parsed_url.path)[1]

            if not file_extension:
                print(f"Skipping {image_url}: No file extension found")
                continue

            file_name = f"nasa_apod_{index + 1}{file_extension}"
            full_file_path = os.path.join(file_path, file_name)

            save_image(image_url, full_file_path)


        except Exception as e:
            print(f"Error processing item {index}: {e}")

