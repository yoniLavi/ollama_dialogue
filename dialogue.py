#!/usr/bin/env python
import ollama

MODEL = "llama3.2:3b"
ROUNDS = 5


class Character:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.messages = [
            {"role": "system", "content": system_prompt},
        ]

    def add_message(self, message: str, role: str = "user"):
        self.messages.append({"role": role, "content": message})


def ollama_response(messages: list[dict[str, str]]) -> str:
    return ollama.chat(model=MODEL, messages=messages)["message"]["content"]


def print_character_line(character: str, line: str):
    print(f"{' '*5}{character}:\n{line}\n")


def generate_dialogue(
    rounds: int, emma_first_line: str = "James, how could you forget our anniversary?!"
):
    emma = Character(
        "Emma",
        "You are Emma, a screenplay character who's a passionate and emotional artist. Reply with only the words spoken, without any parentheticals.",
    )
    james = Character(
        "James",
        "You are James, a screenplay character who's a logical and pragmatic software engineer. You speak calmly and rationally. You forgot your anniversary with Emma and are trying to explain yourself. Reply with only the words spoken, without any parentheticals.",
    )

    emma.add_message(emma_first_line)
    print_character_line(emma.name, emma_first_line)

    for _ in range(rounds):
        reply_from_james = ollama_response(emma.messages)
        james.add_message(reply_from_james)
        emma.add_message(reply_from_james, role="assistant")
        print_character_line(james.name, reply_from_james)

        reply_from_emma = ollama_response(james.messages)
        emma.add_message(reply_from_emma)
        james.add_message(reply_from_emma, role="assistant")
        print_character_line(emma.name, reply_from_emma)


if __name__ == "__main__":
    print(f"Generating a {ROUNDS} rounds dialogue between Emma and James...\n")
    generate_dialogue(ROUNDS)
    print("Dialogue generation complete.")
