import random
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

known_weather_data = {
    'berlin': 20.0,
    'Hyderabad' : 45
}

def get_weather(city: str) -> float:
    city = city.strip().lower()
    if city in known_weather_data:
        return known_weather_data[city]
    return round(random.uniform(-5, 35), 1)

# get_weather_tool = {
#     "name": "get_weather",
#     "description": "Get the current temperature for a given city.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "city": {
#                 "type": "string",
#                 "description": "Name of the city to get the weather for."
#             }
#         },
#         "required": ["city"]
#     }
# }

get_weather_tool = {
    "type": "function",
    "name": "get_weather",  # TODO1: The function's name
    "description": "Get the current temperature for a given city.",  # TODO2: What the function does
    "parameters": {
        "type": "object",
        "properties": {
            "city": {  # TODO3: The function parameter's name
                "type": "string",
                "description": "Name of the city to get the weather for."  # TODO4: Parameter description
            }
        },
        "required": ["city"],  # TODO5: List of required parameters
        "additionalProperties": False
    }
}


def main():
    user_question = input("Ask about the weather: ")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_question}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=[get_weather_tool],
        function_call="auto",
    )

    message = response.choices[0].message

    if message.function_call is not None:
        # function_name = message["function_call"]["name"]
        # arguments = message["function_call"].get("arguments")
        function_name = message.function_call.name
        arguments = message.function_call.arguments

        args = json.loads(arguments)
        city = args.get("city")

        weather = get_weather(city)

        print(f"The weather in {city} is {weather}°C")
    else:
        print(message["content"])

if __name__ == "__main__":
    main()
