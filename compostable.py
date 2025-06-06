import base64
import requests
import streamlit as st
import json

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
            "temperature": 0.3,
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                 "You should identify and determine whether an item in the image provided is compostable in a standard compost bin on college campuses. Answer using the EXACT format below, adjusting for grammar purposes and allocating bulletpoints for applicable sections. Refer to the default response if necessary (found below).\n"
                                "Response Format:\n\n"
                                "# A [Object name] is [compostable/not compostable]\n\n"
                                "[Something like [HOOray -- your contributions are making a big impact!] if the item is compostable or [We appreciate that you're checking — every effort counts!] if the item is not compostable]\n\n"
                                "### [\"Why is a [item] compostable? 🌱 \" if applicable]\n\n"
                                "### [\"Why is a [item] not compostable? 🌱 \" if applicable]\n\n"
                                "### [\"Specific Steps for Compost 🧑‍🌾 \" if applicable]\n\n"
                                "Default Response:\n"
                                "Shucks -- we had a bit of trouble with your request. Make sure you are in good lighting and that no external objects or humans are clearly visible in the camera."
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

        response_text = result['choices'][0]['message']['content']
        #st.success(response.text)
    
        st.session_state["compostable"] = "no"
        if response_text.lower().startswith("#") and " is compostable" in response_text.lower():
            st.session_state["compostable"] = "yes"

        if not (response_text.lower().startswith("#") and (" compostable" in response_text.lower())):
            if not (response_text.lower().startswith("Shucks")):
                response_text = "Uh oh! We detected a human in the image. Please try to best capture the item so we can determine its compostability."
        if(st.session_state["compostable"] == "yes"):
            # Define the structured output format using OpenAI's "function calling" method
            data = {
                "model": "gpt-4o",
                "temperature": 0.3,
                "messages": [
                    {
                        "role": "system",
                        "content": "Classify the compostable item into one of the following categories: "
                                "\"Non-Dairy Food\", \"Cardboard Products\", \"Paper Products\", \"Miscellaneous\", or \"Dairy\". "
                                "Respond with only the category name."
                    },
                    {
                        "role": "user",
                        "content": response_text  # The response from the first model call
                    }
                ],
                "tools": [  # Define structured output constraints
                    {
                        "type": "function",
                        "function": {
                            "name": "classify_compostable_item",
                            "description": "Classify the compostable item into one of the predefined categories.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "category": {
                                        "type": "string",
                                        "enum": [
                                            "Non-Dairy Food",
                                            "Cardboard Products",
                                            "Paper Products",
                                            "Miscellaneous",
                                            "Dairy"
                                        ]
                                    }
                                },
                                "required": ["category"]
                            }
                        }
                    }
                ],
                "tool_choice": {"type": "function", "function": {"name": "classify_compostable_item"}}  # Force structured response
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )

            result = response.json()


            if "error" in result:
                st.error(f"API Error: {result['error']['message']}")
            else:
                structured_output = result["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
                category = json.loads(structured_output)["category"]
                st.session_state["compostable_category"] = category  # Store structured output
        
        return response_text
    

    except Exception as e:
        return f"Unexpected error: {e}"
