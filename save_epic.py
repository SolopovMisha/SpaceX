import os
import requests
from urllib.parse import urlparse
from datetime import datetime
from PIL import Image
from save_image import save_image


def check_api_token():
    api_token = os.environ.get('NASA_API_TOKEN')
    if not api_token:
        print("NASA API ключ не найден.")
        return None
    return api_token


def create_epic_directory():
    image_dir = "images/epic"
    os.makedirs(image_dir, exist_ok=True)
    return image_dir


def fetch_epic_metadata(api_token, count):
    url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={api_token}&count={count}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
        print(f"Error fetching EPIC metadata: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parsing EPIC metadata: {e}")
        return None


def process_epic_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return date_obj.strftime("%Y/%m/%d")


def build_epic_image_url(api_token, date_str, image_name, count):
    return f"https://api.nasa.gov/EPIC/archive/natural/{date_str}/jpg/{image_name}.jpg?api_key={api_token}&{count}"


def process_epic_item(item, api_token, count, image_dir, counter):
    latest_date = item['date']
    date_str = process_epic_date(latest_date)
    image_name = item['image']

    image_url = build_epic_image_url(api_token, date_str, image_name, count)
    file_path = os.path.join(image_dir, f"epic_{image_name}.jpg")
    save_image(image_url, file_path)


def save_EPIC():
    api_token = check_api_token()
    if not api_token:
        return

    image_dir = create_epic_directory()
    count = 5

    epic_data = fetch_epic_metadata(api_token, count)
    if not epic_data:
        return

    counter = 0
    for item in epic_data:
        if counter >= count:
            break

        process_epic_item(item, api_token, count, image_dir, counter)
        counter += 1