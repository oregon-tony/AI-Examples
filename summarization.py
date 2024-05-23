# https://learn.microsoft.com/en-us/azure/ai-services/language-service/summarization/quickstart?tabs=text-summarization%2Cmacos&pivots=programming-language-python

# Take a string of sentence(s) and summarize to smaller text block.
# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
# If you have an Azure account, you can create a 'free' resource to run this example, see URL ^^

import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
key = os.environ.get('LANGUAGE_KEY')
endpoint = os.environ.get('LANGUAGE_ENDPOINT')


# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=ta_credential)
    return text_analytics_client


client = authenticate_client()


# Example method for summarizing text
def sample_extractive_summarization(client):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        ExtractiveSummaryAction
    )

    document = [
        "How do I configure a IPSEC VPN in Skytap?"
    ]

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractiveSummaryAction(max_sentence_count=1)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            print("Summary extracted: \n{}".format(
                " ".join([sentence.text for sentence in extract_summary_result.sentences]))
            )

sample_extractive_summarization(client)

