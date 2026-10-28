# AI-use record: Steady Step (INFOMGMT 399, Group 2, The Big 4)

This record follows the *Presentation and Technical Demo Guide*: tool/model, prompts or conversation export, component supported, what the team changed or checked, and how it was tested. Independently developed and AI-assisted parts are separated in Section 3.

> Items marked **[TO CONFIRM]** must be filled in by the team member who did the work. Do not leave them as written.

---

## 1. Summary

| | |
|---|---|
| **Tools / models** | Replit Agent (Report 2 prototype); Claude, Anthropic (model `claude-opus-5-5`), used through Claude chat with access to the project folder (final demo artefact) |
| **How AI was used** | The team designed the tool (problem, users, checkpoint, indicators, rule, fairness check, screens) in Reports 1 and 2. Claude generated the Python/Streamlit code to that specification, explained it file by file, and revised it each time the team asked for a change. The team reviewed, ran and tested every version and decided what to keep or change. |
| **Conversation export** | `ai_prompts/claude_conversation_2026-10-20_21.pdf` **[TO CONFIRM: export and save]** |
| **Responsibility** | The team remains responsible for all material presented and can explain every component in Q&A. |

---

## 2. Log of material AI use

| # | Date | Tool | Component | What we asked (our input) | What the AI produced | What the team changed / checked | How it was tested |
|---|---|---|---|---|---|---|---|
| 1 | Sept 2026 | Replit Agent | Report 2 prototype UI | One prompt describing our Report 2 dashboard (Report 2, Appendix B) | Clickable student dashboard: Overview, Weekly check-in, My progress, Find support | Replaced in the final artefact. Kept our own design ideas: sidebar menu, 3 named advisers, booking flow, 1–5 check-in, supportive wording | Team role-play walkthrough (Report 2) |
| 2 | 20 Oct 2026 | Claude | `generate_data.py`, `rules.py`, `booking.py`, `scenarios.py`, first `app.py`, tests | Our spec: teaching-team data structure, end-of-Week-3 (day 21) checkpoint, 3 indicators and 2-of-3 rule from Report 2 Appendix H, booking with our 3 advisers | Synthetic data generator, day-21 indicator and flag logic with plain-language reasons, booking validation, test scenarios T1–T3 | Checked the generated fields against the data structure **[TO CONFIRM: who / date]**; confirmed the rule matched our Appendix H | `pytest` (4 tests pass); manual run of every page |
| 3 | 21 Oct 2026 | Claude | Review against the demo guide and marker feedback | Gave Claude the demo guide plus Report 1 and 2 feedback, and asked what the artefact was missing | Gap list: no fairness check in the app; decisions and bookings reset on restart; AI log incomplete | **Team decision:** add the fairness check, and present it as a live in-class demo kept simple | Compared against both rubrics |
| 4 | 21 Oct 2026 | Claude | `fairness.py` (new), simplified `app.py` | Asked for simpler code and a sidebar menu like our Report 2 screens | Flag-rate-by-group check (10-point review rule, groups under 30 marked as too small); plain-Streamlit app with Student / Adviser menus | Chose which pages to keep. Weekly check-in labelled "not used in the flag" in response to Report 2 feedback on self-entered data | App run page by page; 4 tests still pass |
| 5 | 21 Oct 2026 | Claude | `ui.py`, `app.py` restyle, `.streamlit/config.toml` | **Supplied our own Report 2 screenshots as the design template** (Overview, Weekly check-in, result screens, Find support, booking dialog, confirmation) | Styling and page layouts recreating our design in Streamlit | We set the target design, the page flow and the high/low check-in outcomes (low score → "Find an advisor", high score → "See my progress") | Full journey clicked through: check-in → result → booking → confirmation |
| 6 | 21 Oct 2026 | Claude | Sidebar behaviour (`ui.py`, `app.py`) | We found the sidebar could not be reopened, and asked for it to start open on every load | CSS fix for the open/close buttons; script that opens the sidebar on page load | Reported the bug and re-tested on our own laptop | Collapse → reopen, and reload, checked |
| 7 | 21 Oct 2026 | Claude | Flow diagram (`steady_step_flow.png/.dot`) | **We identified a design gap:** "advisers make the final decision", but students were shown the flag before any adviser reviewed it | Flow diagram showing the adviser decision step (Contact / Monitor / No action) | The human-review requirement comes from our Reports 1–2 and the brief; the app was updated to match on 28 Oct (row 9) | Diagram checked against the app and the brief |
| 9 | 28 Oct 2026 | Claude | Final artefact: `app.py`, `ui.py`, `rules.py` (`student_view_status`), `storage.py` (new), `scenarios.py` (T4), architecture diagram | **Tutor feedback that the design was too crowded**; we asked for a simpler, consistent design kept close to our Report 2 look, and for the adviser decision to control what the student sees | Fewer elements per page, one header and card style throughout, one main button per screen; adviser decides in a review panel; bookings, decisions and check-ins saved to `data/app_state.json`; test results and a reset button on the How it works page | Chose to keep our page structure and Report 2 style; consistent spelling "adviser" across the app **[TO CONFIRM: team review of the final design]** | 5 pytest tests pass (incl. T4 adviser decides); full journey run: adviser decides → student sees prompt → check-in → booking → still there after reload |
| 8 | **[TO CONFIRM]** | — | **Our own edits after the AI output** | — | — | List each change a team member made themselves, e.g. changed thresholds, wording, added a feature, fixed a bug | — |

---

## 3. Independently developed vs AI-assisted

| Component | Team's own work (independent) | AI-assisted |
|---|---|---|
| Problem framing, persona "Cassie", empathy map, HMW questions, idea selection | Team (Report 1) | None |
| Design pivot from a Canvas overlay to a standalone dashboard (privacy and feasibility) | Team (Report 2) | None |
| **Early-support checkpoint: end of Week 3 (day 21), after the first quiz** | Team, in response to Report 1 feedback | Coded with AI |
| **3 indicators + 2-of-3 flag rule** | Team (Report 2, Appendix H) | Coded with AI |
| **Fairness rule: flag rate by group, 10-point review** | Team (Report 2, Appendix H) | Coded with AI (`fairness.py`) |
| Protected attributes excluded from the rule, used only for fairness | Team | Coded with AI |
| **Human adviser makes the final decision** | Team (Reports 1–2); gap identified by the team on 21 Oct | Decision column and flow diagram drafted with AI |
| **Screen design**: sidebar menu, Overview, Weekly check-in (1–5), result screens, Find support, 3 advisers, booking dialog, confirmation | Team (Report 2 prototype screens used as the template) | Recreated in Streamlit with AI |
| Supportive, non-labelling wording | Team (Chang, Chen & Lee, 2025) | Applied in code with AI |
| Synthetic data generator, rule code, booking code, Streamlit pages, styling | Specification and review by team | Code generated by AI |
| Testing (T1 normal, T2 boundary, T3 double booking), walkthroughs | Team ran and checked results | Test code drafted by AI |
| **[TO CONFIRM] Our own code changes** | e.g. "Nick changed X in `app.py` because Y" | — |

---

## 4. Checks we ran on AI output

- Synthetic data uses the teaching team's field names, types and allowed values. **[TO CONFIRM: checked by ___ on ___]**
- No data after day 21 and no final outcome is used in the flag (`build_checkpoint_features` filters `activity_day <= 21` and `submission_day <= 21`).
- Every flagged learner has a reason (`test_every_flag_has_a_reason`).
- T1 normal, T2 boundary and T3 double-booking scenarios pass (`python3 -m pytest -v`, 4 passed).
- Fairness check output reviewed for each attribute; groups under 30 learners are not over-interpreted.
- Full student and adviser journeys clicked through on our own laptop before presenting. **[TO CONFIRM]**

## 5. What we would say in Q&A

"We designed the tool and its rules ourselves in Reports 1 and 2: the Week 3 checkpoint, the three indicators, the two-of-three rule, the fairness check, the adviser decision and every screen. We used Claude to turn that design into Streamlit code and to explain it, then we tested it, found problems (like the sidebar, and students seeing a flag before an adviser reviewed it) and directed the fixes. The code was largely AI-generated; the design decisions, testing and iteration were ours."
