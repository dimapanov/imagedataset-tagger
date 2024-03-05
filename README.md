I made this script for tagging images for stable diffusion training. This script accepts images from a folder input, encodes them into base64, resizes them and sends them for processing to OpenAI's GPT-4 vision API endpoint. The AI model returns a description in comma-separated tags form which is saved in a .txt file in the provided folder path.

## Usage

The script accepts two arguments from command line:
`folder_path` - The path of folder from which images will be processed.
`max tokens` - Maximum number of tokens that the GPT-4 model can return.



## Setup

**Install the dependencies using pip:**

```
pip install pillow requests python-dotenv
```

**Add your OpenAI API key to a .env file in your root directory:**
```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

**Run the script:**
```
python main.py your/imagefolder/path 300
```

Replace your/folder/path with the path of folder where images are stored and set max_tokens with the maximum number of tokens that the GPT-4 model can return (300 is ok).
