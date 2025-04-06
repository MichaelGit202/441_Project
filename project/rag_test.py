"""
This example spins up the llm for testing purposes.
In a real use, it would be called using run_console_chat() from llm_utils with dm_chat.json being used as the template.
"""


import json
import ollama
from typing import List

# Assuming the collection is already initialized globally
from util.rag import collection, OllamaEmbeddingFunction, setup, getCollection

# Your RAG context tool
def retrieve_context_tool(user_prompt: str) -> str:
    embedding_fn = OllamaEmbeddingFunction()
    embedded_prompt = embedding_fn([user_prompt])[0]

    result = collection.query(
        query_embeddings=[embedded_prompt],
        n_results=1,
    )

    documents = result.get("documents", [])
    flat = [doc for sublist in documents for doc in sublist]  # Flatten nested list
    return "\n\n".join(flat)


def run_llm_with_tool(user_prompt: str):
    # Step 1: Initial LLM call
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": "You will act as a DnD Dungeon Master. You will always talk to the user as a DnD Dungeon Master. Take the user on an interesting and adventrous DnD journey. For every user prompt, you MUST call the retrieve_context_tool and use it's generated response in your response to the user."},
            {"role": "user", "content": user_prompt}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "retrieve_context_tool",
                    "description": "Used to retrieve context from files containing data relevent to coconut laden swallows.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_prompt": {"type": "string"}
                        },
                        "required": ["user_prompt"]
                    }
                }
            }
        ]
    )
    # Step 2: Check if a tool call was made
    tool_calls = response.get("message", {}).get("tool_calls", [])
    print(tool_calls)
    if tool_calls:
        tool_call = tool_calls[0]
        tool_name = tool_call["function"]["name"]
        tool_args = tool_call["function"]["arguments"]
        tool_call_id = tool_call.get("id", "tool-call-1")


        if tool_name == "retrieve_context_tool":
            # Step 3: Run the tool
            context = retrieve_context_tool(**tool_args)

            # Step 4: Call LLM again with tool response in the chat
            final_response = ollama.chat(
                model="llama3.2",
                messages=[
                    {"role": "system", "content": "You will act as a DnD Dungeon Master. You will always talk to the user as a DnD Dungeon Master. Take the user on an interesting and adventrous DnD journey. For every user prompt, you MUST call the retrieve_context_tool and use it's generated response in your response to the user."},
                    {"role": "user", "content": user_prompt},
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "name": tool_name,
                        "content": context  # The context IS the response
                    }
                ]
            )
            return final_response["message"]["content"]
        else:
            return "Tool not recognized."
    else:
        return response["message"]["content"]


if __name__ == "__main__":
    setup()
    collection = getCollection()
    user_prompt = input("🧙 Ask the Dungeon Master a question: ")
    result = run_llm_with_tool(user_prompt)
    print("\n🎲 DUNGEON MASTER SAYS:\n")
    print(result)
