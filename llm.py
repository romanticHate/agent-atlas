"""
llm.py

Handles all communication with llama.cpp (OpenAI compatible API).

Nothing else in the project should make HTTP requests
to the LLM.

Author: AI Valades
"""

from __future__ import annotations

import json
import requests

from config import (
    LLAMA_SERVER,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS,
    REQUEST_TIMEOUT,
)


class LLMError(Exception):
    """Raised when the LLM request fails."""


class LLM:

    def __init__(self):

        self.messages = []

    # ----------------------------------------------------
    # Conversation
    # ----------------------------------------------------

    def add_system(self, text: str):

        self.messages.append({
            "role": "system",
            "content": text
        })

    def add_user(self, text: str):

        self.messages.append({
            "role": "user",
            "content": text
        })

    def add_assistant(self, text: str):

        self.messages.append({
            "role": "assistant",
            "content": text
        })

    def add_tool(self, tool_call_id, tool_name, result):

        self.messages.append({

            "role": "tool",

            "tool_call_id": tool_call_id,

            "name": tool_name,

            "content": result

        })

    # ----------------------------------------------------
    # Send request
    # ----------------------------------------------------

    def complete(self, tools=None):

        payload = {

            "model": MODEL_NAME,

            "messages": self.messages,

            "temperature": TEMPERATURE,

            "max_tokens": MAX_TOKENS

        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        response = requests.post(

            LLAMA_SERVER,

            json=payload,

            timeout=REQUEST_TIMEOUT

        )

        if response.status_code != 200:

            raise LLMError(

                f"Server returned {response.status_code}\n"
                f"{response.text}"

            )

        data = response.json()

        return data["choices"][0]["message"]

    # ----------------------------------------------------
    # Streaming
    # ----------------------------------------------------

    def stream(self, tools=None):

        payload = {

            "model": MODEL_NAME,

            "messages": self.messages,

            "temperature": TEMPERATURE,

            "max_tokens": MAX_TOKENS,

            "stream": True

        }

        if tools:

            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        response = requests.post(

            LLAMA_SERVER,

            json=payload,

            stream=True,

            timeout=REQUEST_TIMEOUT

        )

        if response.status_code != 200:

            raise LLMError(response.text)

        for line in response.iter_lines():

            if not line:

                continue

            line = line.decode()

            if not line.startswith("data: "):
                continue

            line = line[6:]

            if line == "[DONE]":
                break

            chunk = json.loads(line)

            delta = chunk["choices"][0]["delta"]

            yield delta

    # ----------------------------------------------------
    # Utility
    # ----------------------------------------------------

    def reset(self):

        self.messages.clear()

    def save_assistant_message(self, message):

        self.messages.append(message)
