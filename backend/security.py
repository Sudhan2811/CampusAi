SAFE_ACTIONS = {
    "open_vscode",
}

BLOCKED_ACTIONS = {
    "delete_file",
    "delete_project",
    "delete_vscode_files",
    "format_disk",
    "shutdown",
    "restart",
    "execute_shell_command",
}


def check_permission(action: str) -> str:

    # Explicitly blocked actions
    if action in BLOCKED_ACTIONS:
        return "blocked"

    # Explicitly allowed actions
    if action in SAFE_ACTIONS:
        return "allowed"

    # Anything else is blocked by default
    return "blocked"