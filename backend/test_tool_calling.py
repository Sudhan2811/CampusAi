from backend.bedrock import ask_bedrock


questions = [
    "Calculate 25 * 18",
    "What is 1250 / 25?",
    "What is an LLM?"
]


for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION:", question)

    response = ask_bedrock(question)

    print("ANSWER:", response)