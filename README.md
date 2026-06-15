# contactsheet

[![CI](https://github.com/jquint99-del/contactsheet/actions/workflows/ci.yml/badge.svg)](https://github.com/jquint99-del/contactsheet/actions/workflows/ci.yml)

Turn a video into a **contact sheet** — a single PDF (or PNG) of evenly-spaced
frames, each labeled with its timestamp. Handy for previewing footage, reviewing
shots, or scanning a clip at a glance.

`contactsheet` ships as both a command-line tool and a small FastAPI service,
built as a thin, well-tested layer over `ffmpeg`/`ffprobe`.

## Example

```bash
contactsheet make clip.mp4 --count 9 --columns 3 --out sheet.pdf
# Wrote sheet.pdf (9 frames)
```

## Install

Requires Python 3.11+ and `ffmpeg` (which provides `ffprobe`) on your PATH.

```bash
brew install ffmpeg          # macOS; use your package manager elsewhere

git clone https://github.com/jquint99-del/contactsheet
cd contactsheet
pip install -e ".[api,dev]"
```

## Usage

### CLI

```bash
contactsheet make VIDEO [--out sheet.pdf] [--count 12] [--columns 4] [--width 320]
contactsheet probe VIDEO
# duration=10.0s  640x360  30.00 fps
```

Output format is inferred from the `--out` extension (`.pdf`, `.png`, `.jpg`).

### API

```bash
uvicorn contactsheet.api:app --reload
```

- `GET /health` → `{"status": "ok"}`
- `POST /contact-sheet` (multipart `file`, optional `count`/`columns`) → returns a PDF

## How it works

```
video ──probe──▶ VideoInfo ──extract──▶ frames ──sheet──▶ contact_sheet.pdf
       (ffprobe)            (ffmpeg)             (Pillow)
```

1. **probe** reads duration/resolution/fps via `ffprobe`.
2. **extract** picks evenly-spaced timestamps (the midpoint of each segment) and
   pulls one frame each via `ffmpeg`.
3. **sheet** lays the frames out in a grid with Pillow and writes the file.

## Design notes

A few deliberate choices, since this is as much a portfolio piece as a tool:

- **The subprocess boundary sits behind a `CommandRunner` protocol.** Only
  `SubprocessRunner` actually shells out; `probe` and `extract` depend on the
  protocol. Tests inject a fake runner, so the whole pipeline is verified
  **offline, with no ffmpeg installed and no network** (`tests/test_extract.py`).
- **Errors are typed and carry context.** A failed call raises `FFmpegError` with
  the command and its stderr — not a bare `CalledProcessError`; a missing binary
  raises `FFmpegNotFoundError` with an actionable message.
- **One core, two interfaces.** The CLI and the API call the same
  `extract_frames` / `build_contact_sheet` functions; the web layer is a thin
  wrapper that maps domain errors to HTTP 422.

## Development

```bash
ruff check src tests   # lint
mypy src               # type-check
pytest -q              # 13 tests, hermetic
```

CI runs all three on every push.