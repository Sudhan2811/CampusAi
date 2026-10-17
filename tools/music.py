
import webbrowser
from urllib.parse import quote_plus


def play_music(query: str, platform: str = "youtube"):
    query = query.strip() or "popular music"
    platform = platform.strip().lower()

    if platform == "youtube":
        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(query)
        )

    elif platform == "spotify":
        url = (
            "https://open.spotify.com/search/"
            + quote_plus(query)
        )

    else:
        return {
            "success": False,
            "message": "Unsupported music platform."
        }

    try:
        webbrowser.open(url, new=2)

        return {
            "success": True,
            "platform": platform,
            "query": query,
            "message": (
                f"Opened {platform} for {query}. "
                "Select the song to start playback."
            )
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
