import io
from unittest import mock

from makefiles.utils import cli_io


class TestCliInput:
    def test_reads_input_from_stdin(self):
        with mock.patch("sys.stdin", new=io.StringIO("hello input\n")):
            result = cli_io.input()
            assert result == "hello input"
