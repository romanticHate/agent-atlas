"""
Web search-read tool

"""

from registry import tool

# ----------------------------------------------------
# Search web
# ----------------------------------------------------

@tool(
    description=
    "Search for web-pages and read them."
)
def search_web(path: str):
    return "Web result."
