#!/usr/bin/env python
import ollama

MODEL = "llama3.2:3b"
ROUNDS = 5


class Character:
    SYSTEM_PROMPT_TEMPLATE = "You are {name}, a screenplay character who's {description}. Reply with only the words spoken, without any parentheticals."

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.messages = [
            {"role": "system", "content": self.generate_system_prompt()},
        ]

    def generate_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT_TEMPLATE.format(name=self.name, description=self.description)

    def add_message(self, message: str, role: str = "user"):
        self.messages.append({"role": role, "content": message})

    def print_line(self, line: str):
        print(f"{' '*5}{self.name}:\n{line}\n")


def ollama_response(messages: list[dict[str, str]]) -> str:
    return ollama.chat(model=MODEL, messages=messages)["message"]["content"]


def generate_dialogue(
    rounds: int, emma_first_line: str = "James, how could you forget our anniversary?!"
):
    emma = Character("Emma", "a passionate and emotional artist")
    james = Character(
        "James",
        "a logical and pragmatic software engineer. You speak calmly and rationally. You forgot your anniversary with Emma and are trying to explain yourself"
    )

    emma.add_message(emma_first_line)
    emma.print_line(emma_first_line)

    for _ in range(rounds):
        reply_from_james = ollama_response(emma.messages)
        james.add_message(reply_from_james)
        emma.add_message(reply_from_james, role="assistant")
        james.print_line(reply_from_james)

        reply_from_emma = ollama_response(james.messages)
        emma.add_message(reply_from_emma)
        james.add_message(reply_from_emma, role="assistant")
        emma.print_line(reply_from_emma)


if __name__ == "__main__":
    print(f"Generating a {ROUNDS} rounds dialogue between Emma and James...\n")
    generate_dialogue(ROUNDS)
    print("Dialogue generation complete.")
