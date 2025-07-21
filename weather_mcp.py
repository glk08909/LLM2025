# weather_mcp.py
import sys
import json

known_weather_data = {
    'berlin': 20.0
}

def get_weather(city: str) -> float:
    city = city.strip().lower()
    return known_weather_data.get(city, 25.0)

def main():
    for line in sys.stdin:
        request = json.loads(line)
        response = {
            "jsonrpc": "2.0",
            "id": request.get("id"),
        }

        if request["method"] == "initialize":
            response["result"] = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "experimental": {},
                    "prompts": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False},
                    "tools": {"listChanged": True}
                },
                "serverInfo": {"name": "Demo 🚀", "version": "1.9.4"}
            }
        elif request["method"] == "notifications/initialized":
            continue
        elif request["method"] == "tools/call":
            params = request["params"]
            if params["name"] == "get_weather":
                city = params["arguments"]["city"]
                temp = get_weather(city)
                response["result"] = {
                    "content": f"The weather in {city.capitalize()} is {temp}°C"
                }

        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
