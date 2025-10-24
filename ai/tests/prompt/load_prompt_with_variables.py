# Test loading a prompt with variables
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from ai.models.Prompt import Prompt

def test_load_prompt_with_variables():
    prompt = Prompt("master", {
        "content": "Test content here",
        "previousMessages": "Previous message 1\nPrevious message 2",
        "userPrompt": "What should I learn?",
    })
    
    prompt_data = prompt.get_prompt()
    messages = prompt.get_messages()
    
    # Convert all messages to a single string for checking
    all_content = ""
    for message in messages:
        all_content += message.get('content', '')
    
    # Check that variables were replaced (without spaces)
    assert "{{content}}" not in all_content, "content variable was not replaced"
    assert "{{previousMessages}}" not in all_content, "previousMessages variable was not replaced"
    assert "{{userPrompt}}" not in all_content, "userPrompt variable was not replaced"
    
    # Check that the actual values are present
    assert "Test content here" in all_content, "content value not found"
    assert "Previous message 1" in all_content, "previousMessages value not found"
    assert "What should I learn?" in all_content, "userPrompt value not found"
    assert "Previous message 1" in all_content, "previousMessages value not found"
    assert "What should I learn?" in all_content, "userPrompt value not found"
    
    print("✅ Test passed: All variables were properly replaced")
    print(f"\n{'='*60}")
    print("PROMPT DATA STRUCTURE:")
    print(f"{'='*60}")
    print(f"Model: {prompt_data.get('model')}")
    print(f"Model Provider: {prompt_data.get('modelProvider')}")
    print(f"Number of messages: {len(messages)}")
    print(f"\n{'='*60}")
    print("MESSAGES:")
    print(f"{'='*60}")
    for i, message in enumerate(messages, 1):
        print(f"\n[Message {i}] Role: {message.get('role')}")
        print(f"Content preview (first 200 chars):")
        content = message.get('content', '')
        print(content[:200] + "..." if len(content) > 200 else content)

if __name__ == "__main__":
    test_load_prompt_with_variables()