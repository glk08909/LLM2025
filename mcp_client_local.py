import run_mcp_client

# Start the MCP server
our_mcp_client = run_mcp_client.MCPClient(["python", "weather_server.py"])

our_mcp_client.start_server()
our_mcp_client.initialize()
our_mcp_client.initialized()

# List available tools
tools = our_mcp_client.get_tools()
print("Available tools:\n", tools)

# Optional: test a tool
response = our_mcp_client.call_tool('get_weather', {'city': 'Berlin'})
print("Weather response:\n", response)
