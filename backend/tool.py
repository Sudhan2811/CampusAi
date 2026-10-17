from tools.calculator import calculate
from tools.vscode import open_vscode
from tools.websites import open_website
from tools.datetime_tool import get_datetime
from tools.weather import get_weather,get_weather_forecast
from tools.music import play_music


# =========================
# Calculator Tool
# =========================

CALCULATOR_TOOL = {
    "toolSpec": {
        "name": "calculator",
        "description": (
            "Perform mathematical calculations using a mathematical expression."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate."
                    }
                },
                "required": ["expression"]
            }
        }
    }
}


# =========================
# VS Code Tool
# =========================

VSCODE_TOOL = {
    "toolSpec": {
        "name": "open_vscode",
        "description": (
            "Open Visual Studio Code on the user's computer and open the "
            "CampusAI project folder. Use this tool when the user asks to "
            "open VS Code, open their CampusAI project, open the mybot "
            "project, or launch the CampusAI project in VS Code. "
            "This is a safe, non-destructive action."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {}
            }
        }
    }
}


WEBSITE_TOOL = {
    "toolSpec": {
        "name": "open_website",
        "description": (
            "Open an approved website in the default browser. "
            "Use this tool when the user asks to open Google, YouTube, "
            "GitHub, or ChatGPT."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": ["google", "youtube", "github", "chatgpt"],
                        "description": "The approved website to open."
                    }
                },
                "required": ["name"]
            }
        }
    }
}


DATETIME_TOOL = {
    "toolSpec": {
        "name": "get_datetime",
        "description": (
            "Get the current date, day of the week, and time in India "
            "Standard Time. Use this tool whenever the user asks what "
            "time it is, today's date, or the current day."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {}
            }
        }
    }
}

WEATHER_TOOL = {
    "toolSpec": {
        "name": "get_weather",
        "description": (
            "Get current weather information for any city or location "
            "in the world. Use this when the user asks about weather, "
            "temperature, humidity, wind, or current conditions."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City or location, optionally including its country."
                    }
                },
                "required": ["location"]
            }
        }
    }
}


MUSIC_TOOL = {
    "toolSpec": {
        "name": "play_music",
        "description": (
            "Search for and open music on YouTube by default. "
            "Use Spotify only when the user explicitly requests Spotify. "
            "Supports any song title, artist, genre, or music style. "
            "For commands such as 'play another song', use a suitable "
            "new search query. This tool opens search results; it does "
            "not guarantee automatic playback."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "Song title, artist, genre, or music style. "
                            "For a random song, provide a suitable query "
                            "such as popular Hindi songs."
                        )
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["youtube", "spotify"],
                        "description": (
                            "Use youtube by default. Choose spotify "
                            "only when the user explicitly requests it."
                        )
                    }
                },
                "required": ["query", "platform"]
            }
        }
    }
}


FORECAST_TOOL = {
    "toolSpec": {
        "name": "get_weather_forecast",
        "description": (
            "Get a 7-day weather forecast for a city or location, "
            "including daily high and low temperatures, weather "
            "conditions, and precipitation probability. Use this "
            "when the user asks about tomorrow's weather, upcoming "
            "days, or the weekly forecast."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City or location to forecast"
                    }
                },
                "required": ["location"]
            }
        }
    }
}



# =========================
# Tool Configuration
# =========================

def get_tool_config():
    return {
        "tools": [
            CALCULATOR_TOOL,
            VSCODE_TOOL,
            WEBSITE_TOOL,
            DATETIME_TOOL,
            WEATHER_TOOL,
            MUSIC_TOOL,
            FORECAST_TOOL
        ]
    }


# =========================
# Tool Execution
# =========================



def execute_tool(tool_name, tool_input):
    if tool_name == "calculator":
        return calculate(tool_input.get("expression", ""))

    if tool_name == "open_vscode":
        return open_vscode()

    if tool_name == "open_website":
        return open_website(tool_input.get("name", ""))

    if tool_name == "get_datetime":
        return get_datetime()

    if tool_name == "get_weather":
        return get_weather(tool_input.get("location", ""))

    if tool_name == "get_weather_forecast":
     return get_weather_forecast(
        tool_input.get("location", "")
    )

    if tool_name == "play_music":
        query = tool_input.get("query", "")
        platform = tool_input.get("platform", "youtube")
        return play_music(query, platform)

    return {
        "success": False,
        "error": f"Unknown tool: {tool_name}"
    }
