import requests

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GPT_API_KEY")


image = "https://storage.googleapis.com/images-lnb-prd-8936dd0.lnb.prd.v8.commerce.mi9cloud.com/product-images/zoom/00244011000004.png"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "system",
            "content": [
                {"type": "text", "text": "You should determine whether an item in the image provided is compostable. Answer in the following format:\n\n1. [Object name]\n2. [Object name] is [compostable/not compostable]\n3. [Reasons for why object is compostable, if applicable]\n4. [Reasons for why object is not compostable, if applicable]\n5. [Specific steps for compost, if applicable]"}
            ]
        },
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image}}
            ]
        }
    ]
}

response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=data
)

print(response.json())
