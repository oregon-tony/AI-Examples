from llama_index.llms.openai import OpenAI

llm = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0.0,
    max_tokens=100,
)

for i in range(10):
    response = llm.complete(
        "Fill in the last word to the phrase: 'The road is ... '"
    )
    print(response)
  
