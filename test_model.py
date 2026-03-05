"""Quick test script for the deployed model."""

import os
import sys
from openai import OpenAI

# RunPod endpoint — replace with your Pod's IP/URL
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/v1"
API_KEY = os.environ.get("RUNPOD_API_KEY", "not-needed")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Check available models
models = client.models.list()
print("Available models:", [m.id for m in models.data])

# Test chat completion
response = client.chat.completions.create(
    model=models.data[0].id,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Привет! Кратко опиши свои возможности."},
    ],
    max_tokens=512,
    temperature=0.7,
)

print("\nResponse:")
print(response.choices[0].message.content)
