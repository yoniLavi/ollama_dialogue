#!/usr/bin/env python
import ollama

MODEL = "llama3.2:3b"
SYSTEM_PROMPT_TEMPLATE = (
    "You are {name}, a screenplay character who's: {description}. "
    "Reply with only the words spoken, without any parentheticals."
)
ROUNDS = 5


class Character:
    def __init__(self, name: str, description: str):
        self.name = name
        system_message = SYSTEM_PROMPT_TEMPLATE.format(
            name=name, description=description
        )
        self.messages = [{"role": "system", "content": system_message}]

    def add_message(self, message: str, role: str = "user"):
        self.messages.append({"role": role, "content": message})

    def speak_line(self, line):
        print(f"{' '*5}{self.name}:\n{line}\n")


def ollama_response(messages: list[dict[str, str]]) -> str:
    return ollama.chat(model=MODEL, messages=messages)["message"]["content"]  # type: ignore


def generate_dialogue(rounds: int):
    james = Character("James", "a logical and pragmatic software engineer, Emma's husband",)
    emma = Character("Emma", "a passionate and emotional artist, James's wife")

    emma_first_line = "Hi honey, seems that we're both free tonight, what would you like to do?"
    emma.speak_line(emma_first_line)
    emma.add_message(emma_first_line, role="assistant")
    james.add_message(emma_first_line, role="user")

    for _ in range(rounds):
        reply_from_james = ollama_response(james.messages)
        james.speak_line(reply_from_james)
        james.add_message(reply_from_james, role="assistant")
        emma.add_message(reply_from_james, role="user")

        reply_from_emma = ollama_response(emma.messages)
        emma.speak_line(reply_from_emma)
        emma.add_message(reply_from_emma, role="assistant")
        james.add_message(reply_from_emma, role="user")


if __name__ == "__main__":
    print(f"Generating a {ROUNDS} rounds dialogue between Emma and James...\n")
    generate_dialogue(ROUNDS)
    print("Dialogue generation complete.")
