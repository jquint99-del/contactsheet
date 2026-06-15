import pytest

from contactsheet.errors import FFmpegError, FFmpegNotFoundError
from contactsheet.runner import SubprocessRunner


def test_runner_captures_stdout():
    result = SubprocessRunner().run(["echo", "hello"])
    assert result.stdout.strip() == "hello"


def test_runner_raises_when_binary_missing():
    with pytest.raises(FFmpegNotFoundError):
        SubprocessRunner().run(["contactsheet-no-such-binary-xyz"])


def test_runner_raises_on_nonzero_exit():
    with pytest.raises(FFmpegError):
        SubprocessRunner().run(["false"])