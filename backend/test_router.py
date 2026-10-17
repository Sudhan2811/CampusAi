from backend.router import route_query


test_questions = [
    "Who built you?",
    "When does the B.Tech registration start?",
    "When should newly admitted students complete their online form?",
    "What is an LLM?"
]


for question in test_questions:
    print("\n" + "=" * 60)
    print("QUESTION:", question)

    result = route_query(question)

    print("TYPE:", result["type"])
    print("RESPONSE:", result["response"])