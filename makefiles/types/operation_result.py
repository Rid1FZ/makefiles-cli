from typing import Any

from makefiles.types import ExitCode


class OperationResult:
    def __init__(
        self,
        result: Any,
        *,
        returncode: ExitCode | int = ExitCode(0),
        output_message: str | bytes = "",
        error_message: str | bytes = "",
    ):
        self.result = result
        self.returncode = returncode
        self.output_message = output_message
        self.error_message = error_message

    """
    A container representing the result of an operation or subprocess execution.

    This class encapsulates the outcome of an operation, including the result object,
    POSIX-compliant exit code, and both output and error messages. It enforces
    that `output_message` and `error_message` are either `str` or `bytes`, and that
    `returncode` is a valid `ExitCode`.

    Attributes:
        result (Any): The payload result of the operation. Can be any type.
        returncode (ExitCode): The exit status code of the operation (0–255).
        output_message (str): Standard output message. Accepts `str` or `bytes`.
        error_message (str): Standard error message. Accepts `str` or `bytes`.

    Arguments:
        result (Any): Arbitrary result returned by the operation.
        returncode (int | ExitCode): A valid integer or `ExitCode` in [0, 255].
        output_message (str | bytes, optional): The captured stdout (default: empty string).
        error_message (str | bytes, optional): The captured stderr (default: empty string).

    Raises:
        TypeError: If `returncode` is not an `int` or `ExitCode`, or not convertible.
        TypeError: If `output_message` or `error_message` is not `str` or `bytes`.

    Example:
        >>> result = OperationResult("OK", returncode=0)
        >>> print(result.returncode)
        0
        >>> print(result.output_message)
        ''
        >>> result = OperationResult(
        ...     result={"status": "success"},
        ...     returncode="0",
        ...     output_message=b"done",
        ...     error_message=""
        ... )
        >>> str(result)
        "OperationResult(result={'status': 'success'}, returncode=0, output_message='done', error_message='')"
    """

    def __str__(self) -> str:
        result: Any = self.result
        returncode: ExitCode = self.returncode
        output_message: str = self.output_message
        error_message: str = self.error_message

        return f"{self.__class__.__name__}({result=}, {returncode=}, {output_message=}, {error_message=})"

    @staticmethod
    def _verify_message(field_name: str, message: str | bytes) -> str:
        if isinstance(message, str):
            return message
        if isinstance(message, bytes):
            return message.decode(errors="replace")

        raise TypeError(f"{field_name} must be str or bytes. Got {type(message).__name__}")

    @property
    def result(self) -> Any:
        return self._result

    @result.setter
    def result(self, value: Any) -> None:
        self._result = value

    @property
    def returncode(self) -> ExitCode:
        return self._returncode

    @returncode.setter
    def returncode(self, value: ExitCode | int):
        if not isinstance(value, ExitCode):
            try:
                value = ExitCode(value)
            except (ValueError, TypeError):
                raise TypeError(f"'returncode' must be convertible to type ExitCode") from None

        self._returncode = value

    @property
    def output_message(self) -> str:
        return self._output_message

    @output_message.setter
    def output_message(self, value: str | bytes):
        self._output_message = self._verify_message("output_message", value)

    @property
    def error_message(self) -> str:
        return self._error_message

    @error_message.setter
    def error_message(self, value: str | bytes):
        self._error_message = self._verify_message("error_message", value)
