# app/api.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.bot import chat as bot_chat

router = APIRouter()

@router.get("/chat/")
async def chat(prompt: str):
    async def generate():
        async for response in bot_chat(prompt):
            yield response.encode("utf-8")

    return StreamingResponse(generate(), media_type="text/plain")
