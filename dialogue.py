#!/usr/bin/env python
import ollama

MODEL = "llama3.2:3b"
SYSTEM_PROMPT_TEMPLATE = (
    "You are {name}, a screenplay character who's: {description}. "
    "Reply with only the words spoken, without any parentheticals."
)
ROUNDS = 5


def ollama_response(messages: list[dict[str, str]]) -> str:
    return ollama.chat(model=MODEL, messages=messages)["message"]["content"]  # type: ignore

class Character:
    def __init__(self, name: str, description: str):
        self.name = name
        system_message = SYSTEM_PROMPT_TEMPLATE.format(
            name=name, description=description
        )
        self.messages = [{"role": "system", "content": system_message}]

    def speak_line(self, line: str):
        print(f"{' '*5}{self.name}:\n{line}\n")

    def add_and_speak_line(self, line: str):
        self.messages.append({"role": "assistant", "content": line})
        self.speak_line(line)
        return line

    def take_turn(self, previous_line: str) -> str:
        self.messages.append({"role": "user", "content": previous_line})
        reply = ollama_response(self.messages)
        self.add_and_speak_line(reply)
        return reply


class Dialogue:
    def __init__(self, character1: Character, character2: Character):
        self.character1 = character1
        self.character2 = character2

    def start_dialogue(self, first_line: str):
        return self.character1.add_and_speak_line(first_line)

    def generate(self, rounds: int):
        current_line = self.start_dialogue("Hi honey, seems that we're both free tonight, what would you like to do?")

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
