"""
Steady Step - simple saved storage
==================================
Bookings, adviser decisions and weekly check-ins are saved to data/app_state.json,
so they survive a page refresh and the adviser sees what the student did.
(A real deployment would use the University's secure database instead.)
"""

import json
from datetime import date
from pathlib import Path

STATE_FILE = Path(__file__).parent / "data" / "app_state.json"
EMPTY = {"bookings": [], "decisions": {}, "checkins": []}


def load_state():
    if not STATE_FILE.exists():
        return {k: (v.copy() if isinstance(v, (list, dict)) else v) for k, v in EMPTY.items()}
    state = json.loads(STATE_FILE.read_text())
    for item in state["bookings"] + state["checkins"]:
        item["date"] = date.fromisoformat(item["date"])        # text -> date
    return state


def save_state(bookings, decisions, checkins):
    def clean(items):
        return [{**i, "date": i["date"].isoformat()} for i in items]
    STATE_FILE.write_text(json.dumps({"bookings": clean(bookings), "decisions": decisions,
                                      "checkins": clean(checkins)}, indent=2))


def reset_state():
    if STATE_FILE.exists():
        STATE_FILE.unlink()
