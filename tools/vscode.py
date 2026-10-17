import subprocess

PROJECT_PATH = r"C:\Users\Acer\OneDrive\Desktop\mybot"
VSCODE_PATH = r"C:\Users\Acer\AppData\Local\Programs\Microsoft VS Code\Code.exe"


def open_vscode():
    try:
        subprocess.Popen([
            VSCODE_PATH,
            "--reuse-window",
            PROJECT_PATH
        ])

        return {
            "success": True,
            "message": "CampusAI project opened in VS Code."
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Could not open CampusAI project: {str(e)}"
        }