import io
from unittest import mock

from makefiles.utils import cli_io


class TestCliPrint:
    def test_prints_to_stdout_and_flushes(self):
        mock_stream = mock.MagicMock(spec=io.TextIOWrapper)
        with mock.patch("sys.stdout", mock_stream):
            cli_io.print("printed text")
            mock_stream.write.assert_called_once_with("printed text")
            mock_stream.flush.assert_called_once()
