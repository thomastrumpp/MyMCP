import os

import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "mymcp-antigravity-prod"
LOCATION = "us-central1"

print(f"Auth file: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Try to list models via API if possible, or just instantiate common ones to check availability
candidates = [
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro-001",
    "gemini-1.5-pro-002",
    "gemini-1.0-pro",
    "gemini-1.0-pro-001",
    "gemini-1.0-pro-002",
    "gemini-pro",
    "text-bison",
    "text-bison@001"
]

print("Checking model availability...")
for model_name in candidates:
    try:
        model = GenerativeModel(model_name)
        # Try a dummy generation (hello world)
        response = model.generate_content("Hello")
        print(f"✅ {model_name} is AVAILABLE (Response: {response.text})")
    except Exception as e:
        print(f"❌ {model_name} failed: {e}")
