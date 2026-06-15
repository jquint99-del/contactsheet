import typer

from contactsheet.extract import extract_frames
from contactsheet.models import ExtractSpec, SheetSpec
from contactsheet.probe import probe_video
from contactsheet.runner import SubprocessRunner
from contactsheet.sheet import build_contact_sheet

app = typer.Typer(help="Turn a video into a contact-sheet PDF of evenly-spaced frames.")


@app.command()
def make(
    video: str,
    out: str = "contact_sheet.pdf",
    count: int = 12,
    columns: int = 4,
    width: int = 320,
    tmp_dir: str = ".frames",
) -> None:
    """Extract COUNT frames from VIDEO and assemble them into a contact sheet."""
    runner = SubprocessRunner()
    frames = extract_frames(video, ExtractSpec(count=count, width=width), runner, tmp_dir)
    path = build_contact_sheet(frames, SheetSpec(columns=columns), out)
    typer.echo(f"Wrote {path} ({len(frames)} frames)")


@app.command()
def probe(video: str) -> None:
    """Print basic metadata about VIDEO (duration, resolution, fps)."""
    info = probe_video(video, SubprocessRunner())
    typer.echo(f"duration={info.duration:.1f}s  {info.width}x{info.height}  {info.fps:.2f} fps")