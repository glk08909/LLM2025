import random

known_weather_data = {
    'berlin': 20.0,
    'India': 30.0
}

def get_weather(city: str) -> float:
    city = city.strip().lower()

    if city in known_weather_data:
        return known_weather_data[city]

    return round(random.uniform(-5, 35), 1)

# Test the function
if __name__ == "__main__":
    city_name = input("Enter a city name: ")
    temperature = get_weather(city_name)
    print(f"The weather in {city_name} is {temperature}°C")
