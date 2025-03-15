import time
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from arg_parser import parse_args, parse_api_args
import io
from anthropic import Anthropic

### Loading config ###
prompt, files = parse_args()
api_key, model_id = parse_api_args("ANTHROPIC")
### End loading config ###

### Initialize GenAI ###
client = Anthropic(api_key=api_key)
print("Anthropic client initialized")
### End initialize GenAI ###

### Process files ###
# Create a batch of requests
requests = []
for i in range(len(files)):
    file = files[i]
    with io.open(file, "r+", encoding="UTF-8") as f:
        old_code = f.read()
        requests.append(
            Request(
                custom_id="file_" + str(i),
                params=MessageCreateParamsNonStreaming(
                    model=model_id,
                    max_tokens=8192,
                    system=prompt,
                    temperature=0.01,
                    messages=[{"role": "user", "content": old_code}],
                ),
            )
        )
batch = client.messages.batches.create(requests=requests)
batch_id = batch.id
results_url = batch.results_url
print(f"Batch created with ID: {batch_id}")

# Wait for batch to complete
time.sleep(10)
finished = False
while not finished:
    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status == "ended":
        finished = True
        print(f"Batch processing complete.")
    else:
        print(f"Batch status: {batch.request_counts}")
        time.sleep(60)

# Retrieve and apply results
results = client.messages.batches.results(batch_id)
for result in results:
    file = files[int(result.custom_id.split("_")[1])]
    response = result.result.message.content[0].text
    response_split = response.split("```")
    if len(response_split) < 3:
        print(f"Invalid response for file: {file}")
        continue
    new_code = response_split[1].split("\n", 1)[1].rsplit("\n", 1)[0]
    with io.open(file, "w", encoding="UTF-8") as f:
        f.write(new_code)

print(f"Finished processing {len(files)}/{len(files)} files (100%)")
### End process files ###
