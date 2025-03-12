Use like this:

```bash
python main.py "C:/path/**/*.ts" "./prompt.txt"
```

This script iterates through files in the specified directory (and subdirectories) using the provided glob pattern. It applies Large Language Model (LLM) transformations to each file based on the instructions in your prompt file.

Make sure to provide a Gemini API Key and Model ID via env and the following parameters via command line:

- First argument: File glob pattern
- Second argument: Path to the prompt file containing instructions for the LLM

Hint: For modifying code it is recommended to explicitely tell the LLM to answer only with code in the prompt.
