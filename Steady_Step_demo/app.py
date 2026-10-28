"""
Steady Step - final artefact (Streamlit)
INFOMGMT 399 Group 2 (The Big 4) - Proposal 2: Student Dropout Risk

Flow:  synthetic CSVs -> rules.py (day-21 indicators -> flag + reasons)
       -> ADVISER reviews each flag and decides (Contact / Monitor / No action)
       -> STUDENT sees their progress; asked to check in only if the adviser chose "Contact learner"
       -> student books an adviser -> saved (storage.py) and shown to both sides
Run:   streamlit run app.py
"""

from datetime import date, timedelta
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import rules
import storage
import ui
from booking import ADVISERS, TIME_SLOTS, make_booking, next_opening, opening_label
from fairness import FAIRNESS_FIELDS, flag_rates
from scenarios import run_all

st.set_page_config(page_title="Steady Step", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")
ui.inject_css()

# Open the sidebar when the page first loads (Streamlit otherwise remembers it was closed)
components.html("""<script>
const doc = window.parent.document;
if (!window.parent.__ssSidebarOpened) {
  window.parent.__ssSidebarOpened = true;
  setTimeout(() => {
    const btn = doc.querySelector('[data-testid="stExpandSidebarButton"] button, [data-testid="stExpandSidebarButton"]');
    if (btn && btn.offsetParent !== null) btn.click();
  }, 400);
}
</script>""", height=0)


# ---------------- 1. DATA (input) ----------------
@st.cache_data
def get_data():
    data = rules.load_data()
    return data, rules.build_checkpoint_features(data)


data, features = get_data()
results = rules.apply_rules(features)                    # default rule: bottom 25%, 2+ indicators

# ---------------- saved app state (bookings, decisions, check-ins) ----------------
if "loaded" not in st.session_state:
    saved = storage.load_state()
    st.session_state.update(bookings=saved["bookings"], decisions=saved["decisions"],
                            checkins=saved["checkins"], loaded=True)
for key, default in {"spage": "Overview", "ci_step": 0, "ci_answers": {}, "ci_result": None,
                     "just_booked": None}.items():
    st.session_state.setdefault(key, default)


def save():
    storage.save_state(st.session_state.bookings, st.session_state.decisions, st.session_state.checkins)


def go(page):
    """Button callback: jump to another student page."""
    st.session_state.spage = page


STUDENT_PAGES = {"Overview": ":material/grid_view:", "Weekly check-in": ":material/check_circle:",
                 "My progress": ":material/monitoring:", "Find support": ":material/calendar_month:"}
ADVISER_PAGES = {"Learners to check in with": ":material/group:", "Fairness check": ":material/balance:",
                 "How it works": ":material/account_tree:"}

# ---------------- SIDE MENU ----------------
ui.sidebar_logo()
with st.sidebar.container(key="nav"):
    if st.session_state.get("view", "Student") == "Student":
        ui.side_label("YOUR SPACE", st)
        page = st.radio("Menu", list(STUDENT_PAGES), key="spage", label_visibility="collapsed",
                        format_func=lambda p: f"{STUDENT_PAGES[p]}  {p}")
    else:
        ui.side_label("ADVISER TOOLS", st)
        page = st.radio("Menu", list(ADVISER_PAGES), key="apage", label_visibility="collapsed",
                        format_func=lambda p: f"{ADVISER_PAGES[p]}  {p}")
ui.side_label("SIGNED IN AS (TEST ACCOUNT)")
view = st.sidebar.radio("View", ["Student", "Adviser"], key="view", horizontal=True, label_visibility="collapsed")
if view == "Student":
    learner_id = st.sidebar.selectbox("Learner", features.learner_id, label_visibility="collapsed")
st.sidebar.caption("Check-point: end of Week 3 (day 21) · synthetic data")


# =====================================================================
# STUDENT PAGES
# =====================================================================
if view == "Student":
    me = results[results.learner_id == learner_id].iloc[0]                 # own record only
    decision = st.session_state.decisions.get(learner_id, "Not reviewed")
    shown = rules.student_view_status(me, decision)                        # adviser decides what is shown
    my_checkins = [c for c in st.session_state.checkins if c["learner_id"] == learner_id]
    my_bookings = [b for b in st.session_state.bookings if b["learner_id"] == learner_id]

    # ------------------------------------------------------------ Overview
    if page == "Overview":
        green = {"On track": "You're doing more right than you think.",
                 "Worth keeping an eye on": "You're closer than you think.",
                 "Suggested check-in": "Let's find your footing together."}[shown]
        wants_chat = decision == "Contact learner" and not my_bookings

        head, action = st.columns([3.2, 1], vertical_alignment="center")
        with head:
            ui.page_header("Week 3 check-point", f"Hey, {learner_id}.", green,
                           f"Your steady view of {me.course_code}. No judgement, just useful next steps.")
        with action:
            if wants_chat:
                st.button("Book a chat →", type="primary", on_click=go, args=("Find support",),
                          use_container_width=True)
            else:
                st.button("Do my check-in →", type="primary", on_click=go, args=("Weekly check-in",),
                          use_container_width=True)

        if wants_chat:
            ui.md('<div class="ss-banner"><b>Your adviser would like to check in.</b> '
                  'A short conversation can help you get back on track.</div>')

        # two cards, always the same height
        n_ci = len(my_checkins)
        duration = int(data["courses"].set_index("course_code").course_duration_days[me.course_code])
        pct = round(100 * rules.CHECKPOINT_DAY / duration)
        momentum = (f'<div class="ss-dark ss-spread">'
                    f'<div><div class="ss-bubble"><b>{n_ci}</b><small>CHECK-IN{"" if n_ci == 1 else "S"}</small></div>'
                    f'<span class="ss-mono" style="color:#9DA1BC">YOUR MOMENTUM</span></div>'
                    f'<div><span class="ss-big">{me.active_days_to_day21}</span> <span>of 22 days</span><br>'
                    f'<span style="color:#B9BCD0">active on Canvas in your first three weeks</span></div>'
                    f'<div><div class="ss-bar"><div style="width:{pct}%"></div></div>'
                    f'<span style="color:#B9BCD0;font-size:.85rem">Keep the rhythm going</span>'
                    f'<span class="ss-mono" style="float:right;color:#9DA1BC">CHECK-POINT · DAY 21</span></div></div>')
        reasons = ("".join(f"<li>{r}</li>" for r in me.student_reasons) if shown != "On track"
                   else "<li>No warning signs by the Week 3 check-point.</li><li>Keep using Canvas and submitting on time.</li>")
        quick = (f'<div class="ss-card"><span class="ss-mono">A QUICK READ</span>'
                 f'<span style="float:right">{ui.pill(shown)}</span><br><br>'
                 f'{ui.ring(int(me.indicator_count), shown)}<b>{shown}</b><br>'
                 f'<span class="ss-muted">{ui.STATUS[shown][4]}</span><div style="clear:both"></div>'
                 + (f'<ul class="ss-muted" style="margin:10px 0 0 0;padding-left:20px;font-size:.88rem">{reasons}</ul>' if reasons else "")
                 + '</div>')
        ui.grid(momentum, quick)

        # three equal tiles
        next_step = "Book a chat" if wants_chat else ("Chat booked" if my_bookings else "Weekly check-in")
        ui.grid(ui.tile("🖱️", "Canvas interactions", me.interactions_to_day21),
                ui.tile("📝", "First quiz", me.first_quiz_status.capitalize(), "#FDEBDD"),
                ui.tile("💗", "Next step", next_step, "#FBE3EC"))

    # ------------------------------------------------------- Weekly check-in
    elif page == "Weekly check-in":
        QUESTIONS = [
            ("How well did you keep up with classes this week?",
             ["Fell behind", "Missed a few", "Mostly there", "Kept up", "All in"]),
            ("How are you feeling about your study?",
             ["Overwhelmed", "Stretched", "Okay", "Pretty good", "Great"]),
            ("How confident are you about your grades?",
             ["Not confident", "A few worries", "Finding my feet", "Feeling good", "I know my stuff"]),
        ]
        ui.page_header("Weekly reset · 2 min", "A quick check-in,", "just for you.",
                       "Three honest taps. Private to you, and not used in the early-support flag.")
        step, answers = st.session_state.ci_step, st.session_state.ci_answers

        if st.session_state.ci_result:                                              # ----- result
            low = st.session_state.ci_result == "Seek support"
            with st.container(border=True):
                ui.md(f'<div style="text-align:center;padding:14px 0 4px">'
                      f'<div class="ss-eyebrow">Your weekly read</div>'
                      f'<div class="ss-title" style="font-size:2rem">'
                      f'{"You deserve some backup." if low else "You&#39;re finding your rhythm."}</div>'
                      f'<div class="ss-muted">'
                      f'{"No need to wait for things to get worse - a friendly chat can help you find your next step." if low else "That is a strong week. Keep choosing the next small thing."}'
                      f'</div></div>')
                b1, b2 = st.columns(2)
                b1.button("Find an adviser →" if low else "See my progress →", type="primary",
                          on_click=go, args=("Find support" if low else "My progress",), use_container_width=True)
                if b2.button("Done for now", use_container_width=True):
                    st.session_state.ci_result = None
                    st.rerun()
        else:                                                                       # ----- questions
            question, labels = QUESTIONS[step]
            with st.container(border=True):
                ui.md(f'<span class="ss-mono">QUESTION {step + 1} OF 3</span>'
                      f'<div class="ss-h2" style="font-size:1.4rem;margin-top:6px">{question}</div>')
                for i, col in enumerate(st.columns(5)):
                    with col.container(key=f"opt{step}_{i}"):
                        chosen = answers.get(step) == i + 1
                        if st.button(f"{'✓ ' if chosen else ''}{i + 1}\n\n{labels[i]}", key=f"q{step}_{i}",
                                     type="primary" if chosen else "secondary", use_container_width=True):
                            answers[step] = i + 1
                            st.rerun()
                if step == 2:
                    st.text_input("Anything else on your mind? (optional)", key="ci_note")
                back, _, nxt = st.columns([1, 1, 1.5])
                if step > 0 and back.button("‹ Back"):
                    st.session_state.ci_step -= 1
                    st.rerun()
                if nxt.button("See my weekly read →" if step == 2 else "Next →", type="primary",
                              disabled=step not in answers, use_container_width=True):
                    if step == 2:
                        avg = round(sum(answers.values()) / 3, 1)
                        result = "Seek support" if avg <= 2.5 else "Keep going"   # rule: average 2.5 or below
                        st.session_state.checkins.append({
                            "learner_id": learner_id, "date": date.today(), "classes": answers[0],
                            "feeling": answers[1], "confidence": answers[2], "average": avg,
                            "result": result, "note": st.session_state.get("ci_note", "")})
                        save()
                        st.session_state.update(ci_result=result, ci_step=0, ci_answers={})
                    else:
                        st.session_state.ci_step += 1
                    st.rerun()

        if my_checkins:
            with st.container(border=True):
                ui.section("Your rhythm", "Previous check-ins")
                ui.md("".join(f'<div class="ss-row"><span><b>{c["date"]:%d %b}</b> · {c["result"]}</span>'
                              f'<span class="ss-mono">average {c["average"]} / 5</span></div>'
                              for c in my_checkins[::-1][:3]))

    # ----------------------------------------------------------- My progress
    elif page == "My progress":
        ui.page_header("Your rhythm", "My progress,", "week by week.",
                       "What we can see up to the Week 3 check-point.")
        s1, s2, s3 = st.columns(3)
        ui.md(ui.stat("Canvas interactions", me.interactions_to_day21), s1)
        ui.md(ui.stat("First quiz", me.first_quiz_status.capitalize()), s2)
        ui.md(ui.stat("Registered", "On time" if me.registration_day <= 0 else f"Day {int(me.registration_day)}"), s3)

        act = data["learning_activity"]
        act = act[(act.course_code == me.course_code) & act.activity_day.between(0, rules.CHECKPOINT_DAY)]
        act = act.assign(week="Week " + ((act.activity_day - 1).clip(lower=0) // 7 + 1).astype(str))
        n_class = int((results.course_code == me.course_code).sum())
        mine = act[act.learner_id == learner_id].groupby("week").interaction_count.sum()
        cls = act.groupby("week").interaction_count.sum() / n_class
        chart = (pd.DataFrame({"Me": mine, "Class average": cls.round(1)}).reindex(["Week 1", "Week 2", "Week 3"])
                 .fillna(0).reset_index(names="week").melt("week", var_name="who"))
        with st.container(border=True):
            ui.section("Signal, not scorekeeping", "Canvas activity compared with your class")
            ui.chart(alt.Chart(chart).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                            .encode(x=alt.X("week", title=None, axis=alt.Axis(labelAngle=0)), xOffset="who",
                                    y=alt.Y("value", title="Interactions"),
                                    color=alt.Color("who", title=None, legend=alt.Legend(orient="top"),
                                                    scale=alt.Scale(domain=["Me", "Class average"],
                                                                    range=[ui.GREEN, "#C9C3B6"])))
                            .properties(height=240))
        with st.container(border=True):
            ui.section("What we noticed", "By the end of Week 3")
            for r in me.student_reasons or ["Nothing to worry about - you're engaging well."]:
                st.write("• " + r)

    # ---------------------------------------------------------- Find support
    elif page == "Find support":

        @st.dialog("Book a conversation")
        def booking_dialog(adviser):
            st.markdown(f"**{adviser}** · {ADVISERS[adviser].split(' - ')[0]}")
            opening = next_opening(st.session_state.bookings, adviser)       # pre-fill the next free slot
            first_day, first_time = opening if opening else (date.today() + timedelta(days=1), TIME_SLOTS[0])
            c1, c2 = st.columns(2)
            day = c1.date_input("Date", value=first_day, min_value=date.today())
            time = c2.selectbox("Time", TIME_SLOTS, index=TIME_SLOTS.index(first_time))
            note = st.text_input("What would you like to talk about?", placeholder="e.g. Catching up on study")
            if st.button("Confirm booking", type="primary", use_container_width=True):
                ok, msg = make_booking(st.session_state.bookings, learner_id, adviser, day, time, note)
                if ok:
                    save()
                    st.session_state.just_booked = msg
                    st.rerun()
                st.error(msg)

        ui.page_header("Find support · no wrong door", "People in your corner,", "when you need them.",
                       "Pick an adviser and a time. You choose the topic.")
        if st.session_state.just_booked:
            ui.md(f'<div class="ss-chip">✓ {st.session_state.just_booked} '
                  f'(Simulated: a confirmation email would be sent.)</div>')
            st.session_state.just_booked = None

        with st.container(border=True):
            ui.section("Your calendar", f"Upcoming conversations · {len(my_bookings)}")
            if not my_bookings:
                st.caption("Nothing booked yet.")
            for i, bk in enumerate(sorted(my_bookings, key=lambda x: (x["date"], x["time"]))):
                a, b = st.columns([6, 1])
                a.markdown(f'**{bk["note"] or "A conversation"}**  \n'
                           f'{bk["date"]:%a %d %b} · {bk["time"]} · with {bk["adviser"]} · ✓ Confirmed')
                if b.button("Cancel", key=f"del{i}"):
                    st.session_state.bookings.remove(bk)
                    save()
                    st.rerun()

        ui.section("Meet the team", "Who can help?")
        colours = ["#F2884B", "#E58BE0", "#E9E4D8"]
        for col, (name, role), colour in zip(st.columns(3), ADVISERS.items(), colours):
            title, focus = role.split(" - ")
            label = opening_label(next_opening(st.session_state.bookings, name))
            with col, st.container(border=True):
                ui.md(f'<div class="ss-avatar" style="background:{colour}">{ui.initials(name)}</div>'
                      f'<div class="ss-adv-name">{name}</div>'
                      f'<div class="ss-adv-role">{title}</div>'
                      f'<div class="ss-adv-focus">{focus.capitalize()}</div>'
                      f'<div class="ss-adv-open"><span style="color:{ui.GREEN}">●</span> Next opening <b>{label}</b></div>')
                if st.button("Book a chat", key=f"book_{name}", use_container_width=True):
                    booking_dialog(name)


# =====================================================================
# ADVISER PAGES
# =====================================================================
elif page == "Learners to check in with":
    ui.page_header("End of Week 3 · day 21", "Learners to", "check in with.",
                   "Each flag is a suggestion with plain reasons. You make the final decision.")
    with st.expander("Rule settings (what-if)"):
        c1, c2 = st.columns(2)
        pct = c1.selectbox("Low activity = bottom X% of course", [10, 15, 20, 25, 30, 35, 40, 45, 50], index=3,
                           format_func=lambda v: f"Bottom {v}%")
        min_ind = c2.selectbox("Flag when at least N indicators are true", [1, 2, 3], index=1,
                               format_func=lambda v: f"{v} of 3 indicators")
    results = rules.apply_rules(features, activity_percentile=pct, min_indicators=min_ind)
    flagged = results[results.flagged].copy()
    reviewed = sum(st.session_state.decisions.get(l, "Not reviewed") != "Not reviewed" for l in flagged.learner_id)

    m1, m2, m3 = st.columns(3)
    m1.metric("Learners", len(results))
    m2.metric("Suggested check-ins", len(flagged))
    m3.metric("Reviewed by you", f"{reviewed} / {len(flagged)}")

    with st.container(border=True):
        ui.section("Suggested check-ins", "Learners the rule flagged, with reasons")
        flagged["decision"] = flagged.learner_id.map(st.session_state.decisions).fillna("Not reviewed")
        ui.table(flagged[["learner_id", "course_code", "indicator_count", "reasons", "decision"]]
                 .rename(columns={"learner_id": "Learner", "course_code": "Course", "indicator_count": "Signs (of 3)",
                                  "reasons": "Reason", "decision": "Your decision"}), height=300)

    with st.container(border=True):
        ui.section("Review a learner", "Check the reasons, then make the decision")
        options = list(flagged.learner_id) or list(results.learner_id)
        pick = st.selectbox("Learner", options, label_visibility="collapsed")
        row = results[results.learner_id == pick].iloc[0]
        ui.table(pd.DataFrame({
            "Indicator": ["Low Canvas activity", "First quiz late / missing", "Late registration"],
            "Value": [f"{row.interactions_to_day21} interactions (percentile {row.activity_percentile})",
                      row.first_quiz_status, f"day {int(row.registration_day)}"],
            "Sign?": ["Yes" if row.low_activity else "No", "Yes" if row.first_quiz_issue else "No",
                      "Yes" if row.late_registration else "No"]}))
        current = st.session_state.decisions.get(pick, "Not reviewed")
        choice = st.radio("Your decision", rules.DECISIONS[1:], horizontal=True, key=f"dec_{pick}",
                          index=rules.DECISIONS[1:].index(current) if current in rules.DECISIONS[1:] else None)
        if st.button("Save decision", type="primary", disabled=choice is None):
            st.session_state.decisions[pick] = choice
            save()
            st.rerun()
        dec = st.session_state.decisions.get(pick, "Not reviewed")
        ui.md(f'Tool suggests: {ui.pill(row.status)} &nbsp;·&nbsp; Your decision: <b>{dec}</b> &nbsp;·&nbsp; '
              f'Student sees: {ui.pill(rules.student_view_status(row, dec))}')
        bks = [b for b in st.session_state.bookings if b["learner_id"] == pick]
        st.caption(f"Booked conversations: {len(bks)}" + "".join(
            f" · {b['date']:%d %b} {b['time']} with {b['adviser']}" for b in bks))

elif page == "Fairness check":
    ui.page_header("Light subgroup check", "Is the flag", "fair across groups?",
                   "Protected attributes are used here only - never in the flag rule.")
    field = st.selectbox("Compare by", FAIRNESS_FIELDS)
    table, overall = flag_rates(results, data["learners"], field)
    with st.container(border=True):
        ui.section("Flag rate by group", f"Overall flag rate: {overall}%")
        bars = alt.Chart(table).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, size=46).encode(
            x=alt.X(field, title=None, axis=alt.Axis(labelAngle=0)), y=alt.Y("flag_rate_%", title="Flag rate (%)"),
            color=alt.Color("result", title=None, legend=alt.Legend(orient="top"),
                            scale=alt.Scale(domain=["OK", "Review", "Too small to judge"],
                                            range=[ui.GREEN, ui.RED, "#C9C3B6"])))
        line = alt.Chart(pd.DataFrame({"y": [overall]})).mark_rule(strokeDash=[4, 4]).encode(y="y")
        ui.chart((bars + line).properties(height=260))
        ui.table(table.rename(columns={field: "Group", "learners": "Learners", "flagged": "Flagged",
                                       "flag_rate_%": "Flag rate %", "gap_vs_overall": "Gap (pts)",
                                       "result": "Result"}))
        st.caption("Review = more than 10 points from the overall rate (dashed line). "
                   "Too small to judge = fewer than 30 learners.")
    if (table.result == "Review").any():
        ui.md('<div class="ss-banner" style="background:#FDEBDD;border-color:#F6CDAE;color:#7A3B12">'
              '<b>A group needs review:</b> find which indicator causes the gap, adjust its threshold '
              'or wording, re-run, and record the change.</div>')

elif page == "How it works":
    ui.page_header("Input → processing → output", "How it", "works.",
                   "Rule-based and explainable: every flag comes with its reasons.")
    diagram = Path(__file__).parent / "steady_step_architecture.png"
    if diagram.exists():
        with st.container(border=True):
            st.image(str(diagram), use_container_width=True)

    with st.container(border=True):
        ui.section("The rule", "Flag for a check-in when 2 or more are true by day 21")
        st.write("1. Low Canvas activity - bottom 25% of the course\n"
                 "2. First quiz late or not submitted\n"
                 "3. Registered after the course started (day 0)")
        st.caption("Never used in the flag: final outcome, data after day 21, gender, age, deprivation, "
                   "accessibility, and the weekly check-in. The adviser makes the final decision.")

    with st.container(border=True):
        tests = run_all()
        ui.section("Test scenarios", f"{int(tests.passed.sum())} of {len(tests)} passed")
        ui.table(tests.assign(passed=tests.passed.map({True: "✓ Pass", False: "✗ Fail"}))
                 [["id", "type", "input", "expected", "actual", "passed"]]
                 .rename(columns={"id": "Test", "type": "Type", "input": "Input", "expected": "Expected",
                                  "actual": "Actual", "passed": "Result"}))

    with st.container(border=True):
        ui.section("Build status", "Working, simulated and planned")
        ui.table(pd.DataFrame({
            "Feature": ["Synthetic dataset, day-21 rule and reasons", "Adviser decisions, fairness check",
                        "Student pages, check-in, booking (saved)", "Login", "Confirmation email",
                        "Real Canvas / student data"],
            "Status": ["Working", "Working", "Working", "Simulated (test accounts)", "Simulated",
                       "Planned"]}))
        if st.button("Reset demo data (clear bookings, decisions, check-ins)"):
            storage.reset_state()
            st.session_state.update(bookings=[], decisions={}, checkins=[])
            st.rerun()
