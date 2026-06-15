class ContactSheetError(Exception):
    """Base class for all contactsheet errors."""


class FFmpegNotFoundError(ContactSheetError):
    """The ffmpeg/ffprobe binary is not on PATH."""


class FFmpegError(ContactSheetError):
    """An ffmpeg/ffprobe invocation exited non-zero."""

    def __init__(self, command: list[str], returncode: int, stderr: str) -> None:
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(
            f"Command failed ({returncode}): {' '.join(command)}\n{stderr.strip()}"
        )


class InvalidVideoError(ContactSheetError):
    """A video file is missing, empty, or has no video stream."""