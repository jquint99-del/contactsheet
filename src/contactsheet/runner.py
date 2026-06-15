import shutil
import subprocess
from dataclasses import dataclass
from typing import Protocol

from contactsheet.errors import FFmpegError, FFmpegNotFoundError


@dataclass
class CommandResult:
    stdout: str
    stderr: str


class CommandRunner(Protocol):
    def run(self, command: list[str]) -> CommandResult: ...


class SubprocessRunner:
    """Runs external commands, surfacing clear errors.

    Checks the binary exists before running, and raises FFmpegError
    (carrying stderr) on non-zero exit instead of a raw CalledProcessError.
    """

    def run(self, command: list[str]) -> CommandResult:
        binary = command[0]
        if shutil.which(binary) is None:
            raise FFmpegNotFoundError(
                f"'{binary}' was not found on your PATH. Install ffmpeg and try again."
            )
        proc = subprocess.run(command, capture_output=True, text=True)
        if proc.returncode != 0:
            raise FFmpegError(command, proc.returncode, proc.stderr)
        return CommandResult(stdout=proc.stdout, stderr=proc.stderr)