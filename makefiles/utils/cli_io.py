"""
This module has functions/classes which will be used for input/output from or to
terminal in this project. The standard `input` and `print` functions seems to
have some odd behaviours. For example, `input` functions sometimes writes
the `prompt` argument to `stderr` instead of `stdout`. To avoid inconsistency,
we will use functions/classes from `sys` module to handle input and output
manually.
"""

import io
import sys


def _write_to_stream(text: str, *, stream: io.TextIOWrapper) -> None:
    try:
        stream.write(text)
    except UnicodeEncodeError:
        # Fallback to safe encoding
        encoded = text.encode(stream.encoding or "utf-8", "backslashreplace")

        if hasattr(stream, "buffer"):
            stream.buffer.write(encoded)
        else:
            # Decode back to text if binary buffer is unavailable
            fallback_text = encoded.decode(stream.encoding or "utf-8", "strict")
            stream.write(fallback_text)


def print(text: str) -> None:
    stream: io.TextIOWrapper = sys.stdout  # type:ignore
    _write_to_stream(text, stream=stream)
    stream.flush()


def eprint(text: str) -> None:
    stream: io.TextIOWrapper = sys.stderr  # type:ignore
    _write_to_stream(text, stream=stream)
    stream.flush()


def input() -> str:
    stream: io.TextIOWrapper = sys.stdin  # type:ignore
    input: str = stream.readline().rstrip("\n")
    return input
