import os
import requests


def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_image(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None


def save_to_file(response, file_path):
    try:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print(f"Saved image to {file_path}")
    except Exception as e:
        print(f"Error saving image to file: {e}")


def save_image(url, file_path):
    ensure_directory_exists(file_path)

    response = download_image(url)
    if response:
        save_to_file(response, file_path)
