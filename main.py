"""
main.py

Command line interface for the local AI assistant.
"""

from pathlib import Path

import tools
from agent import Agent
from registry import registry

print(
    registry.tools.keys()
)

SYSTEM_FILE = Path(
    "prompts/system.txt"
)


def load_system_prompt():

    if SYSTEM_FILE.exists():

        return SYSTEM_FILE.read_text(
            encoding="utf-8"
        )

    return (
        "You are a helpful local AI assistant."
    )



def main():

    print()
    print("==============================")
    print(" Local AI Assistant")
    print(" llama.cpp + Qwen3")
    print("==============================")
    print()

    print(
        "Type 'exit' to quit."
    )

    print()


    agent = Agent(
        load_system_prompt()
    )


    while True:

        try:

            user = input(
                "\nYou: "
            )


        except KeyboardInterrupt:

            print()
            break


        if not user.strip():

            continue


        if user.lower() in (
            "exit",
            "quit",
            "bye"
        ):

            break


        try:

            answer = agent.chat(
                user
            )


            print(
                "\nAssistant:"
            )

            print(
                answer
            )


        except Exception as e:

            print(
                "\nERROR:"
            )

            print(e)



if __name__ == "__main__":

    main()
