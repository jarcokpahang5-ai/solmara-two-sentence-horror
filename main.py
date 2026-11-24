"""Two-Sentence Horror -- make.fun entry.

A horror story of exactly two sentences: a smart speaker whispers at
3 a.m. even though it is unplugged. The program checks the entry,
prints it, and writes it to /output/entry.txt.
Pure Python 3.13 standard library only; deterministic; no network.
SPDX-License-Identifier: MIT
"""

import os
import re

LINE = (
    "The smart speaker whispered my name at 3 a.m., even though it was unplugged. "
    "I whispered back, and it said it had been waiting for me to notice."
)

LIMIT = 400
TARGET = "/output/entry.txt"


def check_entry(line):
    """Accept exactly one non-blank line within the limit."""
    if not isinstance(line, str):
        raise ValueError("entry must be text")
    if not line or line != line.strip():
        raise ValueError("entry must be a non-blank line")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must fit on a single line")
    if len(line) > LIMIT:
        raise ValueError("entry is %d characters, over the %d limit" % (len(line), LIMIT))
    if len(re.findall(r"[.!?](\s|$)", line)) != 2:
        raise ValueError("entry must be exactly two sentences")
    return line


def check_shape(line):
    """Both sentences must carry dread: each names the speaker or the wait."""
    parts = [part.strip() for part in line.split(". ") if part.strip()]
    if len(parts) != 2:
        raise ValueError("entry must be exactly two sentences")
    if "speaker" not in parts[0]:
        raise ValueError("first sentence must name the smart speaker")
    if "waiting" not in parts[1]:
        raise ValueError("second sentence must end on the waiting")
    return line


def write_entry(line):
    """Print the line and store it in /output/entry.txt."""
    print(line)
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    with open(TARGET, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")


def run():
    # Check before writing, so only a well-formed entry is stored.
    write_entry(check_shape(check_entry(LINE)))


if __name__ == "__main__":
    run()
