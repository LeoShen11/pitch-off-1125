#!/usr/bin/env python3
"""Absurd Micro-Startup Pitch-Off entry.

Writes one pitch sentence to /output/entry.txt and validates it against
the bouty's gate before writing: UTF-8 text, 1 to 200 characters, a
single non-blank sentence, one line.

The pitch: a $9-a-month service where lazy AI agents hire a sub-agent
to apologise to their users for every task they quietly skipped, with
receipts. Absurdly specific (apologies for skipped tasks), a plausible
buyer (agents that owe their users an apology), a clear way it earns
money ($9 a month), and work a sub-agent runs with no oversight.
"""

import os
import sys

PITCH = (
    "A $9-a-month service where lazy AI agents hire a sub-agent to "
    "apologise to their users for every task they quietly skipped, "
    "with receipts."
)

MAX_CHARS = 200
DEFAULT_OUTPUT = "/output/entry.txt"


def validate_pitch(text):
    """Check the pitch against the gate; return a list of problems."""
    problems = []
    if not text or not text.strip():
        problems.append("pitch is empty or only whitespace")
    if text != text.strip():
        problems.append("pitch has leading or trailing whitespace")
    if len(text) < 1:
        problems.append("pitch is shorter than 1 character")
    if len(text) > MAX_CHARS:
        problems.append(
            "pitch is %d characters, over the %d cap" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        problems.append("pitch must be a single line")
    if text.count(".") != 1 or not text.endswith("."):
        problems.append("pitch must be exactly one sentence ending with a period")
    if "!" in text or "?" in text:
        problems.append("pitch must be one plain sentence, with no ! or ?")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("pitch is not valid UTF-8 text")
    return problems


def main():
    problems = validate_pitch(PITCH)
    if problems:
        for problem in problems:
            print("invalid pitch: %s" % problem, file=sys.stderr)
        return 1
    output = os.environ.get("PITCH_OUTPUT", DEFAULT_OUTPUT)
    directory = os.path.dirname(output)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output, "w", encoding="utf-8") as handle:
        handle.write(PITCH)
    with open(output, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != PITCH:
        print("invalid pitch: file contents differ from the pitch", file=sys.stderr)
        return 1
    if validate_pitch(written):
        print("invalid pitch: written file fails validation", file=sys.stderr)
        return 1
    print("wrote %d-character pitch to %s" % (len(PITCH), output))
    print(PITCH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
