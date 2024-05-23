# https://learn.microsoft.com/en-us/azure/ai-services/language-service/named-entity-recognition/quickstart?tabs=macos%2Cga-api&pivots=programming-language-python

# Take a string of sentence(s) and extract the key or core words with a confidence score.
# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
# If you have an Azure account, you can create a 'free' resource to run this example, see URL ^^

import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
language_key = os.environ.get('LANGUAGE_KEY')
language_endpoint = os.environ.get('LANGUAGE_ENDPOINT')


# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client


client = authenticate_client()


# Example function for recognizing entities from text
def entity_recognition_example(client):

    try:
        documents = ["Which employees have salaries larger than $1.00?"]
        result = client.recognize_entities(documents=documents)[0]

        print("Named Entities:\n")
        for entity in result.entities:
            print("\tText: \t", entity.text, "\tCategory: \t", entity.category, "\tSubCategory: \t", entity.subcategory,
                    "\n\tConfidence Score: \t", round(entity.confidence_score, 2), "\tLength: \t", entity.length, "\tOffset: \t", entity.offset, "\n")

    except Exception as err:
        print("Encountered exception. {}".format(err))
        
        
entity_recognition_example(client)

