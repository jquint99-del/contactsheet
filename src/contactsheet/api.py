import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from contactsheet.errors import ContactSheetError
from contactsheet.extract import extract_frames
from contactsheet.models import ExtractSpec, SheetSpec
from contactsheet.runner import SubprocessRunner
from contactsheet.sheet import build_contact_sheet

app = FastAPI(title="contactsheet", description="Video to contact-sheet PDF")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/contact-sheet")
async def contact_sheet(
    file: UploadFile = File(...),
    count: int = 12,
    columns: int = 4,
) -> FileResponse:
    workdir = Path(tempfile.mkdtemp())
    video_path = workdir / (file.filename or "upload.mp4")
    video_path.write_bytes(await file.read())
    out_path = workdir / "contact_sheet.pdf"
    runner = SubprocessRunner()
    try:
        frames = extract_frames(video_path, ExtractSpec(count=count), runner, workdir / "frames")
        build_contact_sheet(frames, SheetSpec(columns=columns), out_path)
    except ContactSheetError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return FileResponse(out_path, media_type="application/pdf", filename="contact_sheet.pdf")