import io

from makefiles.utils import cli_io


class TestWriteToStream:
    def test_writes_text_to_stream(self):
        stream = io.StringIO()
        cli_io._write_to_stream("hello world", stream=stream)
        assert stream.getvalue() == "hello world"

    def test_fallback_encoding_when_unicode_error(self):
        class FakeStream(io.StringIO):
            def __init__(self):
                super().__init__()
                self._buffer = io.BytesIO()

            def write(self, text):
                # make _write_to_stream function use fallback
                raise UnicodeEncodeError("ascii", text, 0, len(text), "encoding error")

            @property
            def encoding(self) -> str:
                return "ascii"

            @property
            def buffer(self) -> io.BytesIO:
                return self._buffer

        stream = FakeStream()
        cli_io._write_to_stream("€", stream=stream)
        assert stream.buffer.getvalue() != b""
