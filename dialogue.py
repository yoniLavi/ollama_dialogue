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


class Dialogue:
    def __init__(self, character1: Character, character2: Character):
        self.character1 = character1
        self.character2 = character2

    def generate(self, rounds: int):
        first_line = "Hi honey, seems that we're both free tonight, what would you like to do?"
        self.character1.speak_line(first_line)
        self.character1.add_message(first_line, role="assistant")
        self.character2.add_message(first_line, role="user")

        for _ in range(rounds):
            self._generate_round(self.character2, self.character1)
            self._generate_round(self.character1, self.character2)

    def _generate_round(self, speaker: Character, listener: Character):
        reply = ollama_response(speaker.messages)
        speaker.speak_line(reply)
        speaker.add_message(reply, role="assistant")
        listener.add_message(reply, role="user")


if __name__ == "__main__":
    james = Character("James", "a logical and pragmatic software engineer, Emma's husband")
    emma = Character("Emma", "a passionate and emotional artist, James's wife")
    
    print(f"Generating a {ROUNDS} rounds dialogue between Emma and James...\n")
    dialogue = Dialogue(emma, james)
    dialogue.generate(ROUNDS)
    print("Dialogue generation complete.")
