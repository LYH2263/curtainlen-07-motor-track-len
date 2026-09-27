"""motor_track: 电动轨长度 = 窗宽 + 左外延 + 右外延（米）。"""

DEFAULT_EXT = 0.15


def track_meters(window_w: float, ext_left: float, ext_right: float) -> dict:
    ext_left = float(ext_left)
    ext_right = float(ext_right)
    if ext_left < 0 or ext_right < 0:
        raise ValueError("track extension must be >= 0")
    length = float(window_w) + ext_left + ext_right
    return {
        "motor_track": True,
        "track_ext_left": ext_left,
        "track_ext_right": ext_right,
        "track_meters": round(length, 2),
    }
