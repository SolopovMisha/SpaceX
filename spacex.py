import requests
import os
from save_image import save_image


API_URL = 'https://api.spacexdata.com/v5/launches/'
response = requests.get(API_URL)
response.raise_for_status()

image_urls = []


def get_launch_data():
    return response.json()


def extract_image_links(launch_data):
    links = []
    for launch in launch_data:
        image_links = launch.get('links', {}).get('flickr', {}).get('original', [])
        links.extend(image_links)
    return links


def save_spacex_images(image_links, file_path, max_count=5):
    counter = 0
    for url in image_links:
        if counter >= max_count:
            print("Скачивание завершено")
            break

        save_image(url, os.path.join(file_path, f'spacex{counter+1}.jpg'))
        counter += 1


def fetch_spacex_last_launch(file_path):
    launch_data = get_launch_data()
    image_links = extract_image_links(launch_data)
    save_spacex_images(image_links, file_path)
