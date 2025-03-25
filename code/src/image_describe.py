import requests
import json
import os
from dotenv import load_dotenv
import base64


def image_transcribe(base64: str) -> str:
    load_dotenv()

    OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
    OPEN_ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = "google/gemini-2.0-pro-exp-02-05:free"

    headers = {
        "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe in human language what's in the image under 70 words",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64}",
                        },
                    },
                ],
            },
        ],
    }
    response = requests.post(OPEN_ROUTER_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        description = (
            response.json()
            .get("choices", [{}])[0]
            .get("message", {})
            .get("content", "No description available.")
        )
        return description
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return ""


if __name__ == "__main__":
    with open("./data/pexels-flodahm-699459.jpg", "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    print(image_transcribe(base64_image))
