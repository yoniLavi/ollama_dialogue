import ollama

ROUNDS = 5

def ollama_response(messages, model):
    return ollama.chat(model=model, messages=messages)['message']['content']


def generate_dialogue(rounds, model='llama3.2:3b'):
    emma_messages = [
        {'role': 'system', 'content': "You are Emma, a screenplay character who's a passionate and emotional artist. Reply in brief sentences, and add parentheticals as appropriate."},
        {'role': 'user', 'content': 'James, how could you forget our anniversary?!'}
    ]

    james_messages = [
        {'role': 'system', 'content': "You are James, a screenplay character who's a logical and pragmatic software engineer. You speak calmly and rationally. You forgot your anniversary with Emma and are trying to explain yourself. Reply in brief sentences, and add parentheticals as appropriate."}
    ]

    for _ in range(rounds):
        reply_from_james = ollama_response(model, emma_messages)
        james_messages.append({'role': 'user', 'content': reply_from_james})
        emma_messages.append({'role': 'assistant', 'content': reply_from_james})
        print("Emma:", reply_from_james)

        reply_from_emma = ollama_response(model, james_messages)
        emma_messages.append({'role': 'user', 'content': reply_from_emma})
        james_messages.append({'role': 'assistant', 'content': reply_from_emma})
        print("James:", reply_from_emma)


if __name__ == "__main__":
    print(f"Generating a {ROUNDS} rounds dialogue between Emma and James...")
    generate_dialogue(ROUNDS)
    print("Dialogue generation complete.")
