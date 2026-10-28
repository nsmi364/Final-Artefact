"""Run with:  python3 -m pytest -v"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import rules  # noqa: E402
from scenarios import ALL_SCENARIOS  # noqa: E402


@pytest.mark.parametrize("scenario", ALL_SCENARIOS, ids=lambda s: s.__name__)
def test_scenario(scenario):
    result = scenario()
    assert result["passed"], f"{result['id']}: expected {result['expected']}, got {result['actual']}"


def test_every_flag_has_a_reason():
    res = rules.apply_rules(rules.build_checkpoint_features(rules.load_data()))
    assert (res[res.flagged].reasons != "No indicators").all()


def test_next_opening_skips_booked_slot():
    from datetime import datetime
    from booking import make_booking, next_opening
    now = datetime(2026, 11, 2, 8, 0)                 # a Monday, 8am
    bookings = []
    assert next_opening(bookings, "Mia Chen", now) == (now.date(), "10:00")
    bookings.append({"learner_id": "L0001", "adviser": "Mia Chen", "date": now.date(), "time": "10:00"})
    assert next_opening(bookings, "Mia Chen", now) == (now.date(), "11:00")
