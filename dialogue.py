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
        self.description = description

    def speak_line(self, line: str):
        print(f"{' '*5}{self.name}:\n{line}\n")


class Dialogue:
    def __init__(self, character1: Character, character2: Character):
        self.character1 = character1
        self.character2 = character2
        self.messages = []
        self.current_speaker = self.character1

    def say_line(self, line: str):
        self.current_speaker.speak_line(line)
        self.messages.append({"role": "assistant", "content": line})
        self.current_speaker = self.character2 if self.current_speaker == self.character1 else self.character1

    def generate(self, rounds: int):
        for _ in range(rounds):
            system_message = SYSTEM_PROMPT_TEMPLATE.format(
                name=self.current_speaker.name, 
                description=self.current_speaker.description
            )
            messages = [{"role": "system", "content": system_message}] + self.messages
            reply = ollama_response(messages)
            self.say_line(reply)

    def start_dialogue(self, first_line: str):
        self.say_line(first_line)


if __name__ == "__main__":
    emma = Character("Emma", "a passionate and emotional artist, James's wife")
    james = Character("James", "a logical and pragmatic software engineer, Emma's husband")

    print(f"Generating a dialogue between Emma and James...\n")
    dialogue = Dialogue(emma, james)
    dialogue.start_dialogue("Hi honey, seems that we're both free tonight, what would you like to do?")
    dialogue.generate(2)  # Generate 2 rounds
    dialogue.say_line("Actually, I just remembered we have tickets for a concert tonight!")
    dialogue.generate(2)  # Generate 2 more rounds
    print("Dialogue generation complete.")
