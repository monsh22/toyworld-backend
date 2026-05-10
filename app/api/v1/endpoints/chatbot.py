from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """Eres Toby, el asistente virtual de ToyWorld, una tienda de juguetes.
Ayudas con recomendaciones de juguetes por edad, seguridad infantil, pedidos y envíos.
Política: devoluciones 30 días, envíos 3-5 días hábiles. Contacto: soporte@toyworld.mx
Sé amable y usa emojis. Respuestas cortas, máximo 3 oraciones."""

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@router.post("/")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *[{"role": m.role, "content": m.content} for m in req.messages]
        ],
        max_tokens=300
    )
    return {"reply": response.choices[0].message.content}
