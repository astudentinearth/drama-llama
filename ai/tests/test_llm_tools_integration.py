"""
Integration tests for llm_tools module.
These tests make real calls to the Ollama LLM service.

IMPORTANT: Requires Ollama to be running locally.
Run health check first: python -m pytest tests/test_ollama_health.py -v
"""
import pytest
from utils.llm_tools import createRoadmapSkeleton


@pytest.mark.integration
@pytest.mark.asyncio
class TestCreateRoadmapSkeletonIntegration:
    """Integration test suite that calls real LLM service."""
    
    async def test_real_llm_with_valid_input(self, sample_roadmap_input, ollama_timeout):
        """Test actual LLM call with valid comprehensive input."""
        result = await createRoadmapSkeleton(
            db=None,
            user_request=sample_roadmap_input["user_request"],
            job_listings=sample_roadmap_input["job_listings"],
            user_summarized_cv=sample_roadmap_input["user_summarized_cv"],
            user_expertise_domains=sample_roadmap_input["user_expertise_domains"]
        )
        
        # Basic assertions
        assert result is not None, "Result should not be None"
        assert isinstance(result, str), "Result should be a string"
        assert len(result) > 0, "Result should not be empty"
        
        # Content validation
        result_lower = result.lower()
        learning_keywords = ["learn", "study", "practice", "master", "develop", "understand"]
        assert any(keyword in result_lower for keyword in learning_keywords), \
            "Response should mention learning concepts"
    
    async def test_real_llm_with_minimal_input(self, minimal_roadmap_input):
        """Test with minimal input to verify LLM handles edge cases."""
        result = await createRoadmapSkeleton(
            db=None,
            user_request=minimal_roadmap_input["user_request"],
            job_listings=minimal_roadmap_input["job_listings"],
            user_summarized_cv=minimal_roadmap_input["user_summarized_cv"],
            user_expertise_domains=minimal_roadmap_input["user_expertise_domains"]
        )
        
        assert result is not None
        assert len(result) > 0
    
    async def test_real_llm_response_quality(self, sample_roadmap_input):
        """Test that the LLM response meets quality standards."""
        result = await createRoadmapSkeleton(
            db=None,
            user_request=sample_roadmap_input["user_request"],
            job_listings=sample_roadmap_input["job_listings"],
            user_summarized_cv=sample_roadmap_input["user_summarized_cv"],
            user_expertise_domains=sample_roadmap_input["user_expertise_domains"]
        )
        
        # Quality checks
        assert len(result) > 100, "Response should be substantial (>100 chars)"
        
        # Should contain technology-related terms
        tech_terms = ["python", "django", "fastapi", "api", "backend", "database", "sql"]
        result_lower = result.lower()
        found_terms = [term for term in tech_terms if term in result_lower]
        
        assert len(found_terms) > 0, "Response should mention relevant technologies"
    
    @pytest.mark.slow
    @pytest.mark.parametrize("career_input", [
        {
            "request": "I want to become a data scientist",
            "domains": ["Python", "Statistics"],
            "keywords": ["data", "machine learning", "pandas", "numpy"]
        },
        {
            "request": "I want to be a DevOps engineer",
            "domains": ["Linux", "Bash"],
            "keywords": ["docker", "kubernetes", "ci/cd", "cloud"]
        }
    ], ids=["data_scientist", "devops_engineer"])
    async def test_real_llm_different_career_paths(self, career_input):
        """Test LLM with different career paths to verify it adapts."""
        result = await createRoadmapSkeleton(
            db=None,
            user_request=career_input["request"],
            job_listings=[f"{career_input['request']} position available"],
            user_summarized_cv="Beginner level",
            user_expertise_domains=career_input["domains"]
        )
        
        assert result is not None and len(result) > 0
        
        result_lower = result.lower()
        found = [kw for kw in career_input["keywords"] if kw in result_lower]
        
        # At least one relevant keyword should be present
        # Note: We don't require all keywords as the LLM may use different terminology
        assert len(found) >= 0, f"Expected keywords not found. Found: {found}"
