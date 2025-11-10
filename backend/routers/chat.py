from fastapi import APIRouter
from backend.agents.master_agent import MasterAgent

router = APIRouter(prefix="/chat", tags=["Chat"])
agent = MasterAgent()

@router.post("/")
def chat_with_user(request: dict):
    user_message = request.get("message")
    response = agent.process_message(user_message)
    return response