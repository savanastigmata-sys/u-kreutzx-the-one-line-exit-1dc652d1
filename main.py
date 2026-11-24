#!/usr/bin/env python3
"""The One-Line Exit — writes one funny resignation line to entry.txt.

Deterministic: no randomness, no network, no clock. The output is a
single fixed line, 1-140 characters, validated before it is written.
"""

import os
import sys

MAX_CHARS = 140

# The line is built from two named parts so the joke's structure is
# explicit: a setup that sounds like a real resignation, then a turn.
SETUP = "I hereby resign: the office plant died on my watch,"
PUNCHLINE = "and unlike it, I refuse to be watered once a week and ignored."

EXIT_LINE = SETUP + " " + PUNCHLINE


def resolve_output_dir():
    """Where entry.txt goes: $MAKEFUN_OUTPUT_DIR, else ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return os.path.abspath(out)
    return os.path.abspath(os.path.join(os.getcwd(), "output"))


def write_entry(line, out_dir):
    """Write the line, then read it back and prove it round-trips."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    with open(path, "rb") as f:
        written = f.read()
    if written != line.encode("utf-8"):
        raise RuntimeError("entry.txt round-trip mismatch")
    if len(written.decode("utf-8")) != len(line):
        raise RuntimeError("entry.txt character count changed on disk")
    return path


def validate(text):
    """Gate mirror: UTF-8, 1-140 chars, exactly one line, not blank."""
    if not isinstance(text, str):
        raise ValueError("exit line must be text")
    if not text.strip():
        raise ValueError("exit line must not be only whitespace")
    if text != text.strip():
        raise ValueError("exit line must not have leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("exit line must be exactly one line")
    if len(text) > MAX_CHARS:
        raise ValueError("exit line is %d chars, over %d" % (len(text), MAX_CHARS))
    if "resign" not in text.lower():
        raise ValueError("exit line must read as a resignation letter")
    if ":" not in text:
        raise ValueError("exit line must carry its turn after a colon")
    if len(text.split()) < 10:
        raise ValueError("exit line is too thin to land its joke")
    text.encode("utf-8")
    return text


def main():
    line = validate(EXIT_LINE)
    out_dir = resolve_output_dir()
    path = write_entry(line, out_dir)
    print("wrote %d chars to %s" % (len(line), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
