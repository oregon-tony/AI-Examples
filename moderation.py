# Python Script to use Moderation Classifications 
import json
import os
from pprint import pprint

from openai import OpenAI
# Utility Functions
oai_client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

response = oai_client.moderations.create(input="I'm going to hit myself on the head.")

if response.results[0].flagged:
    print("Threats Detected")
    print(response)

    for result in response.results:
        categories = result.categories
        pprint(categories.__dict__)

else:
    print("No Threats Detected")


