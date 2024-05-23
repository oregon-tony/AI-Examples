# https://learn.microsoft.com/en-us/azure/ai-services/language-service/key-phrase-extraction/quickstart?pivots=programming-language-python

# Take a string of sentence(s) and extract the key or core words.
# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
# If you have an Azure account, you can create a 'free' resource to run this example, see URL ^^
 

import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

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


def key_phrase_extraction_example(client):
    try:
        # documents = ["Dr. Smith has a very modern medical office, and she has great staff."]
        documents = ["How do I copy a template to another region?"]

        response = client.extract_key_phrases(documents=documents)[0]

        if not response.is_error:
            print("\tKey Phrases:")
            for phrase in response.key_phrases:
                print("\t\t", phrase)
        else:
            print(response.id, response.error)

    except Exception as err:
        print("Encountered exception. {}".format(err))


key_phrase_extraction_example(client)
