#!/usr/bin/env python3
"""Test OpenAI API connection and Whisper availability."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from openai import OpenAI

print("=" * 60)
print("OpenAI Connection Test")
print("=" * 60)

# Check if API key exists
print("\n1. Checking API Key...")
if settings.openai_api_key:
    print(f"   [OK] OPENAI_API_KEY is set")
    print(f"   Key length: {len(settings.openai_api_key)} characters")
    print(f"   Key prefix: {settings.openai_api_key[:20]}...")
else:
    print("   [ERROR] OPENAI_API_KEY is NOT set")
    sys.exit(1)

# Try to create client
print("\n2. Creating OpenAI client...")
try:
    client = OpenAI(api_key=settings.openai_api_key)
    print("   [OK] OpenAI client created successfully")
except Exception as e:
    print(f"   [ERROR] Failed to create client: {e}")
    sys.exit(1)

# Test API connection with a simple call
print("\n3. Testing API connection...")
try:
    # Make a minimal API call to test connectivity
    print("   Attempting to list available models...")
    response = client.models.list()
    print("   [OK] API connection successful!")
    print(f"   Available models: {len(response.data)} models")

    # Check if whisper-1 is available
    model_names = [m.id for m in response.data]
    if "whisper-1" in model_names:
        print("   [OK] whisper-1 model is available!")
    else:
        print("   [WARNING] whisper-1 model not found in available models")
        print(f"   Available models: {model_names[:10]}...")

except Exception as e:
    print(f"   [ERROR] API connection failed: {e}")
    print(f"   Error type: {type(e).__name__}")
    print(f"   Error details: {str(e)}")
    sys.exit(1)

print("\n" + "=" * 60)
print("[OK] All tests passed! OpenAI API is properly configured.")
print("=" * 60)
