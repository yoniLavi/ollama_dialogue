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

    def take_turn(self, previous_line: str) -> str:
        self.messages.append({"role": "user", "content": previous_line})
        response = ollama_response(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        self.speak_line(response)
        return response

    def speak_line(self, line: str):
        print(f"{' '*5}{self.name}:\n{line}\n")


def ollama_response(messages: list[dict[str, str]]) -> str:
    return ollama.chat(model=MODEL, messages=messages)["message"]["content"]  # type: ignore


class Dialogue:
    def __init__(self, character1: Character, character2: Character):
        self.character1 = character1
        self.character2 = character2

    def generate(self, rounds: int):
        first_line = "Hi honey, seems that we're both free tonight, what would you like to do?"
        self.character1.speak_line(first_line)
        current_line = first_line

        for _ in range(rounds):
            current_line = self.character2.take_turn(current_line)
            current_line = self.character1.take_turn(current_line)


if __name__ == "__main__":
    emma = Character("Emma", "a passionate and emotional artist, James's wife")
    james = Character("James", "a logical and pragmatic software engineer, Emma's husband")
    
    print(f"Generating a {ROUNDS} rounds dialogue between Emma and James...\n")
    dialogue = Dialogue(emma, james)
    dialogue.generate(ROUNDS)
    print("Dialogue generation complete.")
