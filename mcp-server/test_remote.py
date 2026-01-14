import asyncio
import sys
import traceback
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.types import CallToolResult

# This matches the Cloud Run URL deployed earlier
REMOTE_URL = "https://mcp-server-139388198422.europe-west1.run.app/sse"

async def run_tests():
    print(f"Connecting to Remote MCP server at {REMOTE_URL}...")
    
    # Connect via SSE
    async with sse_client(REMOTE_URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # List tools
            print("\n--- Listing Tools ---")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"Tool: {tool.name} - {tool.description}")
            
            # Test Add
            print("\n--- Testing Add (10 + 5) ---")
            result_add = await session.call_tool("add", arguments={"a": 10, "b": 5})
            print(f"Result: {result_add.content[0].text}")
            
            # Test Subtract
            print("\n--- Testing Subtract (20 - 7) ---")
            result_sub = await session.call_tool("subtract", arguments={"a": 20, "b": 7})
            print(f"Result: {result_sub.content[0].text}")
            
            # Test Multiply
            print("\n--- Testing Multiply (6 * 8) ---")
            result_mul = await session.call_tool("multiply", arguments={"a": 6, "b": 8})
            print(f"Result: {result_mul.content[0].text}")

            # Test Misuse (Type Error)
            print("\n--- Testing Misuse: Invalid Type (String instead of Float) ---")
            try:
                result_misuse_1 = await session.call_tool("add", arguments={"a": "ten", "b": 5})
                if result_misuse_1.isError:
                    print(f"Result: Caught Expected Error (via isError=True) -> {result_misuse_1.content[0].text}")
                else:
                    print(f"Result: Unexpected success -> {result_misuse_1.content[0].text}")
            except Exception as e:
                 print(f"Result: Caught Exception -> {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_tests())
    except Exception as e:
        print(f"Test failed: {e}")
        traceback.print_exc()
        sys.exit(1)
