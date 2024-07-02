# sample code to test the tokens consumed by a specific LLM
# different models produce slightly different results

import tiktoken

# Initialize the encoding for the specific model
encoding = tiktoken.encoding_for_model("gpt-4o")  # try text-davinci-003

prompts = [
    "dog",
    "dogz",
    "my dog has fleas",
    "myz dogz haz fleaz",
    "skytap",
    "sky tap",
    "unbelievable"
]

for prompt in prompts:
    tokens = encoding.encode(prompt)
    each_token = [encoding.decode([token]) for token in tokens]
    token_count = len(tokens)
    word_count = len(prompt.split())
    ratio = token_count / word_count
    print(f"Prompt: {prompt}")
    print(f"Number of tokens: {token_count}")
    print(f"Number of words: {word_count}")
    print(f"Token to word ratio: {ratio:.2f}")
    print(f"Tokens: {each_token}\n")
