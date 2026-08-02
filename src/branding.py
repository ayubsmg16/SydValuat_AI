"""SydValuat_AI 'Harbour night' branding.

One shared module injects the theme so all six pages stay coherent:
dark navy canvas, harbour-teal actions, window-light gold accents, and a
different piece of Sydney-skyline artwork on every page.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import streamlit as st

# ------------------------------------------------------------------ palette
NAVY_0 = "#0B1F2A"   # page canvas
NAVY_1 = "#0F2733"   # panels
NAVY_2 = "#123240"   # cards
NAVY_3 = "#16404F"   # raised elements
TEAL = "#1D9E75"     # primary action
TEAL_LT = "#5DCAA5"
TEAL_PALE = "#9FE1CB"
GOLD = "#F5D06B"     # window lights
AMBER = "#EF9F27"
CORAL = "#F0997B"
INK = "#E8F4F0"      # main text
MUTED = "#7FB8A8"    # secondary text

SUBURB_COLORS = {"Mosman": GOLD, "Marrickville": CORAL, "Blacktown": TEAL_LT}

_CSS = f"""
<style>
[data-testid="stMetric"] {{
    background: {NAVY_2};
    border-radius: 0 0 10px 10px;
    padding: 14px 16px;
    border-top: 3px solid var(--sv-accent, {TEAL});
}}
[data-testid="stMetricLabel"] {{ color: {TEAL_PALE}; }}
[data-testid="stMetricDelta"] {{ color: {MUTED}; }}
h1, h2, h3 {{ color: {INK}; }}
[data-testid="stSidebar"] {{
    background: {NAVY_1};
    border-right: 1px solid {NAVY_3};
}}
.stButton > button[kind="primary"], .stFormSubmitButton > button {{
    background: {TEAL}; color: #04342C; border: none; font-weight: 600;
}}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button:hover {{
    background: {TEAL_LT}; color: #04342C;
}}
.stDownloadButton > button {{ border: 1px solid {TEAL}; color: {TEAL_PALE}; }}
[data-testid="stExpander"], .stAlert {{ border-radius: 10px; }}
.sv-banner svg {{ display: block; width: 100%; height: auto; border-radius: 10px; }}
</style>
"""


def accent_line(colors=None, height=4):
    """A flat multi-colour rule, echoing the harbour-dusk accent."""
    colors = colors or [(TEAL, 2), (TEAL_LT, 1), (GOLD, 1)]
    segs = "".join(
        f'<div style="flex:{w};background:{c};"></div>' for c, w in colors)
    return (f'<div style="display:flex;height:{height}px;'
            f'margin:2px 0 18px;border-radius:2px;overflow:hidden;">{segs}</div>')


def _svg(inner, h=86):
    return (f'<div class="sv-banner" style="margin:4px 0 10px;">'
            f'<svg viewBox="0 0 900 {h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="Sydney skyline artwork">'
            f'<rect width="900" height="{h}" fill="{NAVY_1}"/>{inner}</svg></div>')


def _windows(coords):
    return "".join(f'<rect x="{x}" y="{y}" width="5" height="5" fill="{GOLD}"/>'
                   for x, y in coords)


_BANNERS = {
    # Home: full skyline with the bridge arch
    "home": _svg(
        f'<rect x="30" y="30" width="34" height="56" fill="{NAVY_2}"/>'
        f'<rect x="74" y="16" width="26" height="70" fill="{NAVY_3}"/>'
        f'<rect x="110" y="40" width="40" height="46" fill="{NAVY_2}"/>'
        f'<rect x="160" y="24" width="24" height="62" fill="{NAVY_3}"/>'
        f'<path d="M230 86 Q 320 -30 410 86 Z" fill="none" stroke="{TEAL_LT}" stroke-width="4"/>'
        f'<path d="M247 86 Q 320 0 393 86" fill="none" stroke="{TEAL}" stroke-width="2.5"/>'
        f'<rect x="450" y="34" width="30" height="52" fill="{NAVY_2}"/>'
        f'<rect x="490" y="18" width="24" height="68" fill="{NAVY_3}"/>'
        f'<path d="M560 86 L586 40 L612 86 Z" fill="{GOLD}"/>'
        f'<path d="M602 86 L628 32 L654 86 Z" fill="{AMBER}"/>'
        f'<path d="M644 86 L670 40 L696 86 Z" fill="{GOLD}"/>'
        f'<rect x="730" y="26" width="28" height="60" fill="{NAVY_3}"/>'
        f'<rect x="768" y="44" width="36" height="42" fill="{NAVY_2}"/>'
        f'<rect x="820" y="20" width="22" height="66" fill="{NAVY_3}"/>'
        + _windows([(38, 40), (82, 24), (120, 48), (166, 32), (458, 42),
                    (496, 26), (738, 34), (826, 28), (776, 52)])),
    # Single prediction: one house under a teal roof, spotlight on the estimate
    "predict": _svg(
        f'<path d="M330 86 L330 44 L450 8 L570 44 L570 86 Z" fill="{NAVY_2}"/>'
        f'<path d="M318 48 L450 4 L582 48" fill="none" stroke="{TEAL_LT}" stroke-width="7"/>'
        f'<rect x="368" y="52" width="26" height="26" fill="{GOLD}"/>'
        f'<rect x="506" y="52" width="26" height="26" fill="{GOLD}"/>'
        f'<rect x="432" y="46" width="36" height="40" fill="{NAVY_3}"/>'
        f'<circle cx="460" cy="66" r="3" fill="{GOLD}"/>'
        f'<rect x="60" y="52" width="26" height="34" fill="{NAVY_2}"/>'
        f'<rect x="100" y="38" width="20" height="48" fill="{NAVY_3}"/>'
        f'<rect x="780" y="52" width="26" height="34" fill="{NAVY_2}"/>'
        f'<rect x="820" y="38" width="20" height="48" fill="{NAVY_3}"/>'
        + _windows([(66, 58), (104, 44), (786, 58), (824, 44)])),
    # Batch: a terrace row - many properties at once
    "batch": _svg("".join(
        f'<g><path d="M{x} 86 L{x} 42 L{x+55} 20 L{x+110} 42 L{x+110} 86 Z" fill="{NAVY_2 if i % 2 else NAVY_3}"/>'
        f'<path d="M{x-6} 44 L{x+55} 17 L{x+116} 44" fill="none" stroke="{TEAL if i % 2 else TEAL_LT}" stroke-width="5"/>'
        f'<rect x="{x+20}" y="52" width="16" height="16" fill="{GOLD}"/>'
        f'<rect x="{x+72}" y="52" width="16" height="16" fill="{GOLD}"/></g>'
        for i, x in enumerate(range(40, 800, 130)))),
    # Insights: skyline as a bar chart
    "insights": _svg("".join(
        f'<rect x="{x}" y="{86-hgt}" width="46" height="{hgt}" fill="{c}"/>'
        for x, hgt, c in [(80, 26, NAVY_3), (150, 40, TEAL), (220, 34, NAVY_3),
                          (290, 58, TEAL_LT), (360, 44, NAVY_3), (430, 70, GOLD),
                          (500, 52, NAVY_3), (570, 62, TEAL), (640, 38, NAVY_3),
                          (710, 48, TEAL_LT), (780, 30, NAVY_3)])
        + f'<path d="M80 52 L173 38 L313 20 L453 10 L593 16 L733 30 L826 48" '
          f'fill="none" stroke="{AMBER}" stroke-width="3"/>'),
    # Explanation: house with an x-ray grid - seeing inside the model
    "explain": _svg(
        f'<path d="M360 86 L360 40 L450 12 L540 40 L540 86 Z" fill="none" stroke="{TEAL_LT}" stroke-width="3"/>'
        f'<path d="M350 42 L450 8 L550 42" fill="none" stroke="{TEAL}" stroke-width="5"/>'
        f'<line x1="360" y1="58" x2="540" y2="58" stroke="{NAVY_3}" stroke-width="2"/>'
        f'<line x1="360" y1="72" x2="540" y2="72" stroke="{NAVY_3}" stroke-width="2"/>'
        f'<line x1="405" y1="40" x2="405" y2="86" stroke="{NAVY_3}" stroke-width="2"/>'
        f'<line x1="495" y1="40" x2="495" y2="86" stroke="{NAVY_3}" stroke-width="2"/>'
        f'<circle cx="450" cy="60" r="12" fill="{GOLD}"/>'
        f'<rect x="120" y="30" width="120" height="8" rx="4" fill="{TEAL}"/>'
        f'<rect x="120" y="46" width="84" height="8" rx="4" fill="{TEAL_LT}"/>'
        f'<rect x="120" y="62" width="52" height="8" rx="4" fill="{AMBER}"/>'
        f'<rect x="660" y="30" width="120" height="8" rx="4" fill="{TEAL}"/>'
        f'<rect x="660" y="46" width="84" height="8" rx="4" fill="{TEAL_LT}"/>'
        f'<rect x="660" y="62" width="52" height="8" rx="4" fill="{AMBER}"/>'),
    # About: the harbour at night - water and moored lights
    "about": _svg(
        f'<rect x="0" y="60" width="900" height="26" fill="{NAVY_2}"/>'
        f'<path d="M0 60 Q 120 52 240 60 T 480 60 T 720 60 T 900 60" '
        f'fill="none" stroke="{TEAL}" stroke-width="2"/>'
        f'<path d="M200 60 Q 300 -18 400 60" fill="none" stroke="{TEAL_LT}" stroke-width="4"/>'
        f'<rect x="520" y="26" width="24" height="34" fill="{NAVY_3}"/>'
        f'<rect x="556" y="16" width="20" height="44" fill="{NAVY_2}"/>'
        f'<rect x="586" y="32" width="26" height="28" fill="{NAVY_3}"/>'
        f'<path d="M680 60 L700 34 L720 60 Z" fill="{GOLD}"/>'
        f'<path d="M714 60 L734 28 L754 60 Z" fill="{AMBER}"/>'
        + _windows([(526, 32), (562, 22), (592, 38)])
        + "".join(f'<circle cx="{x}" cy="70" r="2" fill="{GOLD}"/>'
                  for x in range(80, 900, 90))),
}

_ACCENTS = {
    "home": [(TEAL, 2), (TEAL_LT, 1), (GOLD, 1)],
    "predict": [(TEAL, 3), (GOLD, 1)],
    "batch": [(TEAL, 1), (TEAL_LT, 1), (TEAL, 1), (GOLD, 1)],
    "insights": [(TEAL_LT, 1), (GOLD, 1), (CORAL, 1), (AMBER, 1)],
    "explain": [(TEAL, 2), (AMBER, 1)],
    "about": [(GOLD, 1), (TEAL_LT, 2), (TEAL, 1)],
}
_METRIC_ACCENT = {"home": TEAL, "predict": GOLD, "batch": TEAL_LT,
                  "insights": AMBER, "explain": TEAL, "about": GOLD}


def apply(page="home", title=None):
    """Inject the theme, the page banner, and (optionally) the page title."""
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(f"<style>:root {{ --sv-accent: {_METRIC_ACCENT.get(page, TEAL)}; }}"
                f"</style>", unsafe_allow_html=True)
    st.markdown(_BANNERS.get(page, _BANNERS["home"]), unsafe_allow_html=True)
    if title:
        st.title(title)
    st.markdown(accent_line(_ACCENTS.get(page)), unsafe_allow_html=True)
    set_chart_theme()


def set_chart_theme():
    """Match matplotlib/seaborn output to the Harbour night palette."""
    mpl.rcParams.update({
        "figure.facecolor": NAVY_1, "savefig.facecolor": NAVY_1,
        "axes.facecolor": NAVY_2, "axes.edgecolor": NAVY_3,
        "axes.labelcolor": INK, "axes.titlecolor": INK,
        "text.color": INK, "xtick.color": TEAL_PALE, "ytick.color": TEAL_PALE,
        "grid.color": NAVY_3, "axes.grid": True, "grid.linewidth": 0.6,
        "legend.facecolor": NAVY_2, "legend.edgecolor": NAVY_3,
        "legend.labelcolor": INK,
    })


def style_fig(fig):
    """Apply the dark canvas to an existing figure (call before st.pyplot)."""
    fig.patch.set_facecolor(NAVY_1)
    for ax in fig.axes:
        ax.set_facecolor(NAVY_2)
        for spine in ax.spines.values():
            spine.set_color(NAVY_3)
    return fig
