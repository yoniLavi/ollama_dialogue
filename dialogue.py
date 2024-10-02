#!/usr/bin/env python
import ollama
from itertools import cycle, islice

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
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            name=self.name, description=self.description
        )
        messages: list[ollama.Message] = [{"role": "system", "content": system_prompt}]

        for speaker, line in dialogue_lines:
            role = "assistant" if speaker == self else "user"
            messages.append({"role": role, "content": line})

        return ollama.chat(MODEL, messages)["message"]["content"]


class Dialogue:
    def __init__(self, *characters: Character):
        self.characters = list(characters)
        self.lines: list[tuple[Character, str]] = []

    def generate(self, rounds: int, starting_character: Character):
        speaker_cycle = cycle(self.characters)
        # Align the speaker_cycle with the starting character
        while next(speaker_cycle) != starting_character:
            pass

        for current_speaker in islice(speaker_cycle, rounds):
            reply = current_speaker.take_turn(self.lines)
            current_speaker.speak_line(reply)
            self.lines.append((current_speaker, reply))


if __name__ == "__main__":
    emma = Character("Emma", "a passionate and emotional artist, James's wife")
    james = Character("James", "a logical and pragmatic software engineer, Emma's husband")
    alex = Character("Alex", "Emma and James's witty and sarcastic friend")

    print(f"Generating a dialogue between Emma, James, and Alex...\n")
    dialogue = Dialogue(emma, james, alex)
    emma.speak_line("Hi honey, seems that we're all free tonight, what would you like to do?")
    dialogue.lines.append((emma, "Hi honey, seems that we're all free tonight, what would you like to do?"))
    dialogue.generate(3, james)  # Generate 3 rounds, starting with James
    alex.speak_line("Actually, I just remembered we have tickets for a concert tonight!")
    dialogue.lines.append((alex, "Actually, I just remembered we have tickets for a concert tonight!"))
    dialogue.generate(3, emma)  # Generate 3 more rounds, starting with Emma
    print("Dialogue generation complete.")
