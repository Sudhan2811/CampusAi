from fastapi import FastAPI
from pydantic import BaseModel
from backend.safety import check_request_safety


from backend.router import route_query
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="CampusAI",
    description="AWS-powered Generative AI Voice Assistant",
    version="1.0.0"
)

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


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


@app.get("/")
def home():
    return {
        "message": "CampusAI is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }



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
