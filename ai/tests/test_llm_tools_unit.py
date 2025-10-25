"""
Unit tests for llm_tools module.
Tests createRoadmapSkeleton function with mocked dependencies.
"""
import pytest
from unittest.mock import AsyncMock, patch
from utils.llm_tools import createRoadmapSkeleton


@pytest.mark.unit
@pytest.mark.asyncio
class TestCreateRoadmapSkeleton:
    """Unit test suite for createRoadmapSkeleton function."""
    
    async def test_successful_roadmap_creation(
        self, 
        sample_roadmap_input, 
        mock_successful_llm_response, 
        mock_prompt,
        mock_roadmap_schema
    ):
        """Test successful roadmap creation with valid inputs."""
        with patch('models.Prompt') as MockPrompt, \
             patch('services.OllamaClient') as MockOllamaClient:
            
            # Setup mocks
            MockPrompt.return_value = mock_prompt
            mock_client = MockOllamaClient.return_value
            mock_client.generate = AsyncMock(return_value=mock_successful_llm_response)
            
            # Execute
            result = await createRoadmapSkeleton(
                db=None,
                user_request=sample_roadmap_input["user_request"],
                job_listings=sample_roadmap_input["job_listings"],
                user_summarized_cv=sample_roadmap_input["user_summarized_cv"],
                user_expertise_domains=sample_roadmap_input["user_expertise_domains"]
            )
            
            # Assertions
            assert result == "Roadmap generated successfully"
            MockPrompt.assert_called_once()
            mock_client.generate.assert_called_once()
            
            # Verify prompt parameters
            call_args = MockPrompt.call_args
            assert call_args[0][0] == "createroadmapskeleton"
            assert "userRequest" in call_args[1]["format"]
            assert "jobListings" in call_args[1]["format"]
    
    @pytest.mark.parametrize("field,value", [
        ("user_request", ""),
        ("user_request", None),
    ])
    async def test_empty_user_request(
        self, 
        field, 
        value, 
        mock_successful_llm_response, 
        mock_prompt
    ):
        """Test handling of empty or None user request."""
        with patch('models.Prompt') as MockPrompt, \
             patch('services.OllamaClient') as MockOllamaClient:
            
            MockPrompt.return_value = mock_prompt
            mock_client = MockOllamaClient.return_value
            mock_client.generate = AsyncMock(return_value=mock_successful_llm_response)
            
            result = await createRoadmapSkeleton(
                db=None,
                user_request=value,
                job_listings=["Job listing 1"],
                user_summarized_cv="Some CV",
                user_expertise_domains=["Domain1"]
            )
            
            assert result == "Roadmap generated successfully"
            call_args = MockPrompt.call_args
            assert call_args[1]["format"]["userRequest"] == ""
    
    @pytest.mark.parametrize("job_listings,domains", [
        ([], []),
        (None, None),
        ([], None),
        (None, []),
    ])
    async def test_empty_lists(
        self, 
        job_listings, 
        domains, 
        mock_successful_llm_response, 
        mock_prompt
    ):
        """Test handling of empty or None lists."""
        with patch('models.Prompt') as MockPrompt, \
             patch('services.OllamaClient') as MockOllamaClient:
            
            MockPrompt.return_value = mock_prompt
            mock_client = MockOllamaClient.return_value
            mock_client.generate = AsyncMock(return_value=mock_successful_llm_response)
            
            result = await createRoadmapSkeleton(
                db=None,
                user_request="Test request",
                job_listings=job_listings,
                user_summarized_cv="CV content",
                user_expertise_domains=domains
            )
            
            assert result == "Roadmap generated successfully"
            call_args = MockPrompt.call_args
            assert call_args[1]["format"]["jobListings"] == []
            assert call_args[1]["format"]["userDomains"] == []
    
    async def test_ollama_failure(self, mock_prompt, mock_failed_llm_response):
        """Test handling of Ollama API failure."""
        with patch('models.Prompt') as MockPrompt, \
             patch('services.OllamaClient') as MockOllamaClient:
            
            MockPrompt.return_value = mock_prompt
            mock_client = MockOllamaClient.return_value
            mock_client.generate = AsyncMock(return_value=mock_failed_llm_response)
            
            with pytest.raises(Exception) as exc_info:
                await createRoadmapSkeleton(
                    db=None,
                    user_request="Test request",
                    job_listings=["Job listing"],
                    user_summarized_cv="CV",
                    user_expertise_domains=["Domain"]
                )
            
            assert "Failed to generate roadmap skeleton" in str(exc_info.value)
            assert "Connection timeout" in str(exc_info.value)
    
    async def test_prompt_loading_failure(self):
        """Test handling of prompt loading failure."""
        with patch('models.Prompt') as MockPrompt:
            MockPrompt.return_value = None
            
            with pytest.raises(AssertionError) as exc_info:
                await createRoadmapSkeleton(
                    db=None,
                    user_request="Test",
                    job_listings=["Job"],
                    user_summarized_cv="CV",
                    user_expertise_domains=["Domain"]
                )
            
            assert "could not be loaded" in str(exc_info.value)
    
    async def test_ollama_client_parameters(
        self, 
        sample_roadmap_input, 
        mock_successful_llm_response, 
        mock_prompt,
        mock_roadmap_schema
    ):
        """Test that OllamaClient.generate is called with correct parameters."""
        with patch('models.Prompt') as MockPrompt, \
             patch('services.OllamaClient') as MockOllamaClient, \
             patch('models.RoadmapResponse') as MockRoadmapResponse:
            
            MockPrompt.return_value = mock_prompt
            mock_client = MockOllamaClient.return_value
            mock_client.generate = AsyncMock(return_value=mock_successful_llm_response)
            MockRoadmapResponse.model_json_schema.return_value = mock_roadmap_schema
            
            await createRoadmapSkeleton(
                db=None,
                user_request=sample_roadmap_input["user_request"],
                job_listings=sample_roadmap_input["job_listings"],
                user_summarized_cv=sample_roadmap_input["user_summarized_cv"],
                user_expertise_domains=sample_roadmap_input["user_expertise_domains"]
            )
            
            # Verify OllamaClient.generate call
            mock_client.generate.assert_called_once()
            call_kwargs = mock_client.generate.call_args[1]
            
            assert call_kwargs["prompt"] == "User prompt content"
            assert call_kwargs["system_prompt"] == "System prompt content"
            assert call_kwargs["temperature"] == 0.2
            assert call_kwargs["format"] == mock_roadmap_schema
    
    async def test_response_without_response_key(self, mock_prompt):
        """Test handling when Ollama response doesn't contain 'response' key."""
        with patch('models.Prompt') as MockPrompt, \
             patch('services.OllamaClient') as MockOllamaClient:
            
            MockPrompt.return_value = mock_prompt
            mock_client = MockOllamaClient.return_value
            mock_client.generate = AsyncMock(return_value={"success": True})
            
            result = await createRoadmapSkeleton(
                db=None,
                user_request="Test",
                job_listings=["Job"],
                user_summarized_cv="CV",
                user_expertise_domains=["Domain"]
            )
            
            assert result == ""
    
    async def test_with_complex_job_listings(
        self, 
        complex_job_listings, 
        mock_successful_llm_response, 
        mock_prompt
    ):
        """Test with multiple detailed job listings."""
        with patch('models.Prompt') as MockPrompt, \
             patch('services.OllamaClient') as MockOllamaClient:
            
            MockPrompt.return_value = mock_prompt
            mock_client = MockOllamaClient.return_value
            mock_client.generate = AsyncMock(return_value=mock_successful_llm_response)
            
            result = await createRoadmapSkeleton(
                db=None,
                user_request="I want to advance my career",
                job_listings=complex_job_listings,
                user_summarized_cv="5 years as junior developer",
                user_expertise_domains=["Python", "Basic SQL"]
            )
            
            assert result == "Roadmap generated successfully"
            call_args = MockPrompt.call_args
            assert len(call_args[1]["format"]["jobListings"]) == 3

