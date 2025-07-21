# test_client.py
import subprocess
import json

# Start MCP server (weather_mcp.py) as subprocess
proc = subprocess.Popen(
    ["python3", "weather_mcp.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

def send_and_receive(data):
    proc.stdin.write(json.dumps(data) + "\n")
    proc.stdin.flush()
    response = proc.stdout.readline()
    return json.loads(response)

# Step 1: Initialize
init = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
        "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
}
print("Initialize Response:", send_and_receive(init))

# Step 2: notifications/initialized (no response expected)
notification = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}
proc.stdin.write(json.dumps(notification) + "\n")
proc.stdin.flush()

# Step 3: Call get_weather
weather_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "get_weather",
        "arguments": {"city": "Berlin"}
    }
}
print("Weather Response:", send_and_receive(weather_request))
