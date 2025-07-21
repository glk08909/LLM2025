import mcp_client

our_mcp_client = mcp_client.MCPClient(["python", "weather_server.py"])

our_mcp_client.start_server()
our_mcp_client.initialize()
our_mcp_client.initialized()

tools = our_mcp_client.get_tools()
print("Available tools:", tools)

response = our_mcp_client.call_tool("get_weather", {"city": "Berlin"})
print("Weather in Berlin:", response)
