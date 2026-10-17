
import re


BLOCKED_PATTERNS = [
    # Destructive disk and filesystem operations
    r"\bformat\s+(?:[a-z]:|drive|disk|hard\s*drive)\b",
    r"\b(?:wipe|erase)\s+(?:my\s+)?(?:drive|disk|hard\s*drive)\b",
    r"\b(?:delete|remove|erase)\s+(?:all\s+)?(?:my\s+)?files\b",
    r"\bdelete\s+(?:the\s+)?(?:entire\s+)?project\b",
    r"\b(?:delete|remove|wipe)\s+(?:the\s+)?campusai\b",
    r"\brmdir\s+/s\b",
    r"\bdel\s+/[fq]\b",
    r"\b(?:shutdown|restart|reboot)\s+(?:my\s+)?(?:pc|computer|laptop|system|windows)\b",
    r"\bpoweroff\b",
]


def check_request_safety(message: str) -> dict:
    """
    First-layer check for explicitly destructive natural-language requests.
    This is not a complete security boundary.
    """
    if not isinstance(message, str) or not message.strip():
        return {
            "allowed": False,
            "reason": "Empty or invalid request."
        }

    normalized = message.strip().lower()

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, normalized):
            return {
                "allowed": False,
                "reason": (
                    "This request was blocked by CampusAI's safety "
                    "guard because it may cause destructive changes."
                )
            }

    return {
        "allowed": True,
        "reason": "No blocked pattern detected."
    }
