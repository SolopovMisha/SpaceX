
import requests
import os
from save_image import save_image


API_URL = 'https://api.spacexdata.com/v5/launches/'
response = requests.get(API_URL)
response.raise_for_status()

image_urls = []


def fetch_spacex_last_launch(file_path):
    counter = 0
    data = response.json()
    for i, launch in enumerate(data):
        image_links = launch.get('links', {}).get('flickr', {}).get('original', {})
        image_urls.extend(image_links)

        for url in image_links:
            if counter < 5:
                save_image(url, os.path.join(file_path, f'spacex{counter+1}.jpg'))
                counter += 1
            else:
                print("скачивание завершено")

        if counter >= 5:
            break