import asyncio
import ollama
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_chat(model, messages_tuple):
    messages = list(messages_tuple)
    return ollama.chat(model=model, messages=messages)

async def generate_response(model, messages):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, cached_chat, model, tuple(messages))

async def generate_dialogue(model='llama3.1', rounds=5):
    emma_messages = [
        {'role': 'system', 'content': 'You are Emma, a passionate and emotional artist. You speak poetically and dramatically. You are currently upset with your partner, James, for forgetting your anniversary.'},
        {'role': 'user', 'content': 'James, how could you forget our anniversary? Start the dialogue.'}
    ]
    
    james_messages = [
        {'role': 'system', 'content': 'You are James, a logical and pragmatic software engineer. You speak calmly and rationally. You forgot your anniversary with Emma and are trying to explain yourself.'}
    ]

    for _ in range(rounds):
        # Generate both responses concurrently
        emma_response, james_response = await asyncio.gather(
            generate_response(model, emma_messages),
            generate_response(model, james_messages)
        )

        emma_reply = emma_response['message']['content']
        james_reply = james_response['message']['content']

        print("Emma:", emma_reply)
        print("James:", james_reply)

        emma_messages.extend([
            {'role': 'assistant', 'content': emma_reply},
            {'role': 'user', 'content': james_reply}
        ])
        james_messages.extend([
            {'role': 'user', 'content': emma_reply},
            {'role': 'assistant', 'content': james_reply}
        ])

if __name__ == "__main__":
    print("Generating dialogue between Emma and James...")
    asyncio.run(generate_dialogue())
    print("Dialogue generation complete.")
