import pandas as pd
import requests
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)



def fetch_street_view_image(location, save_path=None):
    """
    Fetches an image from Google Street View API and optionally saves it as a file.
    
    Args:
        location (str): The location (address or lat,lng) for the image.
        api_key (str): Your Google API key.
        save_path (str): Path to save the image file. If None, the image won't be saved.
    
    Returns:
        Image object if successful, otherwise None.
    """
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "location": location,
        "size": "600x600",
        "fov": 70,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(base_url, params=params)
    image_paths = []
    if response.status_code == 200:
        image_path = os.path.join(save_path, f"front_view.jpeg")
        with open(image_path, 'wb') as f:
            f.write(response.content)
        image_paths.append(image_path)

    return image_paths
    

# FUNCTION FOR GETTING LAT LONG FROM ADDDRESS
def getLatLongGoogle(locationAddress):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    response = requests.get(
        url, params={"address": locationAddress, "key": GOOGLE_API_KEY})
    if response.status_code == 200:
        return response.json()


# FUNCTION FOR GETTING GOOGLE SAT IMAGE FROM THE LAT LONG
def getGoogleSatImage(lat, long, save_path=None):
    url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": f"{lat},{long}",
        "zoom": 21,
        "size": "600x600",
        "maptype": "satellite",
        "key": GOOGLE_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        image_paths =[]
        if response.status_code == 200:
            image_path = os.path.join(save_path, f"top_view.jpeg")
            with open(image_path, 'wb') as f:
                f.write(response.content)
        image_paths.append(image_path)
        return image_paths
    except Exception as e:
        print("ERROR : ", e)
        return e
    

def analyze_images_with_openai(image_paths, prompt_template=None):
    # Set the default prompt if none is provided
    if prompt_template is None:
        prompt = """
        Using roof, siding, landscaping, driveway and windows as the key factors. Grade this home from 0-10, 10 being perfect.
        """
    else:
        prompt = prompt_template

    analyses = []
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            # Convert image to Base64
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1500
            )
            analyses.append(response.choices[0].message.content)

    return " | ".join(analyses)
