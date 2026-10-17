import boto3

from backend.config import AWS_REGION, AWS_MODEL_ID
from backend.tool import get_tool_config, execute_tool


def get_bedrock_client():
    return boto3.client(
        "bedrock-runtime",
        region_name=AWS_REGION
    )


def ask_bedrock(prompt: str, history=None):

    client = get_bedrock_client()

    messages = []

    # Add previous conversation
    if history:
        for item in history:
            messages.append(
                {
                    "role": item["role"],
                    "content": [
                        {
                            "text": item["message"]
                        }
                    ]
                }
            )

    # Add current user message
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "text": prompt
                }
            ]
        }
    )

    response = client.converse(
        modelId=AWS_MODEL_ID,
        messages=messages,
        toolConfig=get_tool_config()
    )

    output_message = response["output"]["message"]

    # Check whether Nova requested a tool
    tool_uses = [
        content
        for content in output_message["content"]
        if "toolUse" in content
    ]

    # No tool required
    if not tool_uses:
        return output_message["content"][0]["text"]

    # Add Nova's tool request
    messages.append(output_message)

    tool_results = []

    for tool_use_content in tool_uses:

        tool_use = tool_use_content["toolUse"]

        tool_name = tool_use["name"]
        tool_input = tool_use["input"]
        tool_use_id = tool_use["toolUseId"]

        print(f"Tool requested: {tool_name}")
        print(f"Tool input: {tool_input}")

    result = execute_tool(
           tool_name,
        tool_input
     )

    print(f"Tool result: {result}")

    tool_results.append(
            {
                "toolResult": {
                    "toolUseId": tool_use_id,
                    "content": [
                        {
                            "json": result
                        }
                    ]
                }
            }
        )

    # Send tool result back to Nova
    messages.append(
        {
            "role": "user",
            "content": tool_results
        }
    )

    final_response = client.converse(
        modelId=AWS_MODEL_ID,
        messages=messages,
        toolConfig=get_tool_config()
    )

    return final_response["output"]["message"]["content"][0]["text"]