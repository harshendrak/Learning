from dotenv import load_dotenv
load_dotenv()
from mem0 import Memory
from google import genai
from google.genai.types import GenerateContentConfig 
import json
import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client()

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {"api_key": GEMINI_API_KEY, "model": "gemini-embedding-001"}
    },
    "llm": {
        "provider": "gemini",
        "config": {"api_key": GEMINI_API_KEY, "model": "gemini-3-flash-preview" }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 768
        }
    }
}

mem_client = Memory.from_config(config)

while True:
    user_query = input(" What would you like to ask?\n>")

    search_memory = mem_client.search(query=user_query, user_id="laddu")

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory.get("results", [])
    ]

    system_prompt = f"""You are a helpful assistant. Here's what you remember about the user:

{json.dumps(memories, indent=2)}

"""
    # response = client.models.generate_content(
    # model="gemini-3-flash-preview",
    # contents=f"{system_prompt}\n\nUser: {user_query}",  # Inject prompt manually
    # # No system_instruction here)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_query,
        config=GenerateContentConfig(         
            system_instruction=system_prompt,
        ),)
    

    ai_response = response.text
    print(f"\n{ai_response}")

    mem_client.add(
        user_id="laddu",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ]
    )

    print("Memory has been saved")