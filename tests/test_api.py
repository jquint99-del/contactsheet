import io

import pytest
from fastapi.testclient import TestClient

from contactsheet import api
from contactsheet.errors import InvalidVideoError


@pytest.fixture
def client():
    return TestClient(api.app)


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_contact_sheet_handles_bad_video(client, monkeypatch):
    def boom(*args, **kwargs):
        raise InvalidVideoError("bad video")

    monkeypatch.setattr(api, "extract_frames", boom)
    resp = client.post(
        "/contact-sheet",
        files={"file": ("clip.mp4", io.BytesIO(b"data"), "video/mp4")},
    )
    assert resp.status_code == 422
    assert "bad video" in resp.json()["detail"]