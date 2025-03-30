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
                                 "You should determine whether an item in the image provided is compostable in a standard compost bin on college campuses. Answer in the format below, adjusting for grammar purposes. If you get any unexpected image inputs, output the default response (found below)\n"
                                "Response Format:\n\n"
                                "# [Object name] is [compostable/not compostable]\n\n"
                                "[Something like [HOOray -- your contributions are making a big impact!] if the item is compostable or [We appreciate that you're checking — every effort counts!] if the item is not compostable]\n\n"
                                "### [\"Why is [item] compostable? 🌱 \" if applicable]\n\n"
                                "### [\"Why is [item] not compostable? 🌱 \" if applicable]\n\n"
                                "### [\"Specific Steps for Compost 🧑‍🌾 \" if applicable]"
                                "Default Response (in italics):\n"
                                "Shucks -- we had a bit of trouble with your request. Make sure you are in good lighting and that no external objects are visible in the camera."
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
