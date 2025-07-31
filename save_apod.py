import os
import requests
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
from save_image import save_image

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

APOD_IMAGE_COUNT = 30


def fetch_apod_data(api_endpoint, request_params):
    try:
        response = requests.get(api_endpoint, params=request_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"Request failed: {req_err}")
        raise
    except ValueError as json_err:
        print(f"Failed to parse JSON: {json_err}")
        raise


def get_image_extension(image_url):
    try:
        parsed_url = urlparse(image_url)
        return os.path.splitext(parsed_url.path)[1]
    except (AttributeError, TypeError) as url_err:
        print(f"Invalid URL format: {url_err}")
        raise


def save_apod_image(apod_item, apod_index, output_dir):
    try:
        image_url = apod_item['url']
        image_extension = get_image_extension(image_url)
        image_filename = f"nasa_apod_{apod_index + 1}{image_extension}"
        image_path = os.path.join(output_dir, image_filename)
        save_image(image_url, image_path)
    except KeyError as key_err:
        print(f"Missing 'url' in APOD item: {key_err}")
        raise
    except (OSError, IOError) as file_err:
        print(f"File operation failed: {file_err}")
        raise


def download_apod_images(nasa_api_token):
    try:
        apod_api_url = "https://api.nasa.gov/planetary/apod"
        request_parameters = {
            'api_key': nasa_api_token,
            'count': APOD_IMAGE_COUNT
        }
        images_directory = "images"
        os.makedirs(images_directory, exist_ok=True)
        
        apod_items = fetch_apod_data(apod_api_url, request_parameters)

        if apod_items:
            for apod_index, apod_item in enumerate(apod_items):
                try:
                    save_apod_image(apod_item, apod_index, images_directory)
                except (KeyError, AttributeError, TypeError, OSError, IOError) as e:
                    print(f"Failed to process APOD item {apod_index}: {e}")
                    continue
    except requests.exceptions.RequestException as e:
        print(f"Network error while downloading APOD images: {e}")
        raise
    except (ValueError, RuntimeError) as e:
        print(f"Processing error: {e}")
        raise

def main():
    try:
        nasa_api_token = os.getenv('NASA_API_TOKEN')
        if not nasa_api_token:
            raise ValueError("NASA_API_TOKEN not found in .env file")
        
        download_apod_images(nasa_api_token)
    except ValueError as val_err:
        print(f"Configuration error: {val_err}")
        sys.exit(1)
    except requests.exceptions.RequestException as req_err:
        print(f"Network error: {req_err}")
        sys.exit(1)
    except Exception as unexpected_err:
        print(f"Unexpected error: {unexpected_err}")
        sys.exit(1)


if __name__ == "__main__":
    import sys
    main()