import subprocess
import json

class MCPClient:
    def __init__(self, command):
        self.command = command
        self.process = None

    def start_server(self):
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def _send(self, payload):
        json.dump(payload, self.process.stdin)
        self.process.stdin.write("\n")
        self.process.stdin.flush()
        response = self.process.stdout.readline()
        return json.loads(response)

    def initialize(self):
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        return self._send(init_payload)

    def initialized(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        self._send(payload)

    def get_tools(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        return self._send(payload)["result"]

    def call_tool(self, name, arguments):
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        return self._send(payload)
