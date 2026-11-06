"""
Configuration for the AI Assistant.

Edit these values to match your system.
"""

from pathlib import Path

# -----------------------------------------------------
# llama.cpp Server
# -----------------------------------------------------

LLAMA_SERVER = "http://127.0.0.1:8080/v1/chat/completions"

MODEL_NAME = "qwen3"

REQUEST_TIMEOUT = 300

TEMPERATURE = 0.2

MAX_TOKENS = 2048

# -----------------------------------------------------
# Allowed folders
# The assistant will NEVER read outside these folders.
# -----------------------------------------------------

ALLOWED_PATHS = [

    Path.home() / "Notes",

    Path.home() / "assistant/prompts"

]

# -----------------------------------------------------
# Search
# -----------------------------------------------------

MAX_SEARCH_RESULTS = 5

MAX_FILE_SIZE = 2 * 1024 * 1024      # 2 MB

MAX_PAGE_CHARS = 15000

# -----------------------------------------------------
# Conversation
# -----------------------------------------------------

MAX_HISTORY = 20

# -----------------------------------------------------
# Logging
# -----------------------------------------------------

LOG_LEVEL = "INFO"
