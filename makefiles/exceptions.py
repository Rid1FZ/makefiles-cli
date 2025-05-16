class MKFileException(Exception):
    """Base exception for this project"""

    def __init__(self, *args) -> None:
        Exception.__init__(self, *args)


class TemplateCreationError(MKFileException):
    """Failed to create template"""

    def __init__(self, *args) -> None:
        MKFileException.__init__(self, *args)


class TemplateNotFoundError(TemplateCreationError):
    """Given template not found"""

    def __init__(self, *args) -> None:
        TemplateCreationError.__init__(self, *args)


class CopyError(MKFileException):
    """Failed to copy given file"""

    def __init__(self, *args) -> None:
        MKFileException.__init__(self, *args)


class InvalidSourceError(CopyError):
    """Given source is invalid"""

    def __init__(self, *args) -> None:
        CopyError.__init__(self, *args)


class SourceNotFoundError(CopyError, FileNotFoundError):
    """Given source does not exists"""

    def __init__(self, *args) -> None:
        FileNotFoundError.__init__(self, *args)


class DestinationExistsError(CopyError, FileExistsError):
    """Given destination already exists"""

    def __init__(self, *args) -> None:
        FileExistsError.__init__(self, *args)
