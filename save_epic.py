import os
import requests
from urllib.parse import urlparse
from datetime import datetime
from PIL import Image
from save_image import save_image


API_URL = 'https://api.spacexdata.com/v5/launches/'
response = requests.get(API_URL)
response.raise_for_status()


def save_EPIC():
    api_token = os.environ.get('api_token') 
    if not api_token:
        print("NASA API ключ не найден.")
        return

    image_dir = "images/epic"  
    os.makedirs(image_dir, exist_ok=True)  

    count =   5


    url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={api_token}&count={count}"  
    try:
        response = requests.get(url)
        response.raise_for_status()
        epic_data = response.json()

        if not epic_data:
            print("No EPIC data found.")
            return

    except requests.exceptions.RequestException as e:
        print(f"Error fetching EPIC metadata: {e}")
        return
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error parsing EPIC metadata: {e}")
        return
    

  

    counter = 0

    for item in epic_data: 
        if counter >= count:         
            break
          #внимание сюдааа

        latest_date = item['date']
        date_obj = datetime.strptime(latest_date, "%Y-%m-%d %H:%M:%S")
        date_str = date_obj.strftime("%Y/%m/%d")  

        image_name = item['image']
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{date_str}/jpg/{image_name}.jpg?api_key={api_token}&{count}"
        file_path = os.path.join(image_dir, f"epic_{image_name}.jpg")
        save_image(image_url, file_path)  

        counter += 1
