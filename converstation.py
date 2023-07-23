import openai
import json
import requests
from bs4 import BeautifulSoup


# A dummy function that always returns the same weather information
def get_drug_info(question):
    print("IT RAN>>>>>>>>>>")
    url = "https://www.drugs.com/search.php"
    params = {
        "searchterm": f"{question}",
        "a": "1"
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")
    first_result = soup.find("div", class_="ddc-media-list ddc-search-results").find("a")
    if first_result:
        href = first_result.get("href")
        if href:
            response = requests.get(href)
            soup = BeautifulSoup(response.content, "html.parser")
            result = soup.find("div", class_="contentBox")
            if result:
                print("RESULT>>>>>>>>>>>>>", result.text)
                return result.text


messages = []


def run_conversation_backup(api_key, input_message):
    global messages
    print("LENGTH OF MESSAGES", len(messages))
    if len(messages) > 9:
        messages = messages[3:]
    print("LENGTH OF MESSAGES>>>>2", len(messages))
    openai.api_key = api_key
    messages.append({"role": "user", "content": f"{input_message}"})

    functions = [
        {
            "name": "get_drug_info",
            "description": "Get the details about a drug/medication",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question you want to ask about the drug/medication",
                    },
                },
                "required": ["question"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    print("check response", response_message)

    if response_message.get("function_call"):
        available_functions = {"get_drug_info": get_drug_info}
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            question=function_args.get("question")
        )

        messages.append(response_message)
        # messages.append(
        #     {"role": "function", "name": function_name, "content": function_response}
        # )
        print("SECOND RESPONSE>>>>>>>>>>>>>>", messages)
        second_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
        )
        messages.append(second_response['choices'][0]['message'].to_dict())
        # print("SECOND RESPONSE>>>>>>>>>>>>>>", second_response)
        print("MESSAGE 3", messages)
        return second_response, True

    else:
        resp = response_message["content"]
        messages.append({"role": "assistant", "content": resp})
        print("MESSAGE 2", messages)
        return resp, False

# print(run_conversation())
