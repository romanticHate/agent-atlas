"""
File system tools.

These tools allow the AI assistant to:
- browse directories
- find files
- search file contents
- read files

Access is restricted by config.ALLOWED_PATHS.
"""

from pathlib import Path

from registry import tool

from config import (
    ALLOWED_PATHS,
    MAX_FILE_SIZE,
)


# ----------------------------------------------------
# Security
# ----------------------------------------------------

def is_allowed(path: Path):

    path = path.resolve()

    for allowed in ALLOWED_PATHS:

        try:

            allowed = allowed.resolve()

            path.relative_to(
                allowed
            )

            return True

        except ValueError:

            continue


    return False



def safe_path(path):

    p = Path(path).expanduser()

    if not is_allowed(p):

        raise PermissionError(
            f"Access denied: {p}"
        )

    return p.resolve()

# ----------------------------------------------------
#  Allow locations
# ----------------------------------------------------
@tool(
    description=
    "Show the folders that the assistant is allowed to access."
)
def get_allowed_locations():

    locations = []

    for path in ALLOWED_PATHS:

        locations.append(
            str(path)
        )

    return "\n".join(locations)

# ----------------------------------------------------
# List directory
# ----------------------------------------------------

@tool(
    description=
    "List files and folders inside a directory."
)
def list_directory(path: str):

    folder = safe_path(path)

    if not folder.exists():

        return "Directory does not exist."


    results = []


    for item in folder.iterdir():

        if item.is_dir():

            results.append(
                f"[DIR]  {item.name}"
            )

        else:

            results.append(
                f"[FILE] {item.name}"
            )


    return "\n".join(results)



# ----------------------------------------------------
# Find files
# ----------------------------------------------------

@tool(
    description=
    "Find files by name pattern. "
    "Example: *.pdf or *.md"
)
def find_files(
    path: str,
    pattern: str
):

    folder = safe_path(path)


    results = []


    for file in folder.rglob(pattern):

        if is_allowed(file):

            results.append(
                str(file)
            )


    if not results:

        return "No files found."


    return "\n".join(results)



# ----------------------------------------------------
# Search file contents
# ----------------------------------------------------

@tool(
    description="Find files related to the user's request."
)
def find_relevant_files(query: str):

    query_words = [
        w.lower()
        for w in query.split()
        if len(w) > 2
    ]

    matches = []

    for root in ALLOWED_PATHS:

        if not root.exists():
            continue

        for file in root.rglob("*"):

            if not file.is_file():
                continue

            if file.stat().st_size > MAX_FILE_SIZE:
                continue

            try:

                text = file.read_text(
                    errors="ignore"
                )

            except Exception:

                continue

            score = 0

            lower = text.lower()

            for word in query_words:

                score += lower.count(word)

                score += file.name.lower().count(word) * 5

            if score:

                matches.append(

                    (
                        score,
                        file

                    )

                )

    matches.sort(
        reverse=True
    )

    if not matches:

        return "No relevant files found."

    result = []

    for score, file in matches[:5]:

        result.append(

            f"{file} (score={score})"

        )

    return "\n".join(result)



# ----------------------------------------------------
# Read file
# ----------------------------------------------------

@tool(
    description=
    "Read the contents of a text file."
)
def read_file(path: str):

    file = safe_path(path)


    if not file.exists():

        return "File does not exist."


    if file.stat().st_size > MAX_FILE_SIZE:

        return (
            "File is too large to read directly."
        )


    try:

        return file.read_text(
            errors="ignore"
        )


    except Exception as e:

        return (
            f"Unable to read file: {e}"
        )
