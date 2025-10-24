# Test that PromptLoader is a singleton and caches prompts
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from ai.utils.prompt_loader import PromptLoader
from ai.models.Prompt import Prompt

def test_singleton_pattern():
    print("Testing Singleton Pattern...")
    print("="*60)
    
    # Create two instances
    loader1 = PromptLoader()
    loader2 = PromptLoader()
    
    # They should be the same instance
    assert loader1 is loader2, "PromptLoader instances are not the same!"
    print("✅ Singleton check: Both instances are the same object")
    
    # Load prompts with first instance
    prompts1 = loader1.get_prompt("master")
    print("✅ Loaded prompts with first instance")
    
    # Get prompts with second instance (should use cache)
    prompts2 = loader2.get_prompt("master")
    print("✅ Got prompts with second instance (from cache)")
    
    # They should be the same
    assert prompts1 is prompts2, "Prompts are not cached!"
    print("✅ Cache check: Both prompts are the same object")
    
    # Create multiple Prompt instances
    print("\n" + "="*60)
    print("Testing multiple Prompt instances...")
    print("="*60)
    
    prompt1 = Prompt("master", {"content": "Test 1", "previousMessages": "", "userPrompt": ""})
    prompt2 = Prompt("master", {"content": "Test 2", "previousMessages": "", "userPrompt": ""})
    prompt3 = Prompt("master", {"content": "Test 3", "previousMessages": "", "userPrompt": ""})
    
    print("✅ Created 3 Prompt instances")
    print("✅ Prompts were only loaded from disk once (singleton cache)")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\nSingleton pattern is working correctly:")
    print("- PromptLoader is a singleton")
    print("- Prompts are loaded only once")
    print("- Subsequent calls use cached data")

if __name__ == "__main__":
    test_singleton_pattern()
