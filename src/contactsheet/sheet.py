from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from contactsheet.models import Frame, SheetSpec

_LABEL_HEIGHT = 16


def _format_ts(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def build_contact_sheet(
    frames: list[Frame],
    spec: SheetSpec,
    out_path: str | Path,
) -> Path:
    if not frames:
        raise ValueError("No frames to assemble into a contact sheet.")
    thumbs = [Image.open(f.path).convert("RGB") for f in frames]
    label_h = _LABEL_HEIGHT if spec.label_timestamps else 0
    cell_w = max(t.width for t in thumbs)
    cell_h = max(t.height for t in thumbs) + label_h

    cols = spec.columns
    rows = (len(thumbs) + cols - 1) // cols
    pad = spec.padding
    sheet_w = cols * cell_w + (cols + 1) * pad
    sheet_h = rows * cell_h + (rows + 1) * pad

    sheet = Image.new("RGB", (sheet_w, sheet_h), spec.background)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for idx, (thumb, frame) in enumerate(zip(thumbs, frames)):
        row, col = divmod(idx, cols)
        x = pad + col * (cell_w + pad)
        y = pad + row * (cell_h + pad)
        sheet.paste(thumb, (x, y))
        if spec.label_timestamps:
            draw.text(
                (x + 2, y + thumb.height + 2),
                _format_ts(frame.timestamp),
                fill="black",
                font=font,
            )

    out = Path(out_path)
    sheet.save(out)  # Pillow infers PDF/PNG/JPEG from the extension
    return out