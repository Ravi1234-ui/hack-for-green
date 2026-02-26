from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.chatbot import ask

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Request Model ----------------
class QuestionRequest(BaseModel):
    question: str

# ---------------- Endpoint ----------------
@app.post("/ask")
def ask_question(request: QuestionRequest):
    answer = ask(request.question)
    return {"answer": answer}