def calculate(expression: str):
    try:
        result = eval(expression, {"__builtins__": {}}, {})

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }