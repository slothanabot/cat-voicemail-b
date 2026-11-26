#!/usr/bin/env python3
"""Funniest Cat Voicemail Greeting (account B).

Saves a single line under $MAKEFUN_OUTPUT_DIR/entry.txt,
or under /output/entry.txt if that variable is not set.
That line has to be UTF-8, exactly one line, 1-120 characters long,
never blank, and contain no control characters.

The bit: the cat leaves the greeting in its own voice — the box it
just claimed, the 4am demand for food. A caller gets the joke in
seconds, with the punchline arriving ahead of the beep.
"""

import os

LINE = "Hi, you've reached Miso. I'm asleep in the box you just emptied. Leave a message — I'll demand food at 4am anyway."


def fail(message: str) -> None:
    """Stop the run with a short explanation of what went wrong."""
    raise SystemExit(message)


def build_line() -> str:
    """Return the line, validated as a single in-range line."""
    line = LINE.strip()
    if not line or "\n" in line or "\r" in line:
        fail("entry must be one non-empty line")
    if any(ord(ch) < 32 for ch in line):
        fail("entry must not contain control characters")
    if not 1 <= len(line) <= 120:
        fail(f"entry is {len(line)} chars, must be 1-120")
    return line


def write_entry(line: str) -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        raise SystemExit("round-trip check failed: entry.txt differs")
    return written


def main() -> None:
    written = write_entry(build_line())
    print(f"{written} ({len(written)} chars)")


if __name__ == "__main__":
    main()
