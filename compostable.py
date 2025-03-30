import base64
import requests
import streamlit as st
import sys

def analyze_image(image_path):
    with open (image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    image_data = f"data:image/jpeg;base64,{base64_image}"

    api_key = st.secrets['GPT_API_KEY']

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
                    {"type": "image_url", "image_url": {"url": image_data}}
                ]
            }
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()
    return result['choices'][0]['message']['content']
