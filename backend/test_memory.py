from backend.bedrock import ask_bedrock


history = [
    {
        "role": "user",
        "message": "My name is Sudhanshu."
    },
    {
        "role": "assistant",
        "message": "Nice to meet you, Sudhanshu!"
    }
]


response = ask_bedrock(
    "What is my name?",
    history=history
)

print("Response:")
print(response)