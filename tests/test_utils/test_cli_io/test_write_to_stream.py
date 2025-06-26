import io
from unittest import mock

from makefiles.utils import cli_io


class TestWriteToStream:
    def test_writes_text_to_stream(self) -> None:
        """
        Should write the given text to the provided stream without error.
        """
        stream: io.StringIO = io.StringIO()
        cli_io._write_to_stream("hello world", stream=stream)
        assert stream.getvalue() == "hello world"

    def test_fallback_encoding_when_unicode_error(self) -> None:
        """
        Should fallback to encoded bytes when UnicodeEncodeError is raised.
        """
        fake_buffer: io.BytesIO = io.BytesIO()
        stream: mock.Mock = mock.Mock(spec=io.TextIOBase)

        # simulate encoding failure and provide fallback mechanisms
        stream.write.side_effect = UnicodeEncodeError("ascii", "€", 0, 1, "encoding error")
        stream.encoding = "ascii"
        stream.buffer = fake_buffer

        cli_io._write_to_stream("€", stream=stream)

        assert fake_buffer.getvalue() != b""
        assert b"\\" in fake_buffer.getvalue()  # expect backslash-escaped fallback
