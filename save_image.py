import os
import requests


def save_image(url, file_path):

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)

        print(f"Saved image to {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
    except Exception as e:
        print(f"Error saving image to file: {e}")