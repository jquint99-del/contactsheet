import json
from pathlib import Path

from contactsheet.errors import InvalidVideoError
from contactsheet.models import VideoInfo
from contactsheet.runner import CommandRunner


def _parse_fps(rate: str) -> float:
    # ffprobe reports frame rate as a fraction, e.g. "30000/1001".
    if "/" in rate:
        num, den = rate.split("/")
        denom = float(den)
        return float(num) / denom if denom else 0.0
    return float(rate)


def probe_video(path: str | Path, runner: CommandRunner) -> VideoInfo:
    p = Path(path)
    if not p.is_file():
        raise InvalidVideoError(f"Video not found: {p}")
    result = runner.run(
        [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,avg_frame_rate",
            "-show_entries", "format=duration",
            "-of", "json",
            str(p),
        ]
    )
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    if not streams:
        raise InvalidVideoError(f"No video stream found in {p}")
    stream = streams[0]
    fmt = data.get("format", {})
    return VideoInfo(
        duration=float(fmt.get("duration", 0.0)),
        width=int(stream["width"]),
        height=int(stream["height"]),
        fps=_parse_fps(stream.get("avg_frame_rate", "0/1")),
    )