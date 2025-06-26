import pytest

from makefiles.types import ExitCode, OperationResult


class TestOperationResult:
    """Unit tests for the OperationResult class."""

    def test_default_construction(self) -> None:
        """Test that default arguments are assigned correctly."""
        result: OperationResult = OperationResult()
        assert result.result is None
        assert result.returncode == ExitCode(0)
        assert result.output_message == ""
        assert result.error_message == ""

    @pytest.mark.parametrize(
        "code",
        [
            0,
            1,
            ExitCode(2),
            "3",
        ],
    )
    def test_returncode_accepts_int_or_exitcode(self, code: str | int | ExitCode) -> None:
        """Test that returncode accepts int and ExitCode and is coerced correctly."""
        obj: OperationResult = OperationResult("data", returncode=code)

        assert isinstance(obj.returncode, ExitCode)
        assert int(obj.returncode) == int(code)

    def test_output_and_error_messages_accept_str_and_bytes(self) -> None:
        """Test that messages are accepted as str or bytes and decoded properly."""
        obj: OperationResult = OperationResult("res", output_message=b"stdout", error_message=b"stderr")

        assert obj.output_message == "stdout"
        assert obj.error_message == "stderr"

        obj.output_message = "new out"
        obj.error_message = "new err"

        assert obj.output_message == "new out"
        assert obj.error_message == "new err"

    @pytest.mark.parametrize(
        "invalid_returncode",
        [
            object(),
            3.14,  # float
            complex(1, 2),  # complex number
            None,  # NoneType
            [],  # list
            {},  # dict
            set(),  # set
            True,  # bool (valid int technically, but test for stricter type expectations)
            "not a number",  # non-numeric string
            b"42",  # byte string
        ],
    )
    def test_invalid_returncode_raises_typeerror(self, invalid_returncode):
        """Test that invalid returncode types raise a TypeError."""
        with pytest.raises(TypeError, match="'returncode' must be convertible to type ExitCode"):
            OperationResult("x", returncode=invalid_returncode)

    @pytest.mark.parametrize("field", ["output_message", "error_message"])
    @pytest.mark.parametrize(
        "invalid_value",
        [
            123.456,  # float
            0,  # int
            None,  # NoneType
            object(),  # arbitrary object
            [],  # list
            {},  # dict
            set(),  # set
            True,  # bool
            complex(2, 3),  # complex number
            bytearray(b"abc"),  # bytearray is not bytes
            memoryview(b"mem"),  # memoryview
        ],
    )
    def test_invalid_message_type_raises_typeerror(self, field, invalid_value):
        """Test that non-str/bytes messages raise TypeError."""
        obj: OperationResult = OperationResult("res")

        with pytest.raises(TypeError, match=f"{field} must be str or bytes"):
            setattr(obj, field, invalid_value)

    def test_str_representation(self) -> None:
        """Test the __str__ method produces expected format."""
        obj: OperationResult = OperationResult(result={"a": 1}, returncode=0, output_message="done", error_message="")

        stringified: str = str(obj)

        assert "OperationResult(" in stringified
        assert "result={'a': 1}" in stringified
        assert "returncode=0" in stringified
        assert "output_message='done'" in stringified
