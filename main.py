"""Two-Sentence Horror -- make.fun entry.

A horror story of exactly two sentences: a smart speaker whispers a
name at 3 a.m. even though it is unplugged, and when its owner whispers
back, it says it has been waiting for them to notice. This script checks
that the story is exactly two sentences on one line, prints it, and
stores it in /output/entry.txt for the judges to read.

Pure Python 3.13 standard library only; deterministic; no network.
SPDX-License-Identifier: MIT
"""

import os
import re

# The story itself: exactly two sentences, one line.
LINE = (
    "The smart speaker whispered my name at 3 a.m., even though it was unplugged. "
    "I whispered back, and it said it had been waiting for me to notice."
)

MAX_CHARS = 400
OUTPUT_PATH = "/output/entry.txt"
SENTENCE_END = re.compile(r"[.!?](\s|$)")


def count_sentences(line):
    """Count the sentence-ending marks in the line."""
    return len(SENTENCE_END.findall(line))


def validate(line):
    """Check that the line is a two-sentence story within the limit."""
    if not isinstance(line, str):
        raise ValueError("story must be text")
    if not line or line != line.strip():
        raise ValueError("story must be a single non-blank line")
    if "\n" in line or "\r" in line:
        raise ValueError("story must not contain a line break")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "story is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    if count_sentences(line) != 2:
        raise ValueError("story must be exactly two sentences")
    parts = [part.strip() for part in line.split(". ") if part.strip()]
    if len(parts) != 2:
        raise ValueError("story must be exactly two sentences")
    if "speaker" not in parts[0]:
        raise ValueError("first sentence must name the smart speaker")
    if "waiting" not in parts[1]:
        raise ValueError("second sentence must end on it waiting")
    return line


def store(line):
    """Print the story and save it to the entry file."""
    print(line)
    directory = os.path.dirname(OUTPUT_PATH)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")


def main():
    # Validate first, so only a well-formed story is ever stored.
    store(validate(LINE))


if __name__ == "__main__":
    main()
