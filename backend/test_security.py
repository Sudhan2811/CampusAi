from backend.security import check_permission


actions = [
    "open_vscode",
    "delete_file",
    "delete_project",
    "delete_vscode_files",
    "format_disk",
    "shutdown",
    "restart",
    "execute_shell_command",
    "something_unknown",
]


for action in actions:

    permission = check_permission(action)

    print(
        f"{action:25} -> {permission}"
    )