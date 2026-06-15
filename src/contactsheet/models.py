from pydantic import BaseModel, Field


class VideoInfo(BaseModel):
    duration: float  # seconds
    width: int
    height: int
    fps: float


class Frame(BaseModel):
    path: str
    timestamp: float  # seconds into the video


class ExtractSpec(BaseModel):
    count: int = Field(default=12, ge=1, le=200)
    width: int = Field(default=320, ge=16)


class SheetSpec(BaseModel):
    columns: int = Field(default=4, ge=1, le=12)
    padding: int = Field(default=8, ge=0)
    background: str = "white"
    label_timestamps: bool = True