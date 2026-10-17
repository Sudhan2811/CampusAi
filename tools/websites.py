import webbrowser

ALLOWED_WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
}


def open_website(name: str):
    website_name = name.strip().lower()

    if website_name not in ALLOWED_WEBSITES:
        return {
            "success": False,
            "message": "Website is not allowed."
        }

    try:
        opened = webbrowser.open(
            ALLOWED_WEBSITES[website_name],
            new=2
        )

        if opened:
            return {
                "success": True,
                "message": f"Opened {website_name} successfully."
            }

        return {
            "success": False,
            "message": (
                "Could not open the browser. Check your default "
                "browser settings in Windows."
            )
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }