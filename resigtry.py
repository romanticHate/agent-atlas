"""
Tool Registry

Every tool is automatically registered using the @tool decorator.

The registry also generates the OpenAI tool schema
used by llama.cpp.
"""

from __future__ import annotations

import inspect
from typing import get_type_hints


class ToolRegistry:

    def __init__(self):

        self.tools = {}

    # --------------------------------------------

    def register(self, fn, description):

        name = fn.__name__

        self.tools[name] = {

            "function": fn,

            "description": description,

            "schema": self.build_schema(fn, description)

        }

        return fn

    # --------------------------------------------

    def build_schema(self, fn, description):

        signature = inspect.signature(fn)

        hints = get_type_hints(fn)

        properties = {}

        required = []

        for parameter in signature.parameters.values():

            ptype = hints.get(parameter.name, str)

            if ptype == int:

                t = "integer"

            elif ptype == float:

                t = "number"

            elif ptype == bool:

                t = "boolean"

            else:

                t = "string"

            properties[parameter.name] = {

                "type": t

            }

            if parameter.default is inspect.Parameter.empty:

                required.append(parameter.name)

        return {

            "type": "function",

            "function": {

                "name": fn.__name__,

                "description": description,

                "parameters": {

                    "type": "object",

                    "properties": properties,

                    "required": required

                }

            }

        }

    # --------------------------------------------

    def execute(self, name, arguments):

        if name not in self.tools:

            raise Exception(f"Unknown tool: {name}")

        fn = self.tools[name]["function"]

        return fn(**arguments)

    # --------------------------------------------

    def openai_tools(self):

        return [

            tool["schema"]

            for tool in self.tools.values()

        ]


registry = ToolRegistry()


def tool(description=""):

    def decorator(fn):

        registry.register(fn, description)

        return fn

    return decorator
