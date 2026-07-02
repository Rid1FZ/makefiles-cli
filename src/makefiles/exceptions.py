class MKFileException(Exception):
    """Base exception for this project"""

    def __init__(self, message: str) -> None:
        super().__init__(self, message)


class InvalidPathError(MKFileException):
    """Path is invalid"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class PathNotFoundError(MKFileException, FileNotFoundError):
    """Path does not exists"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class TemplateCreationError(MKFileException):
    """Failed to create template"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoTemplatesAvailableError(MKFileException, FileNotFoundError):
    """No template found"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class TemplateNotFoundError(MKFileException, FileNotFoundError):
    """Given template not found"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class CopyError(MKFileException):
    """Failed to copy file"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidSourceError(CopyError, InvalidPathError):
    """Copy source is invalid"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class SourceNotFoundError(CopyError, FileNotFoundError):
    """Copy source does not exists"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DestinationExistsError(CopyError, FileExistsError):
    """Copy destination already exists"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class FZFError(MKFileException):
    """Failed to run fzf"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class FZFNotFoundError(FZFError):
    """fzf executable not found"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
