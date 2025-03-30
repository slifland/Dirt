import base64
import requests
import streamlit as st

def analyze_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        image_data = f"data:image/jpeg;base64,{base64_image}"

        api_key = st.secrets["GPT_API_KEY"]

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
                        {
                            "type": "text",
                            "text": (
                                "You should determine whether an item in the image provided is compostable. "
                                "Answer in the following format:\n\n"
                                "1. [Object name]\n"
                                "2. [Object name] is [compostable/not compostable]\n"
                                "3. [Reasons for why object is compostable, if applicable]\n"
                                "4. [Reasons for why object is not compostable, if applicable]\n"
                                "5. [Specific steps for compost, if applicable]"
                            )
                        }
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

        # Check for errors in the response
        if "error" in result:
            return f"API Error: {result['error']['message']}"

        return result['choices'][0]['message']['content']

    except Exception as e:
        return f"Unexpected error: {e}"
