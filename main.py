import glob
import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

### Load api key, prompt and files ###
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model_id = os.getenv("GEMINI_MODEL_ID")
if not api_key:
    print("Error: API key not provided via environment variable GEMINI_API_KEY")
    sys.exit(1)

try:
    path = sys.argv[1]
    prompt_path = sys.argv[2]
except IndexError:
    print("Error: Please provide both path and prompt file arguments")
    sys.exit(1)

try:
    with open(prompt_path, "r") as f:
        prompt = f.read().strip()
    print(f"Successfully loaded prompt from: {prompt_path}")
except FileNotFoundError:
    print(f"Error: Prompt file not found: {prompt_path}")
    sys.exit(1)

files = glob.glob(path, recursive=True)
if not files:
    print(f"Error: No files found matching pattern: {path}")
    sys.exit(1)

print(f"Found {len(files)} file(s) to process")
### End load prompt and files ###

### Initialize GenAI ###
client = genai.Client(api_key=api_key)
print("GenAI client initialized")
### End initialize GenAI ###

### Process files ###
for i in range(len(files)):
    print(f"\rProcessing file {i+1}/{len(files)} ({(i)/len(files)*100:.2f}%)", end="")
    file = files[i]
    with open(file, "r+") as f:
        old_code = f.read()
        response = client.models.generate_content(
            model=model_id,
            contents=old_code,
            config=types.GenerateContentConfig(
                max_output_tokens=65536, temperature=0.01, system_instruction=prompt
            ),
        ).text
        new_code = response.split("```")[1].split("\n", 1)[1].rsplit("\n", 1)[0]
        f.seek(0)
        f.write(new_code)
        f.truncate()

print(f"\rFinished processing {len(files)}/{len(files)} files (100%)")
### End process files ###
