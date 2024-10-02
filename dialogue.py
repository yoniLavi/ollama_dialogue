#!/usr/bin/env python
import ollama
from itertools import cycle

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
        self.speaker_cycle = cycle(self.characters)
        self.current_speaker = next(self.speaker_cycle)

    def say_line(self, character: Character, line: str):
        character.speak_line(line)
        self.lines.append((character, line))
        self.current_speaker = next(self.speaker_cycle)

    def generate(self, rounds: int):
        for _ in range(rounds):
            reply = self.current_speaker.take_turn(self.lines)
            self.say_line(self.current_speaker, reply)


if __name__ == "__main__":
    emma = Character("Emma", "a passionate and emotional artist, James's wife")
    james = Character(
        "James", "a logical and pragmatic software engineer, Emma's husband"
    )

    print(f"Generating a dialogue between Emma and James...\n")
    dialogue = Dialogue(emma, james)
    dialogue.say_line(emma, "Hi honey, seems that we're both free tonight, what would you like to do?")
    dialogue.generate(2)  # Generate 2 rounds
    dialogue.say_line(emma, "Actually, I just remembered we have tickets for a concert tonight!")
    dialogue.generate(2)  # Generate 2 more rounds
    print("Dialogue generation complete.")
