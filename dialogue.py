#!/usr/bin/env python
import ollama

MODEL = "llama3.2:3b"
ROUNDS = 5


def ollama_response(messages):
    return ollama.chat(model=MODEL, messages=messages)["message"]["content"]


def print_character_line(character, line):
    print(f"{' '*5}{character}:\n{line}\n")


def generate_dialogue(
    rounds, emma_first_line="James, how could you forget our anniversary?!"
):
    emma_messages = [
        {
            "role": "system",
            "content": "You are Emma, a screenplay character who's a passionate and emotional artist. Reply with only the words spoken, without any parentheticals.",
        },
        {"role": "user", "content": emma_first_line},
    ]
    print_character_line("Emma", emma_first_line)

    james_messages = [
        {
            "role": "system",
            "content": "You are James, a screenplay character who's a logical and pragmatic software engineer. You speak calmly and rationally. You forgot your anniversary with Emma and are trying to explain yourself. Reply with only the words spoken, without any parentheticals.",
        }
    ]

    for _ in range(rounds):
        reply_from_james = ollama_response(emma_messages)
        james_messages.append({"role": "user", "content": reply_from_james})
        emma_messages.append({"role": "assistant", "content": reply_from_james})
        print_character_line("James", reply_from_james)

        reply_from_emma = ollama_response(james_messages)
        emma_messages.append({"role": "user", "content": reply_from_emma})
        james_messages.append({"role": "assistant", "content": reply_from_emma})
        print_character_line("Emma", reply_from_emma)


if __name__ == "__main__":
    print(f"Generating a {ROUNDS} rounds dialogue between Emma and James...\n")
    generate_dialogue(ROUNDS)
    print("Dialogue generation complete.")
