"""
agent.py

The tool-calling agent loop.

Responsibilities:
- Send messages to Qwen
- Detect tool calls
- Execute Python tools
- Return tool results to Qwen
- Repeat until Qwen provides a final answer
"""

from __future__ import annotations

import json

from llm import LLM
from registry import registry


MAX_TOOL_ROUNDS = 8


class Agent:

    def __init__(self, system_prompt=None):

        self.llm = LLM()

        if system_prompt is None:
            prompt_file = Path("prompts/system.txt")
            

        if system_prompt:
            self.llm.add_system(system_prompt)

    # ---------------------------------------------------------
    # Main chat loop
    # ---------------------------------------------------------

    def chat(self, message: str):

        self.llm.add_user(message)

        tool_round = 0

        while tool_round < MAX_TOOL_ROUNDS:

            tool_round += 1

            response = self.llm.complete(
                tools=registry.openai_tools()
            )

            self.llm.save_assistant_message(response)

            # -----------------------------------------
            # Model answered normally
            # -----------------------------------------

            tool_calls = response.get("tool_calls")

            if not tool_calls:

                return response.get(
                    "content",
                    ""
                )

            # -----------------------------------------
            # Execute every requested tool
            # -----------------------------------------

            for call in tool_calls:

                tool_name = call["function"]["name"]

                arguments = json.loads(
                    call["function"]["arguments"]
                )

                print(f"\n[Tool {tool_round}] {tool_name}")
                print(arguments)

                try:

                    result = registry.execute(
                        tool_name,
                        arguments
                    )

                except Exception as e:

                    result = f"Tool error: {e}"

                print("\n[Result]")
                print(result)

                self.llm.add_tool(
                    call["id"],
                    tool_name,
                    str(result)
                )

            #
            # Give the model a small hint after every tool round.
            #
            self.llm.add_user(
                "If the tool results are sufficient, answer the user now. "
                "Only call another tool if more information is truly needed."
            )

        # -------------------------------------------------
        # Safety stop
        # -------------------------------------------------

        return (
            "I stopped after reaching the maximum number "
            "of tool calls. The model may be stuck in a loop."
        )
