import pytest
from PIL import Image

from contactsheet.models import Frame, SheetSpec
from contactsheet.sheet import build_contact_sheet


def _make_frame(tmp_path, i):
    img = Image.new("RGB", (64, 36), (i * 20 % 255, 0, 0))
    p = tmp_path / f"f{i}.jpg"
    img.save(p)
    return Frame(path=str(p), timestamp=float(i))


def test_build_contact_sheet_writes_pdf(tmp_path):
    frames = [_make_frame(tmp_path, i) for i in range(6)]
    out = tmp_path / "sheet.pdf"
    result = build_contact_sheet(frames, SheetSpec(columns=3), out)
    assert result.exists()
    assert result.stat().st_size > 0


def test_build_contact_sheet_png_dimensions(tmp_path):
    frames = [_make_frame(tmp_path, i) for i in range(4)]
    out = tmp_path / "sheet.png"
    build_contact_sheet(frames, SheetSpec(columns=2, padding=8), out)
    sheet = Image.open(out)
    assert sheet.width > 64
    assert sheet.height > 36


def test_build_contact_sheet_empty_raises():
    with pytest.raises(ValueError):
        build_contact_sheet([], SheetSpec(), "x.pdf")