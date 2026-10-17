from backend.creator import get_creator_response
from backend.bedrock import ask_bedrock
from backend.intent import is_rag_question
from backend.memory import get_history, save_message
from rag.rag_pipeline import answer_question


CREATOR_KEYWORDS = [
    "who built you",
    "who created you",
    "who developed you",
    "who made you",
    "who is your creator",
    "who is your developer",
]


def is_creator_question(message: str) -> bool:
    message = message.lower().strip()

    return any(
        keyword in message
        for keyword in CREATOR_KEYWORDS
    )


def route_query(message: str, session_id: str = "default"):

    # Get previous conversation
    history = get_history(session_id)

    # 1. Creator questions
    if is_creator_question(message):

        response = get_creator_response()

        save_message(session_id, "user", message)
        save_message(session_id, "assistant", response)

        return {
            "type": "creator",
            "response": response
        }

    # 2. RAG questions
    if is_rag_question(message):

        result = answer_question(message)

        response = result["answer"]

        save_message(session_id, "user", message)
        save_message(session_id, "assistant", response)

        return {
            "type": "rag",
            "response": response,
            "sources": result["sources"]
        }

    # 3. General LLM questions
    response = ask_bedrock(
        message,
        history=history
    )

    save_message(session_id, "user", message)
    save_message(session_id, "assistant", response)

    return {
        "type": "llm",
        "response": response
    }
