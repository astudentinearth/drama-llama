from typing import Union
from fastapi import FastAPI
from models.schemas import ChatRequest
from utils.llm_tools import master
app = FastAPI()

@app.post("/chat")
async def chat(request: ChatRequest):
    # call master function
    return await master(request)

@app.get("/health")
def health_check():
    return {"status": "ok"}