#!/usr/bin/env python3
"""
Ollama diagnostic script.
Run this to check if Ollama is running and properly configured.

Usage:
    python scripts/check_ollama.py
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ollama import AsyncClient
from config import settings


async def check_connection() -> bool:
    """Test basic connectivity to Ollama."""
    print("\n" + "="*70)
    print("🔍 Ollama Connectivity Check")
    print("="*70)
    print(f"Host: {settings.ollama_host}")
    print(f"Model: {settings.ollama_model}")
    print(f"Timeout: {settings.ollama_timeout}s")
    
    try:
        client = AsyncClient(host=settings.ollama_host)
        
        print("\n⏳ Testing connection...")
        response = await asyncio.wait_for(
            client.chat(
                model=settings.ollama_model,
                messages=[{"role": "user", "content": "Say 'Hello' and nothing else."}],
                options={"temperature": 0.1}
            ),
            timeout=30
        )
        
        if hasattr(response, 'message'):
            content = response.message.content if hasattr(response.message, 'content') else str(response.message)
        else:
            content = response.get("message", {}).get("content", "")
        
        print(f"✅ SUCCESS! Response: {content[:100]}")
        return True
        
    except asyncio.TimeoutError:
        print("\n❌ TIMEOUT! Ollama did not respond within 30 seconds.")
        print("\n🔧 Troubleshooting:")
        print("  1. Is Ollama running? Try: ollama serve")
        print(f"  2. Is the model downloaded? Try: ollama pull {settings.ollama_model}")
        return False
        
    except ConnectionError as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("\n🔧 Troubleshooting:")
        print("  1. Is Ollama running? Try: ollama serve")
        print(f"  2. Is it accessible at {settings.ollama_host}?")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        print("\n🔧 Troubleshooting:")
        print(f"  1. Try: ollama pull {settings.ollama_model}")
        print("  2. Check Ollama logs: ollama ps")
        return False


async def check_model() -> bool:
    """Check if the configured model is available."""
    print("\n" + "="*70)
    print("🤖 Model Availability Check")
    print("="*70)
    
    try:
        client = AsyncClient(host=settings.ollama_host)
        print(f"⏳ Checking model '{settings.ollama_model}'...")
        
        await asyncio.wait_for(
            client.chat(
                model=settings.ollama_model,
                messages=[{"role": "user", "content": "Test"}],
                options={"num_predict": 1}
            ),
            timeout=30
        )
        
        print(f"✅ Model '{settings.ollama_model}' is available!")
        return True
        
    except Exception as e:
        print(f"❌ Model '{settings.ollama_model}' not available: {e}")
        print(f"\n🔧 Try: ollama pull {settings.ollama_model}")
        return False


async def check_json_format() -> bool:
    """Check if Ollama can handle JSON format requests."""
    print("\n" + "="*70)
    print("📋 JSON Format Support Check")
    print("="*70)
    
    try:
        client = AsyncClient(host=settings.ollama_host)
        print("⏳ Testing JSON format generation...")
        
        schema = {
            "type": "object",
            "properties": {"test": {"type": "string"}},
            "required": ["test"]
        }
        
        response = await asyncio.wait_for(
            client.chat(
                model=settings.ollama_model,
                messages=[{"role": "user", "content": "Return JSON with test='success'"}],
                format=schema,
                options={"temperature": 0.1}
            ),
            timeout=30
        )
        
        print("✅ JSON format is supported!")
        return True
        
    except Exception as e:
        print(f"❌ JSON format test failed: {e}")
        return False


async def main():
    """Run all diagnostic checks."""
    print("\n" + "🏥 "*20)
    print("OLLAMA HEALTH CHECK")
    print("🏥 "*20)
    
    connection_ok = await check_connection()
    if not connection_ok:
        print("\n⚠️  Fix connection issues before proceeding!")
        return False
    
    model_ok = await check_model()
    json_ok = await check_json_format()
    
    print("\n" + "="*70)
    if connection_ok and model_ok and json_ok:
        print("✅ ALL CHECKS PASSED!")
        print("\nYou can now run tests:")
        print("  pytest tests/test_llm_tools_unit.py -v")
        print("  pytest tests/test_llm_tools_integration.py -v -s")
    else:
        print("⚠️  Some checks failed. Please fix issues above.")
    print("="*70 + "\n")
    
    return connection_ok and model_ok and json_ok


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)

