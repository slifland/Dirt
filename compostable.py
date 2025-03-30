import base64

with open("captured.jpg", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

image = f"data:image/jpeg;base64,{base64_image}"

import requests
import streamlit as st
import sys

api_key = st.secrets['GPT_API_KEY']

#image = "captured.jpg"

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
