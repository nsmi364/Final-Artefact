"""
Steady Step - look and feel (same style as our Report 2 screens, kept simple)
Presentation only: no data processing happens in this file.

One set of rules for every page:
  - page_header()  : small green label + title (green second half) + one-line subtitle
  - card()         : white rounded card for every block of content
  - section()      : small green label + heading inside a page
  - one primary (green) button per screen
"""

import html

import streamlit as st

NAVY, GREEN, CREAM, INK, MUTED, ORANGE, RED = "#252A47", "#2F9E7B", "#F8F5EE", "#1E2235", "#6B6F80", "#F2884B", "#D9534F"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&family=Fraunces:opsz,wght@9..144,600&display=swap');

.stApp {{ background: {CREAM}; color: {INK}; }}
.block-container {{ max-width: 1000px; padding-top: 3rem; }}
[data-testid="stToolbarActions"], [data-testid="stMainMenu"], [data-testid="stAppDeployButton"],
[data-testid="stDecoration"] {{ display: none; }}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {{ background: {NAVY}; }}
section[data-testid="stSidebar"] * {{ color: #D9DBE7; }}
section[data-testid="stSidebar"] .st-key-nav [data-baseweb="radio"] > div:first-child,
section[data-testid="stSidebar"] .st-key-nav [data-testid="stRadioOption"] > div > div:first-child {{ display: none; }}
section[data-testid="stSidebar"] .st-key-nav [data-testid="stRadio"],
section[data-testid="stSidebar"] .st-key-nav [role="radiogroup"] {{ width: 100%; }}
section[data-testid="stSidebar"] .st-key-nav [role="radiogroup"] label {{
  display: flex; width: 100%; box-sizing: border-box; padding: 10px 12px; border-radius: 10px; margin: 2px 0; cursor: pointer; }}
section[data-testid="stSidebar"] .st-key-nav [role="radiogroup"] label:hover {{ background: rgba(255,255,255,.06); }}
section[data-testid="stSidebar"] .st-key-nav [role="radiogroup"] label:has(input:checked) {{
  background: rgba(255,255,255,.10); box-shadow: inset 3px 0 0 {GREEN}; }}
section[data-testid="stSidebar"] .st-key-nav [role="radiogroup"] label:has(input:checked) p {{ color: #fff; font-weight: 600; }}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [role="group"],
section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
  background: rgba(255,255,255,.08) !important; border-color: rgba(255,255,255,.2) !important; }}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] input,
section[data-testid="stSidebar"] [data-testid="stSelectbox"] svg,
section[data-testid="stSidebar"] [data-baseweb="select"] * {{ color: #fff !important; -webkit-text-fill-color: #fff !important; }}
[data-testid="stSidebarCollapseButton"], [data-testid="stSidebarCollapseButton"] button {{ visibility: visible !important; opacity: 1 !important; }}
[data-testid="stSidebarCollapseButton"] svg, [data-testid="stSidebarCollapseButton"] span {{ color: #fff !important; }}
[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"] {{ background: {NAVY}; border-radius: 10px; }}
[data-testid="stExpandSidebarButton"] svg, [data-testid="stExpandSidebarButton"] span {{ color: #fff !important; }}
.ss-logo {{ display:flex; align-items:center; gap:10px; font-weight:700; font-size:1.3rem; color:#fff !important; margin:4px 0 22px; }}
.ss-logo span.box {{ width:32px; height:32px; border-radius:9px; background:{GREEN}; display:inline-flex;
  align-items:center; justify-content:center; box-shadow:3px 3px 0 {ORANGE}; color:#fff !important; }}
.ss-logo b {{ color:{GREEN} !important; }}
.ss-side-label {{ font-family:'DM Mono',monospace; font-size:.7rem; letter-spacing:.14em; color:#8B8FA8 !important; margin:14px 0 4px; }}

/* ---------- page text ---------- */
.ss-eyebrow {{ font-family:'DM Mono',monospace; font-size:.72rem; letter-spacing:.16em; color:{GREEN}; text-transform:uppercase; }}
.ss-title {{ font-size:2.3rem; font-weight:700; line-height:1.12; letter-spacing:-.02em; color:{INK}; margin:4px 0 6px; }}
.ss-title em {{ font-family:'Fraunces',serif; font-style:normal; color:{GREEN}; }}
.ss-sub {{ color:{MUTED}; font-size:1rem; margin-bottom:18px; }}
.ss-h2 {{ font-size:1.2rem; font-weight:600; color:{INK}; margin:2px 0 8px; }}
.ss-muted {{ color:{MUTED}; font-size:.92rem; }}
.ss-mono {{ font-family:'DM Mono',monospace; font-size:.75rem; color:{MUTED}; }}

/* ---------- cards ---------- */
.ss-card {{ background:#FFFDF9; border:1px solid #ECE6DA; border-radius:16px; padding:18px 20px; margin-bottom:14px; }}
.ss-dark {{ background:{NAVY}; border-radius:16px; padding:18px 20px; color:#fff; margin-bottom:14px; }}
.ss-dark * {{ color:#fff; }}
.ss-big {{ font-family:'Fraunces',serif; font-size:3rem; line-height:1; }}
.ss-banner {{ background:#E3F4EC; border:1px solid #BFE3D2; border-radius:16px; padding:14px 18px; margin-bottom:14px; color:#1F5E49; }}
.ss-pill {{ display:inline-block; font-family:'DM Mono',monospace; font-size:.7rem; letter-spacing:.06em;
  padding:4px 10px; border-radius:99px; font-weight:500; }}
.ss-ring {{ width:78px; height:78px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; float:left; margin-right:16px; }}
.ss-ring div {{ width:60px; height:60px; border-radius:50%; background:#FFFDF9; text-align:center; padding-top:10px; }}
.ss-ring b {{ font-family:'Fraunces',serif; font-size:1.35rem; display:block; line-height:1.1; color:{INK}; }}
.ss-ring small {{ font-family:'DM Mono',monospace; font-size:.5rem; color:{MUTED}; }}
.ss-stat small {{ color:{MUTED}; display:block; font-size:.8rem; }}
.ss-stat b {{ font-family:'Fraunces',serif; font-size:1.5rem; color:{INK}; }}
.ss-row {{ display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #EFEAE0; }}
.ss-row:last-child {{ border-bottom:none; }}
.ss-avatar {{ width:52px; height:52px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  font-weight:700; font-family:'DM Mono',monospace; margin-bottom:10px; color:{INK}; }}
.ss-chip {{ display:inline-block; background:#E3F4EC; color:#1F7A5C; border-radius:10px; padding:8px 14px; font-size:.9rem; margin:0 0 14px; }}

/* ---------- equal-height rows ---------- */
.ss-grid {{ display:flex; gap:16px; align-items:stretch; margin-bottom:16px; }}
.ss-grid > div {{ flex:1 1 0; margin:0; }}
.ss-spread {{ display:flex; flex-direction:column; justify-content:space-between; gap:10px; }}
@media (max-width: 760px) {{ .ss-grid {{ flex-direction:column; }} }}
.ss-bubble {{ float:right; width:78px; height:78px; border-radius:50%; background:{GREEN}; text-align:center;
  padding-top:15px; box-shadow:0 0 0 9px rgba(47,158,123,.2); }}
.ss-bubble b {{ font-family:'Fraunces',serif; font-size:1.5rem; display:block; line-height:1; }}
.ss-bubble small {{ font-family:'DM Mono',monospace; font-size:.55rem; letter-spacing:.06em; }}
.ss-bar {{ height:5px; background:rgba(255,255,255,.15); border-radius:9px; margin:18px 0 8px; }}
.ss-bar > div {{ height:5px; background:{GREEN}; border-radius:9px; }}
.ss-tile {{ display:flex; gap:12px; align-items:center; }}
.ss-tile .ic {{ width:38px; height:38px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.05rem; flex:none; }}
.ss-tile small {{ color:{MUTED}; display:block; font-size:.8rem; }}
.ss-tile b {{ font-family:'Fraunces',serif; font-size:1.35rem; color:{INK}; }}

/* ---------- adviser cards (fixed layout so all three match) ---------- */
.ss-adv-name {{ font-weight:700; font-size:1.05rem; color:{INK}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.ss-adv-role {{ color:{INK}; font-size:.9rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.ss-adv-focus {{ color:{MUTED}; font-size:.88rem; line-height:1.4; height:2.8em; overflow:hidden; margin:4px 0 10px;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; }}
.ss-adv-open {{ font-family:'DM Mono',monospace; font-size:.75rem; color:{MUTED}; margin-bottom:12px; white-space:nowrap; }}
.ss-adv-open b {{ color:{INK}; }}

/* ---------- ALWAYS LIGHT: same colours even if the viewer's Streamlit/computer is in dark mode ---------- */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], header[data-testid="stHeader"] {{
  background:{CREAM} !important; color:{INK}; color-scheme: light; }}
header[data-testid="stHeader"] {{ background:transparent !important; }}
[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] [data-testid="stWidgetLabel"], [data-testid="stMain"] [data-testid="stWidgetLabel"] p,
[data-testid="stMain"] [data-testid="stRadioOption"] p, [data-testid="stMain"] [data-testid="stExpander"] summary,
[data-testid="stMain"] [data-testid="stExpander"] summary p, [data-testid="stMain"] [data-testid="stExpander"] svg,
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] p, [data-testid="stMetricValue"],
[role="dialog"], [role="dialog"] p, [role="dialog"] label, [role="dialog"] [data-testid="stMarkdownContainer"] {{ color:{INK}; }}
[data-testid="stMain"] [data-testid="stCaptionContainer"], [data-testid="stMain"] [data-testid="stCaptionContainer"] p,
[role="dialog"] [data-testid="stCaptionContainer"] p {{ color:{MUTED} !important; }}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{ color:#9DA1BC !important; }}
[data-testid="stMain"] [data-testid="stExpander"] details {{ background:#FFFDF9; border-color:#ECE6DA; }}
[data-testid="stMain"] [data-testid="stExpander"] summary:hover p {{ color:{GREEN}; }}

/* inputs (main page and pop-up) */
[data-testid="stMain"] [data-baseweb="select"] > div, [data-testid="stMain"] [data-testid="stSelectbox"] [role="group"],
[role="dialog"] [data-baseweb="select"] > div, [role="dialog"] [data-testid="stSelectbox"] [role="group"],
[data-baseweb="input"], [data-baseweb="input"] > div, [data-baseweb="base-input"], [data-testid="stDateInput"] > div > div,
[data-testid="stTextInputRootElement"], [data-testid="stMain"] input, [role="dialog"] input, [data-testid="stMain"] textarea {{
  background:#FFFFFF !important; border-color:#E2DCCF !important; }}
[data-testid="stMain"] input, [role="dialog"] input, [data-testid="stMain"] textarea,
[data-testid="stMain"] [data-baseweb="select"] *, [role="dialog"] [data-baseweb="select"] *,
[data-testid="stMain"] [data-testid="stSelectbox"] svg, [role="dialog"] [data-testid="stSelectbox"] svg {{
  color:{INK} !important; -webkit-text-fill-color:{INK} !important; }}
[data-testid="stDateInput"] *, [data-testid="stTimeInput"] * {{ color:{INK} !important; -webkit-text-fill-color:{INK} !important; }}
[role="dialog"] button[aria-label="Close"], [role="dialog"] button[aria-label="Close"] svg {{ color:{INK} !important; }}
.stButton > button[kind="primary"] *, .stFormSubmitButton > button[kind="primary"] * {{ color:#fff !important; }}
.stButton > button[kind="secondary"] * {{ color:inherit; }}
input::placeholder, textarea::placeholder {{ color:#9A9AA8 !important; -webkit-text-fill-color:#9A9AA8 !important; }}
[data-baseweb="popover"] ul, [data-baseweb="popover"] li, [role="listbox"], [role="option"],
[data-baseweb="calendar"], [data-baseweb="calendar"] * {{ background-color:#FFFFFF; color:{INK} !important; }}
[role="option"]:hover, [role="option"][aria-selected="true"] {{ background-color:#E3F4EC !important; }}

/* radio buttons + sliders */
[data-testid="stMain"] [data-testid="stRadioOption"] > div > div:first-child,
[data-testid="stMain"] [data-baseweb="radio"] > div:first-child {{ background:#FFFFFF !important; border:2px solid #C9C3B6 !important; }}
[data-testid="stMain"] [data-testid="stRadioOption"]:has(input:checked) > div > div:first-child,
[data-testid="stMain"] [data-baseweb="radio"]:has(input:checked) > div:first-child {{ background:{GREEN} !important; border-color:{GREEN} !important; }}
section[data-testid="stSidebar"] [data-testid="stRadioOption"] > div > div:first-child {{ background:#FFFFFF !important; }}
section[data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked) > div > div:first-child {{ background:{GREEN} !important; }}
[data-testid="stSlider"] [role="slider"] {{ background:{GREEN} !important; }}
[data-testid="stSlider"] [data-testid="stSliderThumbValue"], [data-testid="stSlider"] [data-testid="stSliderTickBarMin"],
[data-testid="stSlider"] [data-testid="stSliderTickBarMax"] {{ color:{INK} !important; }}

/* pop-up box, alerts, metrics */
[role="dialog"] {{ background:{CREAM} !important; }}
[data-testid="stAlertContainer"] {{ background:#FDEBDD !important; color:#7A3B12 !important; }}
[data-testid="stAlertContainer"] * {{ color:#7A3B12 !important; }}

/* our HTML tables */
.ss-table-wrap {{ overflow:auto; border:1px solid #ECE6DA; border-radius:12px; background:#FFFFFF; }}
.ss-table {{ width:100%; border-collapse:collapse; font-size:.88rem; color:{INK}; }}
.ss-table th {{ position:sticky; top:0; background:#F1ECE2; color:{INK}; text-align:left; font-weight:600; padding:8px 10px; }}
.ss-table td {{ padding:8px 10px; border-top:1px solid #EFEAE0; color:{INK}; vertical-align:top; }}

/* ---------- buttons + widgets ---------- */
.stButton > button, .stFormSubmitButton > button {{ border-radius:10px; border:1px solid #E2DCCF; background:#FFFDF9; color:{INK}; font-weight:600; }}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {{ background:{GREEN}; border-color:{GREEN}; color:#fff; }}
.stButton > button:hover {{ border-color:{GREEN}; color:{GREEN}; }}
.stButton > button[kind="primary"]:hover {{ color:#fff; filter:brightness(.95); }}
[class*="st-key-opt"] .stButton > button {{ height:96px; white-space:pre-line; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background:#FFFDF9; border-radius:16px !important; }}
[data-testid="stMetric"] {{ background:#FFFDF9; border:1px solid #ECE6DA; border-radius:16px; padding:12px 16px; }}
</style>
"""

STATUS = {  # status -> (pill text, pill background, pill text colour, ring colour, one-line message)
    "On track": ("ON TRACK", "#E3F4EC", "#1F7A5C", GREEN,
                 "You're showing up steadily. Keep the rhythm going."),
    "Worth keeping an eye on": ("WORTH A LOOK", "#FDEBDD", "#B5541B", ORANGE,
                                "A couple of things are worth a look. Small steps this week can help."),
    "Suggested check-in": ("LET'S CHAT", "#FBE3E3", "#B23A3A", RED,
                           "Your adviser would like a quick chat. It's support, not a penalty."),
}


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def md(text, where=st):
    where.markdown(text, unsafe_allow_html=True)


def sidebar_logo():
    md('<div class="ss-logo"><span class="box">▤</span><span>Steady Step<b>.</b></span></div>', st.sidebar)


def side_label(text, where=st.sidebar):
    md(f'<div class="ss-side-label">{text}</div>', where)


def page_header(eyebrow, plain, green, sub=""):
    """Same header on every page."""
    md(f'<div class="ss-eyebrow">{eyebrow}</div>'
       f'<div class="ss-title">{plain} <em>{green}</em></div>'
       + (f'<div class="ss-sub">{sub}</div>' if sub else '<div style="height:12px"></div>'))


def section(eyebrow, title, where=st):
    md(f'<div class="ss-eyebrow">{eyebrow}</div><div class="ss-h2">{title}</div>', where)


def pill(status):
    text, bg, fg, _, _ = STATUS[status]
    return f'<span class="ss-pill" style="background:{bg};color:{fg}">● {text}</span>'


def ring(signals, status):
    colour = STATUS[status][3]
    deg = int(360 * max(signals, 0.08) / 3)
    return (f'<div class="ss-ring" style="background:conic-gradient({colour} {deg}deg,#EFEAE0 0)">'
            f'<div><b>{signals}/3</b><small>SIGNS</small></div></div>')


def stat(label, value):
    return f'<div class="ss-card ss-stat"><small>{label}</small><b>{html.escape(str(value))}</b></div>'


def grid(*cards):
    """Cards side by side, always the same height and width."""
    md('<div class="ss-grid">' + "".join(cards) + '</div>')


def tile(icon, label, value, bg="#E3F4EC"):
    return (f'<div class="ss-card ss-tile"><div class="ic" style="background:{bg}">{icon}</div>'
            f'<div><small>{label}</small><b>{html.escape(str(value))}</b></div></div>')


def table(df, height=None):
    """Plain HTML table, so it looks the same in light or dark mode."""
    head = "".join(f"<th>{html.escape(str(c))}</th>" for c in df.columns)
    rows = "".join("<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in r) + "</tr>"
                   for r in df.itertuples(index=False))
    style = f' style="max-height:{height}px"' if height else ""
    md(f'<div class="ss-table-wrap"{style}><table class="ss-table"><thead><tr>{head}</tr></thead>'
       f'<tbody>{rows}</tbody></table></div>')


def chart(c):
    """Altair chart with fixed light colours (ignores the viewer's theme)."""
    c = (c.configure(background="transparent", font="DM Sans")
          .configure_axis(labelColor=INK, titleColor=MUTED, gridColor="#E8E2D6", domainColor="#C9C3B6", tickColor="#C9C3B6")
          .configure_legend(labelColor=INK, titleColor=INK)
          .configure_view(strokeWidth=0))
    st.altair_chart(c, use_container_width=True, theme=None)


def initials(name):
    return "".join(p[0] for p in name.split())[:2]
