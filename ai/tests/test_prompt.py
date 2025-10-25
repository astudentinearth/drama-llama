"""
Unit tests for Prompt class and PromptLoader.
"""
import pytest
from models.Prompt import Prompt
from utils.prompt_loader import PromptLoader


@pytest.mark.unit
class TestPromptLoader:
    """Test suite for PromptLoader singleton pattern."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton before each test."""
        PromptLoader.reset()
        yield
        PromptLoader.reset()
    
    def test_singleton_pattern(self):
        """Test that PromptLoader implements singleton pattern."""
        loader1 = PromptLoader()
        loader2 = PromptLoader()
        
        assert loader1 is loader2, "PromptLoader instances should be the same"
    
    def test_prompt_caching(self):
        """Test that prompts are cached after first load."""
        loader1 = PromptLoader()
        loader2 = PromptLoader()
        
        prompts1 = loader1.get_prompt("master")
        prompts2 = loader2.get_prompt("master")
        
        assert prompts1 is prompts2, "Prompts should be cached"
    
    def test_get_prompt_case_insensitive(self):
        """Test that prompt names are case-insensitive."""
        loader = PromptLoader()
        
        prompt_lower = loader.get_prompt("master")
        prompt_upper = loader.get_prompt("MASTER")
        
        assert prompt_lower is prompt_upper
    
    def test_get_nonexistent_prompt(self):
        """Test that getting a non-existent prompt raises ValueError."""
        loader = PromptLoader()
        
        with pytest.raises(ValueError, match="Prompt 'nonexistent' not found"):
            loader.get_prompt("nonexistent")


@pytest.mark.unit
class TestPrompt:
    """Test suite for Prompt class."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton before each test."""
        PromptLoader.reset()
        yield
        PromptLoader.reset()
    
    def test_prompt_initialization(self, sample_prompt_format):
        """Test basic Prompt initialization."""
        prompt = Prompt("master", format=sample_prompt_format)
        
        assert prompt is not None
        assert prompt.name == "master"
        assert prompt.format == sample_prompt_format
    
    def test_variable_substitution(self, sample_prompt_format):
        """Test that variables are properly replaced in prompt content."""
        prompt = Prompt("master", format=sample_prompt_format)
        
        messages = prompt.get_messages()
        all_content = " ".join(msg.get('content', '') for msg in messages)
        
        # Check that variables were replaced
        assert "{{content}}" not in all_content
        assert "{{previousMessages}}" not in all_content
        assert "{{userPrompt}}" not in all_content
        
        # Check that actual values are present
        assert "Test content here" in all_content
        assert "Previous message 1" in all_content
        assert "What should I learn?" in all_content
    
    def test_variable_substitution_with_spaces(self, sample_prompt_format):
        """Test that variables with spaces are also replaced."""
        prompt = Prompt("master", format=sample_prompt_format)
        
        messages = prompt.get_messages()
        all_content = " ".join(msg.get('content', '') for msg in messages)
        
        # Check both {{key}} and {{ key }} patterns are replaced
        assert "{{ content }}" not in all_content
        assert "{{ previousMessages }}" not in all_content
        assert "{{ userPrompt }}" not in all_content
    
    def test_get_model(self, sample_prompt_format):
        """Test getting model name from prompt."""
        prompt = Prompt("master", format=sample_prompt_format)
        model = prompt.get_model()
        
        assert model is not None
        assert isinstance(model, str)
    
    def test_get_system_prompt(self, sample_prompt_format):
        """Test getting system prompt content."""
        prompt = Prompt("master", format=sample_prompt_format)
        system_prompt = prompt.get_system_prompt()
        
        assert system_prompt is not None
        assert isinstance(system_prompt, str)
    
    def test_get_user_prompt(self, sample_prompt_format):
        """Test getting user prompt content."""
        prompt = Prompt("master", format=sample_prompt_format)
        user_prompt = prompt.get_user_prompt()
        
        assert user_prompt is not None
        assert isinstance(user_prompt, str)
    
    def test_get_messages(self, sample_prompt_format):
        """Test getting messages array."""
        prompt = Prompt("master", format=sample_prompt_format)
        messages = prompt.get_messages()
        
        assert messages is not None
        assert isinstance(messages, list)
        assert len(messages) > 0
        
        # Check message structure
        for message in messages:
            assert "role" in message
            assert "content" in message
            assert message["role"] in ["system", "user", "assistant"]
    
    def test_get_prompt_data(self, sample_prompt_format):
        """Test getting full prompt data structure."""
        prompt = Prompt("master", format=sample_prompt_format)
        prompt_data = prompt.get_prompt()
        
        assert prompt_data is not None
        assert isinstance(prompt_data, dict)
        assert "model" in prompt_data
        assert "messages" in prompt_data
    
    def test_roadmap_prompt(self, roadmap_prompt_format):
        """Test loading roadmap-specific prompt."""
        prompt = Prompt("createroadmapskeleton", format=roadmap_prompt_format)
        
        assert prompt is not None
        
        user_prompt = prompt.get_user_prompt()
        system_prompt = prompt.get_system_prompt()
        
        assert len(user_prompt) > 0
        assert len(system_prompt) > 0
        
        # Check that roadmap-specific variables were replaced
        all_content = user_prompt + system_prompt
        assert "I want to become a backend developer" in all_content
        assert "Backend dev position" in all_content
    
    @pytest.mark.parametrize("format_dict", [
        {},  # Empty dict
        {"key": "value"},  # Unknown keys
    ])
    def test_prompt_with_missing_variables(self, format_dict):
        """Test that prompt works even with missing variables."""
        # Should not raise exception
        prompt = Prompt("master", format=format_dict)
        
        assert prompt is not None
        messages = prompt.get_messages()
        assert len(messages) > 0
    
    def test_multiple_prompt_instances(self, sample_prompt_format):
        """Test creating multiple Prompt instances uses cached loader."""
        prompt1 = Prompt("master", format={"content": "Test 1", "previousMessages": "", "userPrompt": ""})
        prompt2 = Prompt("master", format={"content": "Test 2", "previousMessages": "", "userPrompt": ""})
        prompt3 = Prompt("master", format={"content": "Test 3", "previousMessages": "", "userPrompt": ""})
        
        # All should be created successfully
        assert prompt1 is not None
        assert prompt2 is not None
        assert prompt3 is not None
        
        # They should have different format dicts
        assert prompt1.format["content"] == "Test 1"
        assert prompt2.format["content"] == "Test 2"
        assert prompt3.format["content"] == "Test 3"

