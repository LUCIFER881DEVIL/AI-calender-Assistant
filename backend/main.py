from fastapi import FastAPI, Request
from pydantic import BaseModel
from backend.agent_flow import run_agent_flow

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/chat")
async def chat(msg: Message):
    reply = await run_agent_flow(msg.message)
    return {"response": reply}
