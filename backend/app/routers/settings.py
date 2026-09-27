from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.repositories import settings_repo
router = APIRouter()

class SettingIn(BaseModel):
    key: str
    value: str

@router.get("/settings")
def settings(): return settings_repo.get_all()

@router.post("/settings")
def set_setting(body: SettingIn):
    if body.key == "default_track_ext":
        try:
            if float(body.value) < 0:
                raise ValueError
        except ValueError:
            raise HTTPException(422, "default_track_ext must be a number >= 0")
    settings_repo.set_value(body.key, body.value)
    return settings_repo.get_all()
