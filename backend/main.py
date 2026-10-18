
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.safety import check_request_safety
from backend.router import route_query


# -------------------------------
# Initialize FastAPI
# -------------------------------

app = FastAPI(
    title="CampusAI",
    description="AWS-powered Generative AI Voice Assistant",
    version="1.0.0"
)


# -------------------------------
# CORS Configuration
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)


# -------------------------------
# Frontend File Path
# -------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_FILE = BASE_DIR / "frontend" / "index.html"


# -------------------------------
# Request Model
# -------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# -------------------------------
# Home Route
# -------------------------------

@app.get("/")
def home():
    return FileResponse(FRONTEND_FILE)


# -------------------------------
# Frontend Route
# -------------------------------

@app.get("/app")
def frontend():
    return FileResponse(FRONTEND_FILE)


# -------------------------------
# Health Check
# -------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# -------------------------------
# Chat API
# -------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    safety = check_request_safety(request.message)

    if not safety["allowed"]:
        return {
            "user_message": request.message,
            "type": "blocked",
            "response": (
                "I can't perform that request because it may "
                "damage your computer or project files."
            ),
            "sources": []
        }

    result = route_query(
        request.message,
        request.session_id
    )

    return {
        "user_message": request.message,
        "type": result["type"],
        "response": result["response"],
        "sources": result.get("sources", [])
    }
