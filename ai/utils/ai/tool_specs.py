"""
Tool Specifications Configuration.
Centralized definition of all AI function tools and their parameters.
Inspired by the PHP ToolSpecs.php reference.
"""

from typing import Dict, List, Any, Optional


# Parameter source types
SOURCE_AI = 'ai'           # Filled by AI from tool calls
SOURCE_SERVER = 'server'   # Filled by server/database
SOURCE_CALLBACK = 'callback'  # Function callbacks provided by server


# Complete tool specifications for all AI functions
TOOL_SPECS: Dict[str, Dict[str, Any]] = {
    "createRoadmapSkeleton": {
        "description": (
            "Create a personalized learning roadmap skeleton based on user's career goals, experience, "
            "and optional job listings. This generates a structured list of learning goals with priorities, "
            "time estimates, and dependencies, plus a capstone graduation project that integrates all learned skills. "
            "Use this when the user wants to create a learning path, prepare for a specific role, or skill up in a domain."
        ),
        "ai_required": ["userRequest"],
        "ai_parameters": {
            "userRequest": {
                "type": "string",
                "description": "The user's specific request or goal (e.g., 'I want to become a Python backend developer')",
                "source": SOURCE_AI
            },
            "userExperience": {
                "type": "string",
                "description": "User's current experience and background (optional). Can be extracted from CV or profile.",
                "default": "",
                "source": SOURCE_AI
            },
            "userDomains": {
                "type": "string",
                "description": "Domains or fields the user is interested in or has experience with (optional).",
                "default": "",
                "source": SOURCE_AI
            },
            "jobListings": {
                "type": "string",
                "description": "Job listings or descriptions the user wants to prepare for (optional, only from ourdomain.com).",
                "default": "",
                "source": SOURCE_AI
            },
            "numberOfGoals": {
                "type": "integer",
                "description": "Number of learning goals to generate (default: 5-8, range: 3-15)",
                "default": 6,
                "minimum": 3,
                "maximum": 15,
                "source": SOURCE_AI
            }
        },
        "server_parameters": {
            "session_id": {
                "type": "integer",
                "description": "Session ID for context and storing results",
                "source": SOURCE_SERVER,
                "required": True
            }
        },
        "response_schema": {
            "type": "object",
            "properties": {
                "goals": {
                    "type": "array",
                    "description": "Array of learning goals ordered by priority and dependencies",
                    "items": {
                        "type": "object",
                        "properties": {
                            "goal_number": {
                                "type": "integer",
                                "description": "Sequential goal number (1, 2, 3, ...)"
                            },
                            "title": {
                                "type": "string",
                                "description": "Clear, specific title for the learning goal"
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of what will be learned and why it's important"
                            },
                            "priority": {
                                "type": "integer",
                                "description": "Priority level (1-5, where 1 is highest priority)",
                                "minimum": 1,
                                "maximum": 5
                            },
                            "estimated_hours": {
                                "type": "integer",
                                "description": "Estimated hours to complete this goal"
                            },
                            "prerequisites": {
                                "type": "array",
                                "description": "List of prerequisite goal titles (if any)",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["goal_number", "title", "description", "priority", "estimated_hours"]
                    }
                },
                "graduation_project": {
                    "type": "string",
                    "description": "Detailed description of a capstone project that integrates all learned skills"
                },
                "graduation_project_title": {
                    "type": "string",
                    "description": "Title of the graduation/capstone project"
                }
            },
            "required": ["goals", "graduation_project", "graduation_project_title"]
        }
    },
    
    "createLearningMaterials": {
        "description": (
            "Create comprehensive learning materials for goals within a roadmap. "
            "This generates detailed content including explanations, examples, exercises, and resources. "
            "The materials are contextualized with the previous and next goals to ensure smooth learning progression. "
            "Use this after a roadmap has been created and the user wants to start learning. "
            "You can either specify a single goal_id for one goal, or set generate_for_all_goals=true to create materials for ALL goals in parallel."
        ),
        "ai_required": [],
        "ai_parameters": {
            "goal_id": {
                "type": "integer",
                "description": "Database ID of a specific goal to create materials for. Use the 'Goal ID' number from the available goals list. Optional if generate_for_all_goals is true.",
                "source": SOURCE_AI
            },
            "generate_for_all_goals": {
                "type": "boolean",
                "description": "If true, generate learning materials for ALL goals in the roadmap in parallel. If false or omitted, only generate for the specified goal_id.",
                "source": SOURCE_AI
            }
        },
        "server_parameters": {
            "session_id": {
                "type": "integer",
                "description": "Session ID for context",
                "source": SOURCE_SERVER,
                "required": True
            },
            "currentGoalTitle": {
                "type": "string",
                "description": "Title of the current goal",
                "source": SOURCE_SERVER,
                "required": True
            },
            "currentGoalDescription": {
                "type": "string",
                "description": "Description of the current goal",
                "source": SOURCE_SERVER,
                "required": True
            },
            "previousGoalTitle": {
                "type": "string",
                "description": "Title of the previous goal (for context)",
                "source": SOURCE_SERVER,
                "required": False,
                "default": ""
            },
            "previousGoalDescription": {
                "type": "string",
                "description": "Description of the previous goal (for context)",
                "source": SOURCE_SERVER,
                "required": False,
                "default": ""
            },
            "nextGoalTitle": {
                "type": "string",
                "description": "Title of the next goal (for context)",
                "source": SOURCE_SERVER,
                "required": False,
                "default": ""
            },
            "nextGoalDescription": {
                "type": "string",
                "description": "Description of the next goal (for context)",
                "source": SOURCE_SERVER,
                "required": False,
                "default": ""
            }
        },
        "response_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the learning material"
                },
                "description": {
                    "type": "string",
                    "description": "Brief description of what this material covers"
                },
                "content": {
                    "type": "string",
                    "description": "Main learning content in Markdown format with detailed explanations"
                },
                "exercises": {
                    "type": "array",
                    "description": "List of practical exercises to reinforce learning",
                    "items": {"type": "string"}
                },
                "examples": {
                    "type": "array",
                    "description": "List of examples demonstrating concepts",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "code": {"type": "string"},
                            "explanation": {"type": "string"}
                        }
                    }
                },
                "estimated_time_minutes": {
                    "type": "integer",
                    "description": "Estimated time to complete this material in minutes"
                }
            },
            "required": ["title", "description", "content_markdown", "exercises", "estimated_time_minutes"]
        }
    }
}


def get_tool_spec(tool_name: str) -> Optional[Dict[str, Any]]:
    """
    Get tool specification by name.
    
    Args:
        tool_name: Name of the tool
    
    Returns:
        Tool specification dict or None if not found
    """
    return TOOL_SPECS.get(tool_name)


def get_tool_names() -> List[str]:
    """
    Get all available tool names.
    
    Returns:
        List of tool names
    """
    return list(TOOL_SPECS.keys())


def get_tool_definitions(available_tools: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Get OpenAI-compatible tool definitions.
    
    Args:
        available_tools: Optional list of tool names to include. If None, includes all tools.
    
    Returns:
        List of tool definitions in OpenAI format
    """
    tools_to_include = available_tools if available_tools else get_tool_names()
    definitions = []
    
    for tool_name in tools_to_include:
        spec = get_tool_spec(tool_name)
        if not spec:
            continue
        
        # Build properties from ai_parameters only (server params are filled by backend)
        properties = {}
        for param_name, param_spec in spec.get('ai_parameters', {}).items():
            # Create a clean spec without source metadata
            clean_spec = {
                'type': param_spec['type'],
                'description': param_spec['description']
            }
            
            # Add optional fields if present
            if 'default' in param_spec:
                clean_spec['default'] = param_spec['default']
            if 'minimum' in param_spec:
                clean_spec['minimum'] = param_spec['minimum']
            if 'maximum' in param_spec:
                clean_spec['maximum'] = param_spec['maximum']
            if 'enum' in param_spec:
                clean_spec['enum'] = param_spec['enum']
            
            properties[param_name] = clean_spec
        
        # Build required list
        required = spec.get('ai_required', [])
        
        # Create OpenAI tool definition
        definition = {
            'type': 'function',
            'function': {
                'name': tool_name,
                'description': spec['description'],
                'parameters': {
                    'type': 'object',
                    'properties': properties if properties else {},
                    'required': required
                }
            }
        }
        
        definitions.append(definition)
    
    return definitions


def validate_tool_parameters(tool_name: str, parameters: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate tool parameters against specification.
    
    Args:
        tool_name: Name of the tool
        parameters: Parameters to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    spec = get_tool_spec(tool_name)
    if not spec:
        return False, f"Tool '{tool_name}' not found"
    
    # Check required AI parameters
    for required_param in spec.get('ai_required', []):
        if required_param not in parameters:
            return False, f"Missing required parameter: {required_param}"
    
    # Validate parameter types
    for param_name, param_value in parameters.items():
        if param_name in spec.get('ai_parameters', {}):
            param_spec = spec['ai_parameters'][param_name]
            expected_type = param_spec['type']
            
            # Type checking
            type_map = {
                'string': str,
                'integer': int,
                'boolean': bool,
                'array': list,
                'object': dict
            }
            
            if expected_type in type_map:
                expected_python_type = type_map[expected_type]
                if not isinstance(param_value, expected_python_type):
                    return False, f"Parameter '{param_name}' should be {expected_type}, got {type(param_value).__name__}"
            
            # Range validation for integers
            if expected_type == 'integer':
                if 'minimum' in param_spec and param_value < param_spec['minimum']:
                    return False, f"Parameter '{param_name}' must be >= {param_spec['minimum']}"
                if 'maximum' in param_spec and param_value > param_spec['maximum']:
                    return False, f"Parameter '{param_name}' must be <= {param_spec['maximum']}"
    
    return True, None


def get_response_schema(tool_name: str) -> Optional[Dict[str, Any]]:
    """
    Get the response schema for a tool.
    
    Args:
        tool_name: Name of the tool
    
    Returns:
        Response schema dict or None if not found
    """
    spec = get_tool_spec(tool_name)
    if spec:
        return spec.get('response_schema')
    return None


def get_server_parameters(tool_name: str) -> Dict[str, Any]:
    """
    Get server parameters specification for a tool.
    
    Args:
        tool_name: Name of the tool
    
    Returns:
        Server parameters dict
    """
    spec = get_tool_spec(tool_name)
    if spec:
        return spec.get('server_parameters', {})
    return {}


# ============================================================================
# Graduation Project Tools
# ============================================================================

TOOL_SPECS["createGraduationProjectQuestions"] = {
    "description": (
        "Generate 5 comprehensive open-ended questions for graduation project assessment. "
        "These questions test synthesis, application, and evaluation across all learning goals. "
        "Each question includes a detailed evaluation rubric and requires material citations. "
        "Use this when a learner has completed their roadmap materials and is ready for final assessment."
    ),
    "ai_required": [],  # AI generates questions from structured data
    "ai_parameters": {},
    "server_parameters": {
        "session_id": {
            "type": "integer",
            "description": "Session ID containing the roadmap and materials",
            "source": SOURCE_SERVER
        },
        "graduation_project_title": {
            "type": "string",
            "description": "Title of the graduation project",
            "source": SOURCE_SERVER
        },
        "graduation_project_description": {
            "type": "string",
            "description": "Full description of the graduation project",
            "source": SOURCE_SERVER
        },
        "goals": {
            "type": "array",
            "description": "Array of goals with their materials",
            "source": SOURCE_SERVER
        },
        "total_goals": {
            "type": "integer",
            "description": "Total number of goals",
            "source": SOURCE_SERVER
        }
    },
    "response_schema": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question_id": {"type": "string"},
                        "prompt": {"type": "string"},
                        "rationale": {"type": "string"},
                        "goals_covered": {"type": "array", "items": {"type": "integer"}},
                        "materials_covered": {"type": "array", "items": {"type": "integer"}},
                        "expected_competencies": {"type": "array", "items": {"type": "string"}},
                        "difficulty": {"type": "string", "enum": ["introductory", "intermediate", "advanced"]},
                        "estimated_time_minutes": {"type": "integer"},
                        "evaluation_rubric": {"type": "array", "items": {"type": "string"}},
                        "answer_min_chars": {"type": "integer"},
                        "answer_max_chars": {"type": "integer"},
                        "requires_material_citations": {"type": "boolean"}
                    }
                }
            }
        }
    }
}

TOOL_SPECS["evaluateGraduationProjectAnswer"] = {
    "description": (
        "Evaluate a student's answer to a graduation project question. "
        "Provides detailed scoring against the evaluation rubric, assesses competency demonstration, "
        "evaluates citation quality, and generates constructive feedback. "
        "Use this when a learner submits answers to graduation project questions."
    ),
    "ai_required": [],  # AI evaluates based on structured data
    "ai_parameters": {},
    "server_parameters": {
        "question_id": {
            "type": "string",
            "description": "The question identifier",
            "source": SOURCE_SERVER
        },
        "question_prompt": {
            "type": "string",
            "description": "The full question text",
            "source": SOURCE_SERVER
        },
        "expected_competencies": {
            "type": "array",
            "description": "List of competencies this question tests",
            "source": SOURCE_SERVER
        },
        "evaluation_rubric": {
            "type": "array",
            "description": "Evaluation criteria for the question",
            "source": SOURCE_SERVER
        },
        "relevant_materials": {
            "type": "array",
            "description": "Learning materials related to this question",
            "source": SOURCE_SERVER
        },
        "answer_text": {
            "type": "string",
            "description": "Student's answer text",
            "source": SOURCE_SERVER
        },
        "answer_length": {
            "type": "integer",
            "description": "Length of the answer in characters",
            "source": SOURCE_SERVER
        },
        "citations": {
            "type": "array",
            "description": "Citations provided by the student",
            "source": SOURCE_SERVER
        },
        "citations_count": {
            "type": "integer",
            "description": "Number of citations provided",
            "source": SOURCE_SERVER
        }
    },
    "response_schema": {
        "type": "object",
        "properties": {
            "overall_score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "rubric_scores": {
                "type": "object",
                "additionalProperties": {"type": "number"}
            },
            "competency_assessment": {
                "type": "object",
                "additionalProperties": {"type": "string"}
            },
            "citation_quality_score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "strengths": {"type": "array", "items": {"type": "string"}},
            "areas_for_improvement": {"type": "array", "items": {"type": "string"}},
            "feedback": {"type": "string"}
        }
    }
}
