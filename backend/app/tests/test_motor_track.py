import pytest
from fastapi import HTTPException

from app import seed
from app.modules.motor_track import DEFAULT_EXT, track_meters
from app.repositories import history, settings_repo
from app.services import estimate_service

seed.init_db()


def test_track_sum():
    r = track_meters(3.0, 0.15, 0.2)
    assert r["track_meters"] == 3.35
    assert r["motor_track"] is True
    assert r["track_ext_left"] == 0.15
    assert r["track_ext_right"] == 0.2


def test_track_negative_ext_rejected():
    with pytest.raises(ValueError):
        track_meters(3.0, -0.1, 0.2)


def test_motor_off_matches_base():
    r = estimate_service.run_estimate(1, 1, False, "")
    assert r["meters"] == 14.25
    assert "track_meters" not in r
    assert "motor_track" not in r


def test_motor_on_preview_not_saved():
    before = len(history.list_runs())
    r = estimate_service.run_estimate(1, 1, False, "", True, 0.2, 0.3)
    assert r["track_meters"] == 3.5
    assert r["meters"] == 14.25
    assert r["run_id"] is None
    assert len(history.list_runs()) == before


def test_motor_on_uses_settings_default_ext():
    r = estimate_service.run_estimate(1, 1, False, "", True, None, None)
    assert r["track_meters"] == round(3.0 + 2 * DEFAULT_EXT, 2)
    assert r["track_ext_left"] == DEFAULT_EXT


def test_negative_ext_fails_and_writes_no_history():
    before = len(history.list_runs())
    with pytest.raises(HTTPException):
        estimate_service.run_estimate(1, 1, True, "", True, -0.1, 0.2)
    assert len(history.list_runs()) == before


def test_saved_run_keeps_original_track_after_settings_change():
    r = estimate_service.run_estimate(1, 1, True, "", True, 0.2, 0.2)
    rid = r["run_id"]
    assert rid is not None
    settings_repo.set_value("default_track_ext", "0.9")
    try:
        preview = estimate_service.run_estimate(1, 1, False, "", True, None, None)
        assert preview["track_meters"] == 4.8
        saved = history.get_run(rid)
        assert saved["result"]["motor_track"] is True
        assert saved["result"]["track_meters"] == 3.4
        assert saved["result"]["track_ext_left"] == 0.2
        assert saved["result"]["track_ext_right"] == 0.2
        assert saved["result"]["meters"] == 14.25
    finally:
        settings_repo.set_value("default_track_ext", str(DEFAULT_EXT))
