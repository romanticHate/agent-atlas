"""
This is for accessing git repositories.

"""

from registry import tool

# ----------------------------------------------------
# Read repository
# ----------------------------------------------------

@tool(
    description=
    "Read the content of a repository from GitHub."
)
def read_repository(path: str):
    return "Repository does not exist."
