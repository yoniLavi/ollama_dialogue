#!/usr/bin/env python
from itertools import cycle, islice

import ollama

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

    def take_turn(self, dialogue_lines: list[tuple["Character", str]]) -> str:
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(name=self.name, description=self.description)
        messages: list[ollama.Message] = [{"role": "system", "content": system_prompt}]

        for speaker, line in dialogue_lines:
            role = "assistant" if speaker is self else "user"
            messages.append({"role": role, "content": line})

        reply = ollama.chat(MODEL, messages)["message"]["content"]
        self.speak_line(reply)
        return reply


class Dialogue:
    def __init__(self, *characters: Character):
        self.characters = list(characters)
        self.lines: list[tuple[Character, str]] = []

    def add_line(self, character: Character, line: str):
        character.speak_line(line)
        self.lines.append((character, line))

    def generate(self, rounds: int, starting_with: Character | None = None):
        speaker_cycle = cycle(self.characters)
        while starting_with and next(speaker_cycle) != starting_with:
            continue  # Align the speaker_cycle with the starting character

        for current_speaker in islice(speaker_cycle, rounds):
            reply = current_speaker.take_turn(self.lines)
            self.lines.append((current_speaker, reply))


if __name__ == "__main__":
    emma = Character("Emma", "a passionate and emotional artist, James's wife")
    james = Character("James", "a logical and pragmatic software engineer, Emma's husband")
    alex = Character("Alex", "Emma and James's witty and sarcastic friend")

    print(f"Generating a dialogue between Emma, James, and Alex...\n")
    dialogue = Dialogue(emma, james, alex)
    dialogue.add_line(emma, "Seems that we're all free tonight, should we go out?")
    dialogue.generate(rounds=3, starting_with=james)
    dialogue.add_line(alex, "Actually, I just remembered we have tickets for a concert tonight!")
    dialogue.generate(rounds=5)
    print("Dialogue generation complete.")
