[README.md](https://github.com/user-attachments/files/34205108/README.md)
# Steady Step - INFOMGMT 399 Group 2 (The Big 4)

Final artefact for Proposal 2 (Student Dropout Risk). Synthetic data only.

**Main journey:** the rule flags a learner at day 21 with plain reasons → the adviser reviews and decides → if "Contact learner", the student sees a check-in prompt → student does a weekly check-in and books an adviser → saved and visible to both sides.

## Run (Mac: python3)
```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Data is built automatically on first run. Tests: `pip install pytest`, then `python3 -m pytest -v`.

## What each file does
| File | Role |
|---|---|
| generate_data.py | Synthetic dataset from the teaching team's data structure |
| rules.py | Day-21 features -> 3 indicators -> flag + plain-language reason; `student_view_status` = adviser decides what the student sees |
| booking.py | Booking validation (no double booking) |
| storage.py | Saves bookings, adviser decisions and check-ins to data/app_state.json |
| fairness.py | Flag rate by group vs overall (10-point review rule) |
| scenarios.py | Tests T1 normal, T2 boundary, T3 double booking, T4 adviser decides (used by pytest and the How it works page) |
| app.py | Side menu - Student: Overview, Weekly check-in (3 questions, 1-5), My progress, Find support (book an adviser + confirmation). Adviser: Learners to check in with (review + decide), Fairness check, How it works (diagram, rule, test results, reset demo data) |
| ui.py | Look and feel only (Report 2 style: navy side menu, cream cards, green headings) |
| steady_step_architecture.png / .dot | Architecture diagram (edit the .dot, then run `dot -Tpng`) |

**Before presenting:** open How it works → *Reset demo data* so no old bookings or decisions show.
