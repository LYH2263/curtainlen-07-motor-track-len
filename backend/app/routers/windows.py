from fastapi import APIRouter, HTTPException
from app.modules.motor_track import DEFAULT_EXT, track_meters
from app.repositories import settings_repo
from app.repositories import windows as repo
router = APIRouter()
@router.get("/windows")
def list_windows(): return {"items": repo.list_windows()}
@router.get("/windows/{wid}")
def get_window(wid: int):
    r = repo.get_window(wid)
    if not r: raise HTTPException(404)
    ext = float(settings_repo.get_all().get("default_track_ext") or DEFAULT_EXT)
    r["track_ext"] = ext
    r["track_meters"] = track_meters(r["width"], ext, ext)["track_meters"]
    return r
