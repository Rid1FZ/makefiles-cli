import io
from unittest import mock

from makefiles.utils import cli_io


class TestCliInput:
    def test_reads_input_from_stdin(self) -> None:
        """
        Should read a line from sys.stdin and strip the trailing newline.
        """
        with mock.patch("sys.stdin", new=io.StringIO("hello input\n")):
            result: str = cli_io.input()
            assert result == "hello input"
