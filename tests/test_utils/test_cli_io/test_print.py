import io
from unittest import mock

from makefiles.utils import cli_io


class TestCliPrint:
    def test_prints_to_stdout_and_flushes(self) -> None:
        """
        Should write text to sys.stdout and flush the stream.
        """
        mock_stream: mock.Mock = mock.MagicMock(spec=io.TextIOWrapper)
        with mock.patch("sys.stdout", mock_stream):
            cli_io.print("printed text")
            mock_stream.write.assert_called_once_with("printed text")
            mock_stream.flush.assert_called_once()
