class MKFileException(Exception):
    """Base exception for this project"""

    def __init__(self, *args) -> None:
        Exception.__init__(self, *args)


class InvalidPathError(MKFileException):
    """Path is invalid"""

    def __init__(self, *args) -> None:
        MKFileException.__init__(self, *args)


class PathNotFoundError(MKFileException):
    """Path does not exists"""

    def __init__(self, *args) -> None:
        MKFileException.__init__(self, *args)


class TemplateCreationError(MKFileException):
    """Failed to create template"""

    def __init__(self, *args) -> None:
        MKFileException.__init__(self, *args)


class TemplateNotFoundError(TemplateCreationError):
    """Template not found"""

    def __init__(self, *args) -> None:
        TemplateCreationError.__init__(self, *args)


class CopyError(MKFileException):
    """Failed to copy file"""

    def __init__(self, *args) -> None:
        MKFileException.__init__(self, *args)


class InvalidSourceError(CopyError, InvalidPathError):
    """Copy source is invalid"""

    def __init__(self, *args) -> None:
        CopyError.__init__(self, *args)


class SourceNotFoundError(CopyError, FileNotFoundError):
    """Copy source does not exists"""

    def __init__(self, *args) -> None:
        FileNotFoundError.__init__(self, *args)


class DestinationExistsError(CopyError, FileExistsError):
    """Copy destination already exists"""

    def __init__(self, *args) -> None:
        FileExistsError.__init__(self, *args)


class FZFError(MKFileException):
    """Failed to run fzf"""

    def __init__(self, *args) -> None:
        MKFileException.__init__(self, *args)


class FZFNotFoundError(FZFError):
    """fzf executable not found"""

    def __init__(self, *args) -> None:
        FZFError.__init__(self, *args)
