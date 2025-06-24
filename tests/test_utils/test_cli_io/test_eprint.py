import io
from unittest import mock

from makefiles.utils import cli_io


class TestCliEPrint:
    def test_prints_to_stderr_and_flushes(self):
        mock_stream = mock.MagicMock(spec=io.TextIOWrapper)
        with mock.patch("sys.stderr", mock_stream):
            cli_io.eprint("error text")
            mock_stream.write.assert_called_once_with("error text")
            mock_stream.flush.assert_called_once()
