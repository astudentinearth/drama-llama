from models.Prompt import Prompt
from models.schemas import RoadmapResponse
from services.OllamaClient import OllamaClient
import asyncio

"""
When user stated he/she want to apply for a job, how can I develop my self etc. this tool should be triggered.
This tool briefly takes summary of user request, and the links mentioned.
"""
async def createRoadmapSkeleton(db, user_request: str, job_listings: list[str], user_summarized_cv: str, user_expertise_domains: list[str]) -> str:
    jobListings = ["this is an example job listing, requiring skills in python, django, rest api, sql, git, docker"]
    
    # 0. load prompt with variables
    roadmaprequest = {
        "userRequest": user_request if user_request else "",
        "jobListings": job_listings if job_listings else [],
        "userExperience": user_summarized_cv if user_summarized_cv else "",
        "userDomains": user_expertise_domains if user_expertise_domains else []
    }
    
    prompt = Prompt("createroadmapskeleton", format=roadmaprequest)
    assert prompt is not None, "Prompt 'createroadmapskeleton' could not be loaded."
    
    # 1. using users expertise domain(s) and users past experiences, generate search sentences and store
    
    # 2. search web for roadmaps/learningpaths about the requested expertise and store
    
    # 3. then using user request and related joblisting summarizations, find users needs to create roadmap (for example: user knows node.js , job needs express.js , don't request to learn node.js, since they are related to eachother)
    # 3.1 get joblistings from job microservice
    
    
    
    # 4. using created needs, create an ordered list of things-to-learn array and a end of roadmap project that summarizes all the materials and puts in use.
    # use ollama client here with the loaded prompt
    ollama_client = OllamaClient()
    response = ollama_client.generate(
        prompt=prompt.get_user_prompt(),
        system_prompt=prompt.get_system_prompt(),
        temperature=0.2,
        format=RoadmapResponse.model_json_schema()
    )
    
    async_response = await response
    if not async_response.get("success", False):
        raise Exception(f"Failed to generate roadmap skeleton: {async_response.get('error', 'Unknown error')}")
    
    # 5. put things-to-learn array and end of roadmap project details in session-db
    
    # 6. return this array and project inside a friendly/professinal text
    return async_response.get("response", "")