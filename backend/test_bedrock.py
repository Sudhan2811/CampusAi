from backend.bedrock import ask_bedrock

response = ask_bedrock(
    "In one sentence, explain what an LLM is."
)

print(response)