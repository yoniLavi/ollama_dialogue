import ollama
import time

def generate_dialogue(model='llama2', rounds=5):
    messages = [
        {'role': 'system', 'content': 'You are Emma, a passionate and emotional artist. You speak poetically and dramatically. You are currently upset with your partner, James, for forgetting your anniversary.'},
        {'role': 'user', 'content': 'James, how could you forget our anniversary? Start the dialogue.'},
    ]

    for _ in range(rounds):
        # Emma's turn
        response = ollama.chat(model=model, messages=messages)
        emma_response = response['message']['content']
        print("Emma:", emma_response)
        messages.append({'role': 'assistant', 'content': emma_response})

        # James's turn
        messages.append({'role': 'system', 'content': 'You are James, a logical and pragmatic software engineer. You speak calmly and rationally. You forgot your anniversary with Emma and are trying to explain yourself.'})
        messages.append({'role': 'user', 'content': 'Respond to Emma\'s last statement.'})
        
        response = ollama.chat(model=model, messages=messages)
        james_response = response['message']['content']
        print("James:", james_response)
        messages.append({'role': 'assistant', 'content': james_response})

        # Reset system message for Emma
        messages.append({'role': 'system', 'content': 'You are Emma, a passionate and emotional artist. You speak poetically and dramatically. You are currently upset with your partner, James, for forgetting your anniversary.'})
        messages.append({'role': 'user', 'content': 'Respond to James\'s last statement.'})

        time.sleep(1)  # To avoid overwhelming the API

if __name__ == "__main__":
    print("Generating dialogue between Emma and James...")
    generate_dialogue()
    print("Dialogue generation complete.")
