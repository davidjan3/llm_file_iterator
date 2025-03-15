from google import genai
from google.genai import types
from arg_parser import parse_args, parse_api_args
import io

### Loading config ###
prompt, files = parse_args()
api_key, model_id = parse_api_args("GEMINI")
### End loading config ###

### Initialize GenAI ###
client = genai.Client(api_key=api_key)
print("GenAI client initialized")
### End initialize GenAI ###

### Process files ###
for i in range(len(files)):
    print(f"Processing file {i+1}/{len(files)} ({(i)/len(files)*100:.2f}%)", end="\r")
    file = files[i]
    with io.open(file, "r+", encoding="UTF-8") as f:
        old_code = f.read()
        response = client.models.generate_content(
            model=model_id,
            contents=old_code,
            config=types.GenerateContentConfig(
                max_output_tokens=8192, temperature=0.01, system_instruction=prompt
            ),
        ).text
        response_split = response.split("```")
        if len(response_split) < 3:
            print(f"Invalid response for file: {file}")
            continue
        new_code = response_split[1].split("\n", 1)[1].rsplit("\n", 1)[0]
        f.seek(0)
        f.write(new_code)
        f.truncate()

print(f"Finished processing {len(files)}/{len(files)} files (100%)")
### End process files ###
