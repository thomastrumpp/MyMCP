import asyncio
import os
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession, Tool, FunctionDeclaration
from mcp.client.sse import sse_client
from mcp import ClientSession
from google.protobuf.struct_pb2 import Struct

# Configuration
PROJECT_ID = "mymcp-antigravity-prod"
LOCATION = "us-central1"
REMOTE_URL = f"https://mcp-server-139388198422.europe-west1.run.app/sse"

def map_mcp_tool_to_gemini(mcp_tool):
    return FunctionDeclaration(
        name=mcp_tool.name,
        description=mcp_tool.description,
        parameters=mcp_tool.inputSchema
    )

async def run_gemini_agent_test():
    print(f"🔹 Initializing Vertex AI for project {PROJECT_ID}...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    # Dynamic Model Selection
    print("🔹 Listing available models...")
    model_name = None
    try:
        from vertexai.preview.generative_models import GenerativeModel
        # This listing part is actually tricky in SDK, usually we just try known ones.
        # But let's try to infer if we can.
        # Actually proper way:
        import google.cloud.aiplatform
        google.cloud.aiplatform.init(project=PROJECT_ID, location=LOCATION)
        models = google.cloud.aiplatform.Model.list() 
        # Wait, Model.list() lists custom models. We want foundational models.
        # We'll just define a fallback list.
    except:
        pass

    candidates = ["gemini-1.5-flash-001", "gemini-1.5-pro-001", "gemini-1.5-flash", "gemini-1.0-pro-001", "gemini-1.0-pro", "gemini-pro"]
    
    # We will try them in order until one works
    model = None
    for candidate in candidates:
        print(f"🔹 Trying model: {candidate}")
        try:
            m = GenerativeModel(candidate)
            # Test instantiation effectively
            # Make a dummy call? No, can't easily without tools.
            # We'll just assume the first one that doesn't throw on init is fine, 
            # though init is lazy. Detailed error happens on generation.
            model_name = candidate
            break
        except Exception as e:
            print(f"   Error: {e}")

    # FORCE override to a likely one if dynamic failed logic (lazy init doesn't catch much)
    # Let's trust the loop order.
    
    # Actually, let's just use "gemini-1.0-pro" as it is most stable for new projects usually.
    # But wait, previous run failed on 1.5-flash.
    # Let's try 1.0-pro-002 if 001 failed?
    model_name = "gemini-1.0-pro" 

    print(f"🔹 Connecting to MCP Server at {REMOTE_URL}...")
    async with sse_client(REMOTE_URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            print("🔹 Discovering tools from MCP server...")
            mcp_tools_list = await session.list_tools()
            gemini_funcs = []
            
            print("\n📋 Available Tools:")
            for t in mcp_tools_list.tools:
                print(f"  - {t.name}: {t.description}")
                gemini_funcs.append(map_mcp_tool_to_gemini(t))
            
            gemini_tool = Tool(function_declarations=gemini_funcs)
            
            # Try to start chat
            try:
                model = GenerativeModel(model_name, tools=[gemini_tool])
                chat = model.start_chat()
            except Exception as e:
                print(f"❌ Failed to init model {model_name}: {e}")
                return

            user_prompt = "Calculate (15 + 10) * 2 using the available tools."
            print(f"\n👤 User Prompt: '{user_prompt}'")
            
            try:
                response = await asyncio.to_thread(chat.send_message, user_prompt)
            except Exception as e:
                 print(f"❌ Error during generation with {model_name}: {e}")
                 # Fallback logic could go here but let's just report execution failure
                 raise e

            while response.candidates[0].content.parts[0].function_call:
                func_call = response.candidates[0].content.parts[0].function_call
                func_name = func_call.name
                func_args = dict(func_call.args)
                
                print(f"\n🤖 Model requests tool execution: {func_name}({func_args})")
                
                result = await session.call_tool(func_name, arguments=func_args)
                tool_output = result.content[0].text
                print(f"✅ MCP Server Result: {tool_output}")
                
                response = await asyncio.to_thread(
                    chat.send_message,
                    vertexai.generative_models.Part.from_function_response(
                        name=func_name,
                        response={"result": tool_output}
                    )
                )

            print(f"\n🧠 Final Agent Answer: {response.text}")

if __name__ == "__main__":
    asyncio.run(run_gemini_agent_test())
