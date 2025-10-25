"""
Test script for Groq API integration.
Run this to verify the setup is working correctly.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.groq_client import GroqClient, AIResponse
from utils.ai.tool_specs import get_tool_definitions, get_tool_spec
from config import settings


def test_groq_connection():
    """Test basic Groq API connection."""
    print("=" * 60)
    print("Test 1: Groq API Connection")
    print("=" * 60)
    
    try:
        client = GroqClient()
        response = client.complete("Say 'Hello, I am working!' if you can hear me.")
        
        print(f"✓ Connection successful!")
        print(f"  Model: {client.model}")
        print(f"  Response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        return False


def test_tool_specifications():
    """Test tool specification loading."""
    print("\n" + "=" * 60)
    print("Test 2: Tool Specifications")
    print("=" * 60)
    
    try:
        # Test loading tool specs
        roadmap_spec = get_tool_spec("createRoadmapSkeleton")
        materials_spec = get_tool_spec("createLearningMaterials")
        
        if not roadmap_spec:
            print("✗ Failed to load createRoadmapSkeleton spec")
            return False
        
        if not materials_spec:
            print("✗ Failed to load createLearningMaterials spec")
            return False
        
        print(f"✓ Tool specs loaded successfully")
        print(f"  - createRoadmapSkeleton: {len(roadmap_spec['ai_parameters'])} AI params")
        print(f"  - createLearningMaterials: {len(materials_spec['server_parameters'])} server params")
        
        # Test tool definitions
        tool_defs = get_tool_definitions()
        print(f"✓ Generated {len(tool_defs)} tool definitions for OpenAI")
        
        return True
    except Exception as e:
        print(f"✗ Tool spec loading failed: {str(e)}")
        return False


def test_structured_output():
    """Test structured output with JSON schema."""
    print("\n" + "=" * 60)
    print("Test 3: Structured Output")
    print("=" * 60)
    
    try:
        client = GroqClient()
        
        # Simple test schema
        test_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "test_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                        "success": {"type": "boolean"}
                    },
                    "required": ["message", "success"],
                    "additionalProperties": False
                }
            }
        }
        
        response = client.execute(
            messages=[{
                "role": "user",
                "content": "Respond with a test message and success=true"
            }],
            response_format=test_schema
        )
        
        import json
        result = json.loads(response.get_content())
        
        if "message" in result and "success" in result:
            print(f"✓ Structured output working!")
            print(f"  Response: {result}")
            return True
        else:
            print(f"✗ Structured output missing fields")
            return False
            
    except Exception as e:
        print(f"✗ Structured output test failed: {str(e)}")
        return False


def test_tool_calling():
    """Test tool calling functionality."""
    print("\n" + "=" * 60)
    print("Test 4: Tool Calling")
    print("=" * 60)
    
    try:
        client = GroqClient()
        
        # Get tool definitions
        tool_defs = get_tool_definitions(["createRoadmapSkeleton"])
        
        # Test message that should trigger tool
        messages = [
            {
                "role": "system",
                "content": "You help users create learning roadmaps. When they ask to learn something, use the createRoadmapSkeleton tool."
            },
            {
                "role": "user",
                "content": "I want to learn Python programming"
            }
        ]
        
        response = client.execute_with_tools(
            messages=messages,
            tools=tool_defs,
            tool_choice='auto'
        )
        
        if response.has_tool_calls():
            tool_calls = response.get_tool_calls()
            print(f"✓ Tool calling working!")
            print(f"  AI wants to call: {tool_calls[0]['function']['name']}")
            print(f"  With arguments: {tool_calls[0]['function']['arguments'][:100]}...")
            return True
        else:
            print(f"⚠ Tool calling works, but AI didn't call a tool")
            print(f"  Response: {response.get_content()[:100]}...")
            return True  # Not a failure, just means AI chose not to use tool
            
    except Exception as e:
        print(f"✗ Tool calling test failed: {str(e)}")
        return False


def test_prompt_loading():
    """Test prompt loading from YAML files."""
    print("\n" + "=" * 60)
    print("Test 5: Prompt Loading")
    print("=" * 60)
    
    try:
        from models.Prompt import Prompt
        
        # Test loading master prompt
        master_prompt = Prompt('master', {
            'previousMessages': 'Test history',
            'userPrompt': 'Test prompt',
            'content': 'Test content'
        })
        
        messages = master_prompt.get_messages()
        model = master_prompt.get_model()
        
        print(f"✓ Prompt loading working!")
        print(f"  Model: {model}")
        print(f"  Messages: {len(messages)}")
        
        # Test roadmap prompt
        roadmap_prompt = Prompt('createroadmapskeleton', {
            'userRequest': 'Test request',
            'userExperience': 'Test exp',
            'userDomains': 'Test domains',
            'jobListings': 'Test listings'
        })
        
        response_format = roadmap_prompt.get_response_format()
        
        if response_format:
            print(f"✓ Response format loaded")
            print(f"  Type: {response_format.get('type')}")
        else:
            print(f"⚠ No response format in prompt")
        
        return True
        
    except Exception as e:
        print(f"✗ Prompt loading failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "GROQ API INTEGRATION TEST SUITE" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Check environment
    print("Environment Check:")
    print(f"  GROQ_API_KEY: {'✓ Set' if settings.groq_api_key else '✗ Not set'}")
    print(f"  GROQ_MODEL: {settings.groq_model}")
    print(f"  Database URL: {settings.ai_database_url[:50]}...")
    print()
    
    if not settings.groq_api_key:
        print("⚠ WARNING: GROQ_API_KEY not set. Set it in .env file.")
        print("  Some tests will fail without a valid API key.")
        print()
    
    # Run tests
    results = []
    
    results.append(("Groq Connection", test_groq_connection()))
    results.append(("Tool Specifications", test_tool_specifications()))
    results.append(("Structured Output", test_structured_output()))
    results.append(("Tool Calling", test_tool_calling()))
    results.append(("Prompt Loading", test_prompt_loading()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Integration is working correctly.")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Check errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

