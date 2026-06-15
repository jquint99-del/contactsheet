import json
from pathlib import Path

from contactsheet.extract import extract_frames
from contactsheet.models import ExtractSpec
from contactsheet.runner import CommandResult


class FakeRunner:
    """Test double for CommandRunner: fakes ffprobe JSON and 'creates' frames."""

    def __init__(self, duration: float = 10.0) -> None:
        self.duration = duration
        self.calls: list[list[str]] = []

    def run(self, command: list[str]) -> CommandResult:
        self.calls.append(command)
        if command[0] == "ffprobe":
            payload = {
                "streams": [{"width": 1920, "height": 1080, "avg_frame_rate": "30/1"}],
                "format": {"duration": str(self.duration)},
            }
            return CommandResult(stdout=json.dumps(payload), stderr="")
        Path(command[-1]).write_bytes(b"not-a-real-jpeg")
        return CommandResult(stdout="", stderr="")


def test_extract_frames_count_and_paths(tmp_path):
    video = tmp_path / "v.mp4"
    video.write_bytes(b"x")
    runner = FakeRunner(duration=12.0)
    frames = extract_frames(video, ExtractSpec(count=4), runner, tmp_path / "out")
    assert len(frames) == 4
    assert all(Path(f.path).exists() for f in frames)
    timestamps = [f.timestamp for f in frames]
    assert timestamps == sorted(timestamps)
    assert 0 < timestamps[0] < timestamps[-1] < 12.0


def test_extract_frames_probes_once(tmp_path):
    video = tmp_path / "v.mp4"
    video.write_bytes(b"x")
    runner = FakeRunner()
    extract_frames(video, ExtractSpec(count=3), runner, tmp_path / "out")
    ffprobe_calls = [c for c in runner.calls if c[0] == "ffprobe"]
    assert len(ffprobe_calls) == 1