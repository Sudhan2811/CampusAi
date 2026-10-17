from backend.router import route_query


questions = [
    "Calculate 25 * 18",
    "What is 100 / 4",
    "Solve 50 + 25",
    "What is an LLM?"
]


for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION:", question)

    result = route_query(question)

    print("TYPE:", result["type"])
    print("RESPONSE:", result["response"])