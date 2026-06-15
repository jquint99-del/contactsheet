from pathlib import Path

from contactsheet.errors import InvalidVideoError
from contactsheet.models import ExtractSpec, Frame, VideoInfo
from contactsheet.probe import probe_video
from contactsheet.runner import CommandRunner


def _timestamps(duration: float, count: int) -> list[float]:
    if duration <= 0:
        raise InvalidVideoError("Video duration is zero or unknown; cannot extract frames.")
    step = duration / count
    # sample the midpoint of each evenly sized segment
    return [step * (i + 0.5) for i in range(count)]


def extract_frames(
    video: str | Path,
    spec: ExtractSpec,
    runner: CommandRunner,
    out_dir: str | Path,
    info: VideoInfo | None = None,
) -> list[Frame]:
    video_path = Path(video)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    if info is None:
        info = probe_video(video_path, runner)
    frames: list[Frame] = []
    for i, ts in enumerate(_timestamps(info.duration, spec.count)):
        frame_path = out / f"frame_{i:03d}.jpg"
        runner.run(
            [
                "ffmpeg",
                "-y",
                "-ss", f"{ts:.3f}",
                "-i", str(video_path),
                "-frames:v", "1",
                "-vf", f"scale={spec.width}:-1",
                str(frame_path),
            ]
        )
        frames.append(Frame(path=str(frame_path), timestamp=ts))
    return frames