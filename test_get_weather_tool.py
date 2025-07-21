import openai
import os
import json
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

# Your fake weather function
known_weather_data = {'berlin': 20.0}

def get_weather(city: str) -> float:
    city = city.strip().lower()
    if city in known_weather_data:
        return known_weather_data[city]
    return round(random.uniform(-5, 35), 1)

def set_weather(city: str, temp: float) -> str:
    city = city.strip().lower()
    known_weather_data[city] = temp
    return 'OK'


# Function description
get_weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the current temperature for a given city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city to get the weather for."
            }
        },
        "required": ["city"],
        "additionalProperties": False
    }
}

set_weather_tool = {
    "type": "function",
    "name": "set_weather",
    "description": "Set or update the temperature for a given city in the weather database.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city to set the weather for."
            },
            "temp": {
                "type": "number",
                "description": "Temperature value to be stored for the city."
            }
        },
        "required": ["city", "temp"],
        "additionalProperties": False
    }
}


def main():
    #user_question = "What's the weather like in Germany?"
    user_question = "What's the weather like in Toronto?"

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_question}
    ]

    # Step 1: Ask the model with function description
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,        
        functions=[get_weather_tool, set_weather_tool],
        function_call="auto"
    )

    message = response.choices[0].message

    # Step 2: Check if model decided to call a function
    if message.function_call is not None:
       
        function_name = message.function_call.name
        arguments = json.loads(message.function_call.arguments)
        city = arguments.get("city")

        # Step 3: Execute the function
        weather = get_weather(city)

        # Step 4: Print final response
        print(f"The weather in {city} is {weather}°C")
    else:
        print(message.content)
        
    if message.function_call:
        function_name = message.function_call.name
    arguments = json.loads(message.function_call.arguments)

    if function_name == "get_weather":
        city = arguments.get("city")
        weather = get_weather(city)
        print(f"The weather in {city} is {weather}°C")

    elif function_name == "set_weather":
        city = arguments.get("city")
        temp = arguments.get("temp")
        result = set_weather(city, temp)
        print(f"Weather updated: {result}")


if __name__ == "__main__":
    main()
