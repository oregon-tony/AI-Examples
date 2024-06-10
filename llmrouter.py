# simple implementation of a prompt-router, based on prompt try to determine which tools function should be called.

import json
import os
from openai import OpenAI

DEBUG = True  # global debug flag

oai_client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


###################################
# utility functions
###################################


def log_debug_messages(debug_label, debug_string):
    print(f"{debug_label} : {debug_string}")

###################################
# Define your REST API functions
# One function for each API action
###################################


def answer_benefits_questions(benefits_prompt):
    if DEBUG:
        log_debug_messages("In Benefits", benefits_prompt)

    return {"BENEFITS Question completed": benefits_prompt}


def answer_organizational_questions(org_prompt):
    if DEBUG:
        log_debug_messages("In ORG:", org_prompt)

    return {"Organizational Question completed": org_prompt}


def answer_support_questions(support_prompt):
    if DEBUG:
        log_debug_messages("In Support", support_prompt)

    return {"Support Question completed": support_prompt}

# Define functions to handle user prompts.
# One function per each required action.


# This is the main openai call handler for the primary prompt the user enters.
def handle_primary_prompt(prompt):

    try:
        if DEBUG:
            log_debug_messages("PROMPT: ", prompt)

        messages = [
            {"role": "system", "content": "You answer questions. In some cases a special function call may be required."},
            {"role": "user", "content": prompt}
        ]

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "answer_benefits_questions",
                    "description": "Answer questions about employee benefits including HR, 401K, vacation, and retirement.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The original prompt that was received.",
                            },
                        },
                        "required": ["prompt"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "answer_organizational_questions",
                    "description": ("""Answer questions about people or job roles.
                                    Job roles might be like CEO, CFO, CIO, VP, Manager, Leader, Engineer.
                                    Question related to "Who is", or "What person".
                                    Contact information requests like email, phone number, etc."""),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The original prompt that was received.",
                            },
                        },
                        "required": ["prompt"],
                    },

                },
            },
            {
                "type": "function",
                "function": {
                    "name": "answer_support_questions",
                    "description": ("""Answer support questions about laptops.
                                    Answer support questions about software.
                                    Answer questions about expired passwords.
                                    Answer questions related to system access."""),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The original prompt that was received.",
                            },
                        },
                        "required": ["prompt"],
                    },

                },
            }
        ]
        # ########################################################

        # Use the OpenAI Completion API with the "functions" capability

        # noinspection PyTypeChecker
        response = oai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            tools=tools,
            tool_choice="auto",
        )

        if DEBUG:
            log_debug_messages("OpenAI CALL", response)

        # Need to parse if response from OpenAI contains a function call or not.
        # If not then don't dynamically try to call the function, it is just a regular LLM prompt.
        # print("FINAL RESPONSE")
        # print(response)

        response_message = response.choices[0].message
        # print(f"MESSAGE CONTENT: {response_message.content}")

        # Setup Tools
        tool_calls = response_message.tool_calls
        # print(f"TOOL CALL: {tool_calls}")

        # If a function, the parse the function name, arguments, and indirectly call the actual function()
        # if response.choices[0].finish_reason == 'function_call':

        function_response = ""  # initialize for the if-statement check later

        if tool_calls:
            # print(f"IN TOOLS_CALL IF STATEMENT")
            # function_name = response.choices[0].message.function_call.name
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                # print(f"FUNCTION NAME: {function_name}")
                arguments = json.loads(tool_call.function.arguments)
                # print("ARGUMENTS")
                # print(arguments)
                function_response = execute_function_call(function_name, arguments)

            # print(function_response) # not needed since we are logging inside the function
        else:
            # print("STANDARD LLM RESPONSE-NO API CALL")
            # print("=================================")
            print(response.choices[0].message.content)  # if just a regular LLM answer, then display it

    except Exception as e:
        print(f"Error: {e}")


# Create a dictionary in get the "actual" function to call from the one returned from the openai call
# In this case they are the same, maybe you might want to map to a specific variation base on prompt
available_functions = {
    'answer_organizational_questions': answer_organizational_questions,
    'answer_benefits_questions': answer_benefits_questions,
    'answer_support_questions': answer_support_questions,
}

# Look up the soft function name defined in the functions structure and get the actual function to call
# Make the call to the indirect function name saved in the variable


def execute_function_call(function_name, arguments):
    # check mapping from meta function name to actual function name
    api_function = available_functions.get(function_name, None)
    # print("FUNCTION")
    # print(api_function)
    if api_function:
        # call the indirect function with or without arguments
        if arguments:
            results = api_function(arguments)
        else:
            results = api_function()
    else:
        results = f"Error: function {function_name} does not exist"
    return results


# Get the keyboard input for a prompt
while True:
    print("")
    print("ENTER PROMPT:")
    interactive_prompt = input()
    if interactive_prompt:
        handle_primary_prompt(interactive_prompt)


# ###############################################################################

ENTER PROMPT:
Who was President in 1863?
PROMPT:  : Who was President in 1863?
OAI CALL : ChatCompletion(id='chatcmpl-9WGaig3XMO9vmipCnbM8o2s24hhVz', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='The President of the United States in 1863 was Abraham Lincoln. He served as the 16th President from March 4, 1861, until his assassination on April 15, 1865.', role='assistant', function_call=None, tool_calls=None))], created=1717477300, model='gpt-4o-2024-05-13', object='chat.completion', system_fingerprint='fp_319be4768e', usage=CompletionUsage(completion_tokens=44, prompt_tokens=212, total_tokens=256))
The President of the United States in 1863 was Abraham Lincoln. He served as the 16th President from March 4, 1861, until his assassination on April 15, 1865.

ENTER PROMPT:
How do I change my 401K withholding percentage?
PROMPT:  : How do I change my 401K withholding percentage?
OAI CALL : ChatCompletion(id='chatcmpl-9WGayzHlFz9bPG5yLVq3HO8T7LiI3', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_Oa2D8ICFMxXa8pX1ZKAa1FX2', function=Function(arguments='{"prompt":"How do I change my 401K withholding percentage?"}', name='answer_benefits_questions'), type='function')]))], created=1717477316, model='gpt-4o-2024-05-13', object='chat.completion', system_fingerprint='fp_319be4768e', usage=CompletionUsage(completion_tokens=27, prompt_tokens=215, total_tokens=242))
In Benefits : {'prompt': 'How do I change my 401K withholding percentage?'}

ENTER PROMPT:
Who is VP of Engineering?
PROMPT:  : Who is VP of Engineering?
OAI CALL : ChatCompletion(id='chatcmpl-9WGbIwK4UJcA6u3FL6HbWdl3pNlN9', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_L2yMSZ5CpJzLayC7nCpZgLWp', function=Function(arguments='{"prompt":"Who is VP of Engineering?"}', name='answer_organizational_questions'), type='function')]))], created=1717477336, model='gpt-4o-2024-05-13', object='chat.completion', system_fingerprint='fp_319be4768e', usage=CompletionUsage(completion_tokens=22, prompt_tokens=210, total_tokens=232))
In ORG: : {'prompt': 'Who is VP of Engineering?'}

ENTER PROMPT:
How do I reset my password?
PROMPT:  : How do I reset my password?
OAI CALL : ChatCompletion(id='chatcmpl-9WGbpih0wtvC9YA4OMhTQ76hmANTi', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_iiNSvnluIYM2Ah8fa7pcftZz', function=Function(arguments='{"prompt":"How do I reset my password?"}', name='answer_support_questions'), type='function')]))], created=1717477369, model='gpt-4o-2024-05-13', object='chat.completion', system_fingerprint='fp_319be4768e', usage=CompletionUsage(completion_tokens=21, prompt_tokens=211, total_tokens=232))
In Support : {'prompt': 'How do I reset my password?'}
