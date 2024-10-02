import ollama

def generate_dialogue(model='llama3.1', rounds=5):
    emma_messages = [
        {'role': 'system', 'content': 'You are Emma, a passionate and emotional artist. You speak poetically and dramatically. You are currently upset with your partner, James, for forgetting your anniversary.'},
        {'role': 'user', 'content': 'James, how could you forget our anniversary? Start the dialogue.'}
    ]
    
    james_messages = [
        {'role': 'system', 'content': 'You are James, a logical and pragmatic software engineer. You speak calmly and rationally. You forgot your anniversary with Emma and are trying to explain yourself.'}
    ]

    for _ in range(rounds):
        # Emma's turn
        emma_response = ollama.chat(model=model, messages=emma_messages)
        emma_reply = emma_response['message']['content']
        print("Emma:", emma_reply)

        # Update James' messages with Emma's reply
        james_messages.append({'role': 'user', 'content': emma_reply})

        # James' turn
        james_response = ollama.chat(model=model, messages=james_messages)
        james_reply = james_response['message']['content']
        print("James:", james_reply)

        # Update Emma's messages with James' reply
        emma_messages.append({'role': 'assistant', 'content': emma_reply})
        emma_messages.append({'role': 'user', 'content': james_reply})

        # Update James' messages with his own reply
        james_messages.append({'role': 'assistant', 'content': james_reply})

if __name__ == "__main__":
    print("Generating dialogue between Emma and James...")
    generate_dialogue()
    print("Dialogue generation complete.")
