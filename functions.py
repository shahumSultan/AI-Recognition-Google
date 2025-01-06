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


def full_address(uploaded_file):
    data = pd.read_csv(uploaded_file)
    data['combined_address'] = data.apply(
        lambda row: ', '.join(row.astype(str)), axis=1)
    return data


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
    # if response.status_code == 200:
    #     image = Image.open(BytesIO(response.content))
    #     return image
    #     # image.save(save_path, "JPEG")
    #     # print(f"Image saved: {save_path}")
    # else:
    #     print(
    #         f"Failed to fetch image for '{location}'. Status code: {response.status_code}")


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
