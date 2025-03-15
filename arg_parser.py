import glob
import sys
import os
from dotenv import load_dotenv


def parse_args():
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
    return prompt, files


def parse_api_args(prefix):
    load_dotenv()
    api_key = os.getenv(f"{prefix}_API_KEY")
    model_id = os.getenv(f"{prefix}_MODEL_ID")
    if not api_key:
        print(f"Error: API key not provided via environment variable {prefix}_API_KEY")
        sys.exit(1)
    if not model_id:
        print(
            f"Error: Model ID not provided via environment variable {prefix}_MODEL_ID"
        )
        sys.exit(1)
    return api_key, model_id
