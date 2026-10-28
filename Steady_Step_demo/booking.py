"""
Steady Step - booking logic
===========================
Bookings are kept in the app session (st.session_state) - SIMULATED storage.
A real deployment would save them in the University's booking system.
"""

from datetime import date

ADVISERS = {
    "Mia Chen": "Academic Success Adviser - study skills, catching up on work",
    "Jordan Williams": "Wellbeing & Support Adviser - stress, balance, personal challenges",
    "Ari Patel": "Course Planning Adviser - workload, changing papers, degree planning",
}
TIME_SLOTS = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]


def make_booking(bookings, learner_id, adviser, day, time, note=""):
    """Validate and add a booking. Returns (ok, message).

    Rules:
      - adviser must exist and the time must be a listed slot
      - date cannot be in the past
      - an adviser cannot be double-booked for the same date and time
    """
    if adviser not in ADVISERS:
        return False, f"Unknown adviser: {adviser}"
    if time not in TIME_SLOTS:
        return False, f"{time} is not an available time slot"
    if day < date.today():
        return False, "Please choose today or a future date"
    for b in bookings:
        if b["adviser"] == adviser and b["date"] == day and b["time"] == time:
            return False, f"{adviser} is already booked at {time} on {day:%a %d %b}. Please pick another time."

    bookings.append({"learner_id": learner_id, "adviser": adviser, "date": day,
                     "time": time, "note": note.strip(), "status": "Confirmed"})
    return True, f"Booked with {adviser} on {day:%A %d %B} at {time}."


def next_opening(bookings, adviser, now=None, days_ahead=14):
    """First free time slot for an adviser (weekdays only), skipping booked slots
    and times that have already passed today. Returns (date, time) or None."""
    from datetime import datetime, timedelta
    now = now or datetime.now()
    taken = {(b["date"], b["time"]) for b in bookings if b["adviser"] == adviser}
    for i in range(days_ahead):
        day = now.date() + timedelta(days=i)
        if day.weekday() >= 5:                       # Saturday / Sunday
            continue
        for t in TIME_SLOTS:
            if i == 0 and int(t[:2]) <= now.hour:    # already passed today
                continue
            if (day, t) not in taken:
                return day, t
    return None


def opening_label(opening, today=None):
    """(date, time) -> 'Today, 14:00' / 'Tomorrow, 10:00' / 'Thu 30 Oct, 11:00'."""
    if opening is None:
        return "No times in the next 2 weeks"
    day, time = opening
    today = today or date.today()
    if day == today:
        return f"Today, {time}"
    if (day - today).days == 1:
        return f"Tomorrow, {time}"
    return f"{day:%a %d %b}, {time}"
