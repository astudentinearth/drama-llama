"""
Shared pytest fixtures and configuration for all tests.
"""
import pytest
from typing import Dict, Any, List
from unittest.mock import AsyncMock, MagicMock
from models.schemas import RoadmapResponse, Goal


# ============= Test Data Fixtures =============

@pytest.fixture
def sample_roadmap_input() -> Dict[str, Any]:
    """Sample input data for roadmap creation tests."""
    return {
        "user_request": "I want to become a backend developer",
        "job_listings": [
            "Backend developer position requiring Python, Django, REST API, SQL",
            "Software engineer role with FastAPI, PostgreSQL, Docker"
        ],
        "user_summarized_cv": "3 years experience in frontend development with React and JavaScript",
        "user_expertise_domains": ["JavaScript", "React", "HTML/CSS"]
    }


@pytest.fixture
def minimal_roadmap_input() -> Dict[str, Any]:
    """Minimal input data for edge case testing."""
    return {
        "user_request": "I want to learn Python",
        "job_listings": ["Python developer needed"],
        "user_summarized_cv": "No experience",
        "user_expertise_domains": []
    }


@pytest.fixture
def complex_job_listings() -> List[str]:
    """Complex job listings for comprehensive testing."""
    return [
        "Senior Backend Engineer - Python, Django, PostgreSQL, Redis, Docker, AWS",
        "Full Stack Developer - React, Node.js, Express, MongoDB, GraphQL",
        "DevOps Engineer - Kubernetes, Terraform, CI/CD, Jenkins, AWS/Azure"
    ]


# ============= Mock Fixtures =============

@pytest.fixture
def mock_successful_llm_response() -> Dict[str, Any]:
    """Mock successful Ollama API response."""
    return {
        "success": True,
        "response": "Roadmap generated successfully"
    }


@pytest.fixture
def mock_failed_llm_response() -> Dict[str, Any]:
    """Mock failed Ollama API response."""
    return {
        "success": False,
        "error": "Connection timeout"
    }


@pytest.fixture
def mock_prompt():
    """Mock Prompt instance with common methods."""
    mock = MagicMock()
    mock.get_user_prompt.return_value = "User prompt content"
    mock.get_system_prompt.return_value = "System prompt content"
    mock.get_model.return_value = "llama3.2:1b"
    mock.get_messages.return_value = [
        {"role": "system", "content": "System prompt content"},
        {"role": "user", "content": "User prompt content"}
    ]
    return mock


@pytest.fixture
def mock_ollama_client(mock_successful_llm_response):
    """Mock OllamaClient with default successful response."""
    mock = MagicMock()
    mock.generate = AsyncMock(return_value=mock_successful_llm_response)
    mock.model = "llama3.2:1b"
    mock.timeout = 300
    return mock


@pytest.fixture
def mock_roadmap_schema() -> Dict[str, Any]:
    """Mock RoadmapResponse JSON schema."""
    return {
        "type": "object",
        "properties": {
            "goals": {"type": "array"},
            "total_estimated_weeks": {"type": "integer"},
            "graduation_project": {"type": "string"}
        },
        "required": ["goals", "total_estimated_weeks", "graduation_project"]
    }


# ============= Prompt Test Fixtures =============

@pytest.fixture
def sample_prompt_format() -> Dict[str, Any]:
    """Sample format dictionary for prompt variable substitution."""
    return {
        "content": "Test content here",
        "previousMessages": "Previous message 1\nPrevious message 2",
        "userPrompt": "What should I learn?",
    }


@pytest.fixture
def roadmap_prompt_format() -> Dict[str, Any]:
    """Roadmap-specific format dictionary."""
    return {
        "userRequest": "I want to become a backend developer",
        "jobListings": ["Backend dev position"],
        "userExperience": "2 years frontend",
        "userDomains": ["JavaScript", "React"]
    }


# ============= Integration Test Helpers =============

@pytest.fixture
def ollama_timeout() -> int:
    """Timeout for integration tests that call real LLM."""
    return 90


# ============= Pytest Markers =============

def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests with mocked dependencies (fast)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that call real services (slow)"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take significant time to run"
    )

