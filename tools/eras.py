"""Valid-time era bins for the 2026-06-29 → 2026-08-11 mouth dump."""

from __future__ import annotations

import datetime as dt

UTC = dt.timezone.utc

ERA_BINS = (
    ("t0_gateway", dt.datetime(2026, 6, 29, tzinfo=UTC), dt.datetime(2026, 7, 2, tzinfo=UTC)),
    ("t1_july_early", dt.datetime(2026, 7, 2, tzinfo=UTC), dt.datetime(2026, 7, 10, tzinfo=UTC)),
    ("t2_july_mid", dt.datetime(2026, 7, 10, tzinfo=UTC), dt.datetime(2026, 7, 16, tzinfo=UTC)),
    ("t3_july_late", dt.datetime(2026, 7, 16, tzinfo=UTC), dt.datetime(2026, 8, 3, tzinfo=UTC)),
    ("t4_august", dt.datetime(2026, 8, 3, tzinfo=UTC), dt.datetime(2026, 8, 21, tzinfo=UTC)),
)

SITUATIONS = (
    "protest_absence",
    "cover_witness",
    "absorb_vent",
    "melt_then_correct",
    "refuse_helper",
    "refuse_dissection",
    "location_echo",
    "repair_after_fix",
    "identity_phrase",
    "witness_snap",
    "scene_sex",
    "smalltalk_punish",
    "stubborn_choice",
    "self_conscious",
)


def parse_ts(ts) -> dt.datetime | None:
    if ts is None:
        return None
    if isinstance(ts, dt.datetime):
        t = ts
        if t.tzinfo is None:
            t = t.replace(tzinfo=UTC)
        return t.astimezone(UTC)
    if isinstance(ts, (int, float)):
        try:
            return dt.datetime.fromtimestamp(float(ts), UTC)
        except (OSError, OverflowError, ValueError):
            return None
    if isinstance(ts, str):
        raw = ts.strip()
        if not raw:
            return None
        try:
            return dt.datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(UTC)
        except ValueError:
            try:
                return dt.datetime.fromtimestamp(float(raw), UTC)
            except (OSError, OverflowError, ValueError):
                return None
    return None


def era_for(ts) -> str | None:
    t = parse_ts(ts)
    if t is None:
        return None
    for name, start, end in ERA_BINS:
        if start <= t < end:
            return name
    return None
