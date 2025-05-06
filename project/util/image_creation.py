import requests
import base64
import os
from pathlib import Path

# Replace this with your Stability AI API key
API_KEY = "sk-fOumcaWXc225YNebBWuttBq9LQ82dwb8W95lLUH94lonKciW"

# API endpoint for text-to-image
url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"

# Headers with authorization
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generateImage(prompt):
    payload = {
        "text_prompts": [{"text": "A DND image-style "+prompt}],
        "cfg_scale": 8,
        "height": 512,
        "width": 512,
        "samples": 1,
        "steps": 30
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        image_base64 = response.json()["artifacts"][0]["base64"]
        image_bytes = base64.b64decode(image_base64)

        # Get user's Downloads folder
        downloads_path = Path.home() / "Downloads"
        output_file = downloads_path / "output_image.png"

        with open(output_file, "wb") as f:
            f.write(image_bytes)

        print(f"Image saved to {output_file}")
    else:
        print("Failed to generate image:", response.text)

#generateImage("an image of a dungeons and dragons style legendary sword with a black background")
