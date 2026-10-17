from backend.bedrock import ask_bedrock


questions = [
    "What's the weather in Tokyo, Japan?",
    "Tell me the current weather in New York, USA.",
    "What's the weather in Paris, France?"
]


for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION:", question)

    response = ask_bedrock(question)

    print("ANSWER:", response)