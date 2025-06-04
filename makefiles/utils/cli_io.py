"""
This module provides functions and classes for handling terminal input and output
in a consistent and controlled manner.

The built-in `input` and `print` functions can exhibit inconsistent behavior.
For example, the `input` function may write its prompt to `stderr` instead of
`stdout` under certain conditions. To avoid such inconsistencies, this module
uses the `sys` module to manage input and output manually.
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
    """
    Writes the specified text to standard output (stdout) and flushes the stream.

    Args:
        text (str): The text string to be written to stdout.

    Notes:
        This function bypasses the built-in `print` to provide consistent
        output behavior by directly writing to `sys.stdout`.

    Side Effects:
        Flushes the stdout buffer immediately after writing.
    """
    stream: io.TextIOWrapper = sys.stdout  # type:ignore
    _write_to_stream(text, stream=stream)
    stream.flush()


def eprint(text: str) -> None:
    """
    Writes the specified text to standard error (stderr) and flushes the stream.

    Args:
        text (str): The text string to be written to stderr.

    Notes:
        This function directly writes to `sys.stderr`, providing consistent error
        output behavior, bypassing the built-in `print`.

    Side Effects:
        Flushes the stderr buffer immediately after writing.
    """
    stream: io.TextIOWrapper = sys.stderr  # type:ignore
    _write_to_stream(text, stream=stream)
    stream.flush()


def input() -> str:
    """
    Reads a line of input from standard input (stdin) and returns it as a string.

    Returns:
        str: The input string with the trailing newline character removed.

    Notes:
        This function reads directly from `sys.stdin` to avoid inconsistencies
        sometimes observed with the built-in `input` function.
    """
    stream: io.TextIOWrapper = sys.stdin  # type:ignore
    input: str = stream.readline().rstrip("\n")
    return input
