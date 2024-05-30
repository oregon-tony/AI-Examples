# Example of comparing a known set of LLM prompts and their correct static
# responses captured as the "expected" result with the actual live LLM result.
# The expected and actual are "scored" from similarity. 1.0=Perfect match

# SEE FILE in 'AI-Examples' called 'test_prompts.json'

import os
import json
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


oai_client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def read_test_prompts(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return []


def get_openai_response(prompt):
    try:

        messages = [
            {"role": "system", "content": """You provide short answers to questions on any general topic."""},
            {"role": "user", "content": prompt}
        ]

        response = oai_client.chat.completions.create(
            model="gpt-4o",  # Replace with your desired model
            messages=messages,
            temperature=0.4
        )
        # print("******\n")
        # print(response)
        # print("******\n")
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return ""


def calculate_similarity(expected, actual):
    vectorizer = TfidfVectorizer().fit_transform([expected, actual])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0][1]


def run_regression_test(file_path):
    input_data = read_test_prompts(file_path)
    test_prompts = input_data['RegressionPrompts']
    # print(test_prompts)
    results = []

    for test in test_prompts:
        # print(test)
        original_prompt = test['Original_Prompt']
        expected_answer = test['Expected_Answer']

        if original_prompt and expected_answer:
            actual_answer = get_openai_response(original_prompt)
            similarity_score = calculate_similarity(expected_answer, actual_answer)

            results.append({
                "Original_Prompt": original_prompt,
                "Expected_Answer": expected_answer,
                "Actual_Answer": actual_answer,
                "Similarity_Score": similarity_score
            })
        else:
            print("Invalid test case format.")

    return results


def print_results(results):
    for result in results:
        print(f"Original Prompt: {result['Original_Prompt']}")
        print(f"Expected Answer: {result['Expected_Answer']}")
        print(f"Actual Answer: {result['Actual_Answer']}")
        print(f"Similarity Score: {result['Similarity_Score']:.2f}")
        print("="*50)


if __name__ == "__main__":
    test_results = run_regression_test('./test_prompts.json')
    print_results(test_results)

# END


Here is the sample output: (see the last entry with the intentional wrong expected result)

Original Prompt: What is the capital of France?
Expected Answer: The capital of France is Paris.
Actual Answer: The capital of France is Paris.
Similarity Score: 1.00
==================================================
Original Prompt: Who wrote 'To Kill a Mockingbird'?
Expected Answer: Harper Lee wrote 'To Kill a Mockingbird'.
Actual Answer: Harper Lee wrote 'To Kill a Mockingbird'.
Similarity Score: 1.00
==================================================
Original Prompt: Who was President in 1863?
Expected Answer: In 2023, Joe Biden was President.
Actual Answer: In 1863, Abraham Lincoln was the President of the United States.
Similarity Score: 0.21
==================================================
