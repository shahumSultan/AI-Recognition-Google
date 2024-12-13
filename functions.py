import pandas as pd
import requests
import os
import base64
from PIL import Image
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def full_address(uploaded_file):
    data = pd.read_csv(uploaded_file)
    data['combined_address'] = data.apply(lambda row: ', '.join(row.astype(str)), axis=1)
    return data


def fetch_street_view_image(location, api_key, save_path=None):
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
        "size": "400x400",
        "key": api_key
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


def analyze_images_with_openai(image_paths):
    """
    Analyze images using OpenAI's GPT-4V model with the Driving for Dollars scoring system
    """
    prompt = """
    Analyze this property image using the Driving for Dollars scoring system (100 points total).
    Provide detailed analysis and scoring for each category:

    1. Siding Condition (0-25 points)
    - Assess: damage, cracks, peeling paint, discoloration, missing panels
    - Provide specific observations and point deductions
    
    2. Landscape and Driveway Condition (0-25 points)
    - Assess: lawn condition, plant health, driveway state, overall cleanliness
    - Provide specific observations and point deductions
    
    3. Windows Condition (0-25 points)
    - Assess: damage, cleanliness, frame condition, window type
    - Provide specific observations and point deductions
    
    4. Roof Condition (0-25 points)
    - Assess: missing shingles, damage, moss/algae, age indicators
    - Provide specific observations and point deductions

    For each category:
    - Start at 25 points
    - Detail specific issues found
    - Show point deductions
    - Give final category score
    
    End with:
    - Total score out of 100
    - Brief overall assessment
    - Comparison to neighborhood standards (if visible)
    """

    analyses = []
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            # Convert image to Base64
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            # Ensure correct MIME type
            mime_type = "png" if image_path.endswith(".png") else "jpeg"
            response = client.chat.completions.create(
                model="gpt-4o-mini",
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
