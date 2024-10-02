#!/usr/bin/env python
from __future__ import annotations
import ollama
from typing import List, Tuple

MODEL = "llama3.2:3b"
SYSTEM_PROMPT_TEMPLATE = (
    "You are {name}, a screenplay character who's: {description}. "
    "Reply with only the words spoken, without any parentheticals."
)

class Character:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def speak_line(self, line: str):
        print(f"{' '*5}{self.name}:\n{line}\n")

    def take_turn(self, dialogue_lines: List[Tuple['Character', str]]) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(
            name=self.name, description=self.description
        )}]

        for speaker, line in dialogue_lines:
            role = "assistant" if speaker == self else "user"
            messages.append({"role": role, "content": line})

        response = ollama.chat(model=MODEL, messages=messages)
        return response["message"]["content"]

class Dialogue:
    def __init__(self, character1: Character, character2: Character):
        self.character1 = character1
        self.character2 = character2
        self.lines: List[Tuple[Character, str]] = []
        self.current_speaker = self.character1

    def say_line(self, line: str):
        self.current_speaker.speak_line(line)
        self.lines.append((self.current_speaker, line))
        self.current_speaker = self.character2 if self.current_speaker == self.character1 else self.character1

    def generate(self, rounds: int):
        for _ in range(rounds):
            reply = self.current_speaker.take_turn(self.lines)
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
