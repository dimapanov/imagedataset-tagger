import base64
import os
import requests
from PIL import Image
from dotenv import load_dotenv
import sys

# Load .env file
load_dotenv()

# OpenAI API Key from .env file
api_key = os.getenv("OPENAI_API_KEY")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Getting Folder path and max tokens as arguments from command line
folder_path = sys.argv[1]
max_tokens = sys.argv[2]
API_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


def process_image(file_path):
    base = os.path.basename(file_path)
    file_name, _ = os.path.splitext(base)

    img = Image.open(file_path)
    img = img.convert('RGB')
    img = img.resize((512, 512), Image.LANCZOS)
    img.save('tmp_image.jpg')

    base64_image = encode_image('tmp_image.jpg')

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Described image though tags. Answer only comma separated words"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": max_tokens
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"HTTP error: status code {response.status_code}")
        print(f"Response content: {response.content}")
        return

    try:
        response_data = response.json()
    except ValueError:
        print(f"Error decoding JSON from response")
        return

    choices = response_data.get('choices', [])
    content = ''
    if choices:
        content = choices[0].get('message', {}).get('content', '')

    os.remove('tmp_image.jpg')

    with open(f"{folder_path}/{file_name}.txt", 'w') as output_file:
        output_file.write(str(content))


for index, file in enumerate(os.listdir(folder_path), start=1):
    if file.lower().endswith(('png', 'jpg', 'jpeg')):
        process_image(os.path.join(folder_path, file))
        print(f"Processed: {file} ({index}/{len(os.listdir(folder_path))})")
