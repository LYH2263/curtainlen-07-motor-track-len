from fastapi import HTTPException
from app.engines.curtain_math import fabric_meters
from app.modules.motor_track import DEFAULT_EXT, track_meters
from app.repositories import fabrics, history, settings_repo, windows

def run_estimate(window_id: int, fabric_id: int, save: bool, note: str,
                 motor_track: bool = False, ext_left=None, ext_right=None):
    w = windows.get_window(window_id)
    f = fabrics.get_fabric(fabric_id)
    if not w or not f:
        raise HTTPException(404, "not found")
    if w.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty window")
    settings = settings_repo.get_all()
    fullness = float(w.get("fullness") or settings.get("default_fullness", 2.0))
    calc = fabric_meters(w["width"], w["height"], fullness, f["hem_top"], f["hem_bottom"], f["fabric_width"])
    if motor_track:
        default_ext = float(settings.get("default_track_ext") or DEFAULT_EXT)
        left = default_ext if ext_left is None else float(ext_left)
        right = default_ext if ext_right is None else float(ext_right)
        try:
            calc.update(track_meters(w["width"], left, right))
        except ValueError as e:
            raise HTTPException(422, str(e))
    run_id = history.insert_run(window_id, fabric_id, calc, note) if save else None
    return {"window": w, "fabric": f, "run_id": run_id, **calc}
