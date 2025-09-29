#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import ast
from collections import Counter
import re
import math
from pathlib import Path
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import unicodedata
import streamlit.components.v1 as components


# --------------------------
# Page config (wide layout)
# --------------------------
st.set_page_config(
    layout="wide",
    page_title="Lazeo: Overall Dashboard "
)

# --------------------------
# Apply dark theme with CSS
# --------------------------

st.markdown(
    """
    <style>
    /* ---------- Base page colors ---------- */
    html, body, .stApp, .main, .block-container {
        background-color: #000000 !important;
        color: #E0E0E0 !important;
        font-family: "Inter","Helvetica Neue",Arial,sans-serif !important;
    }

    /* Titles and headers */
    h1, h2, h3 { color: #76ff03 !important; }
    h4, h5, h6, p, span, li, a, label, div { color: #E0E0E0 !important; }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background-color: #0b0b0b !important;
        color: #E0E0E0 !important;
        border-right: 1px solid #111 !important;
    }
    section[data-testid="stSidebar"] * { color: #E0E0E0 !important; }
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700;
    }

    /* Sidebar widgets */
    section[data-testid="stSidebar"] div[role="combobox"],
    section[data-testid="stSidebar"] div[role="listbox"],
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] .stNumberInput,
    section[data-testid="stSidebar"] .stTextInput,
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stMultiSelect {
        background: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 6px !important;
    }

    /* Tags for selected cities */
    section[data-testid="stSidebar"] div[data-baseweb="tag"] {
        background-color: #c62828 !important;  /* 🔴 red background */
        color: #FFFFFF !important;             /* ⚪ white text */
        border-radius: 4px !important;
        padding: 2px 6px !important;
        font-weight: 600 !important;
    }


    /* Dropdown menu */
    section[data-testid="stSidebar"] div[data-baseweb="popover"],
    section[data-testid="stSidebar"] li {
        background-color: #111111 !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] li:hover {
        background-color: #333333 !important;
    }

    /* Sidebar sliders */
    section[data-testid="stSidebar"] .stSlider .rc-slider-track,
    section[data-testid="stSidebar"] .stSlider .rc-slider-rail,
    section[data-testid="stSidebar"] .stSlider .rc-slider-handle {
        background: #222 !important;
        border-color: #444 !important;
    }
    

    /* ---------- Tabs ---------- */
    button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #29b6f6 !important;   /* cyan-blue */
        margin: 6px 18px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #111111 !important;
        border-bottom: 3px solid #29b6f6 !important;
    }
    button[data-baseweb="tab"]:hover {
        background-color: #222222 !important;
    }

    /* ---------- Dataframes / Tables ---------- */
    div[data-testid="stDataFrame"] table, .stTable table {
        width: 100% !important;
        border-collapse: collapse !important;
    }
    div[data-testid="stDataFrame"] table thead th,
    .stTable thead th {
        background-color: #222222 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-align: left !important;
        padding: 10px !important;
        position: sticky;
        top: 0;
        z-index: 2;
    }
    div[data-testid="stDataFrame"] table tbody td,
    .stTable tbody td {
        background-color: #0b0b0b !important;
        color: #E0E0E0 !important;
        font-size: 14px !important;
        padding: 8px !important;
    }
    div[data-testid="stDataFrame"] table tbody th {
        background-color: #0b0b0b !important;
        color: #cfcfcf !important;
        font-size: 14px !important;
        padding: 8px !important;
    }

    /* ---------- Plotly / Charts ---------- */
    div[data-testid="stPlotlyChart"], .stPlotlyChart > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stPlotlyChart"] iframe,
    div[data-testid="stPlotlyChart"] canvas {
        background: transparent !important;
        border: none !important;
    }

    /* ---------- Negative Points Expander ---------- */
    details[open] summary {
        background-color: #3b0b0b !important;
        color: #ff8a80 !important;
        border-radius: 6px;
        padding: 6px;
    }
    details summary {
        background-color: #1a0000 !important;
        color: #ff5252 !important;
        border-radius: 6px;
        padding: 6px;
        font-weight: 600;
        cursor: pointer;
    }

    /* ---------- Buttons ---------- */
    .stButton>button, button.k-Button {
        background-color: #222 !important;
        color: #E0E0E0 !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
    }

    /* ---------- Misc ---------- */
    hr { border: 1px solid #444; }
    code, pre { background: #0b0b0b !important; color: #e0e0e0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# st.markdown(
#     """
#     <style>
#     /* Force sidebar widgets dark background */
#     section[data-testid="stSidebar"] .stMultiSelect,
#     section[data-testid="stSidebar"] .stSelectbox,
#     section[data-testid="stSidebar"] .stSlider {
#         background-color: #111111 !important;
#         color: #FFFFFF !important;
#     }

#     /* Multiselect box (selected values container) */
#     section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
#         background-color: #111111 !important;
#         color: #FFFFFF !important;
#     }

#     /* Tags for selected cities */
#     section[data-testid="stSidebar"] div[data-baseweb="tag"] {
#         background-color: #222222 !important;
#         color: #FFFFFF !important;
#         border-radius: 4px !important;
#         padding: 2px 6px !important;
#     }

#     /* Dropdown menu */
#     section[data-testid="stSidebar"] div[data-baseweb="popover"] {
#         background-color: #111111 !important;
#         color: #FFFFFF !important;
#         border: 1px solid #333 !important;
#     }

#     /* Dropdown options */
#     section[data-testid="stSidebar"] li {
#         background-color: #111111 !important;
#         color: #FFFFFF !important;
#     }
#     section[data-testid="stSidebar"] li:hover {
#         background-color: #333333 !important;
#     }

#     /* Slider track + handle */
#     section[data-testid="stSidebar"] .stSlider > div[data-baseweb="slider"] {
#         background-color: #111111 !important;
#     }
#     section[data-testid="stSidebar"] .stSlider span {
#         color: #FFFFFF !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# st.markdown(
#     """
#     <style>
#     /* Fix Streamlit selectbox & dropdown styling */
#     div[data-baseweb="select"] {
#         background-color: #111111 !important;   /* dark background */
#         color: #FFFFFF !important;              /* white text */
#         border: 1px solid #444 !important;
#         border-radius: 6px !important;
#         font-size: 18px !important;
#     }

#     /* Selected value inside the selectbox */
#     div[data-baseweb="select"] > div {
#         color: #FFFFFF !important;
#         background-color: #111111 !important;
#     }

#     /* Dropdown menu options */
#     ul[role="listbox"] {
#         background-color: #111111 !important;
#         color: #FFFFFF !important;
#         font-size: 18px !important;
#     }

#     ul[role="listbox"] li {
#         background-color: #111111 !important;
#         color: #FFFFFF !important;
#         padding: 8px !important;
#     }
#     ul[role="listbox"] li:hover {
#         background-color: #333333 !important;
#         color: #76ff03 !important;  /* highlight hover */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


# --------------------------
# Header with logo + styled title
# --------------------------
logo_path = Path("lazeo_logo.png")  # ensure logo file is in same folder


st.markdown(
    """
    <div style='padding:8px 12px; text-align:left;'>
        <div style='display:block;'>
            <h1 style='font-size:48px; color:#76ff03; margin:0; line-height:1.2; font-weight:700;'>
                Lazeo France
            </h1>
        </div>
        <div style='display:block;'>
            <p style='color:#E0E0E0; margin:10px 0 0 0; font-size:28px; font-weight:700;'>
                Customer Reviews Dashboard
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='margin-top:8px; margin-bottom:18px;'>", unsafe_allow_html=True)


# # --------------------------
# # Fix Streamlit top bar background
# # --------------------------
# st.markdown(
#     """
#     <style>
#     /* Streamlit top menu/header bar */
#     header[data-testid="stHeader"] {
#         background: #000000 !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <style>
#     /* Fix selectbox dropdown text for main area */
#     div[data-testid="stSelectbox"] div[role="combobox"] {
#         background-color: #111111 !important;
#         color: #FFFFFF !important;
#         font-size: 16px !important;
#         border: 1px solid #444 !important;
#     }

#     div[data-testid="stSelectbox"] option,
#     div[data-testid="stSelectbox"] select {
#         background-color: #111111 !important;
#         color: #FFFFFF !important;
#         font-size: 16px !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )




# --------------------------
# Load CSVs
# --------------------------
CSV_PATH = "store_level_overall_insights.csv"
REVIEWS_CSV = "all_lazeo_reviews.csv"
NEGATIVE_CSV = "negative_points_final2.csv"

@st.cache_data
def load_reviews(path):
    return pd.read_csv(path)

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    if "lat" in df.columns and "lng" in df.columns:
        df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
        df["lng"] = pd.to_numeric(df["lng"], errors="coerce")
    elif "location" in df.columns:
        def parse_loc(val):
            try:
                d = ast.literal_eval(val) if isinstance(val, str) else val
                return d.get("lat"), d.get("lng")
            except Exception: return None, None
        latlng = df["location"].apply(parse_loc)
        df["lat"], df["lng"] = [p[0] for p in latlng], [p[1] for p in latlng]
    else:
        st.error("CSV must contain either `lat`/`lng` or `location` column.")
        return pd.DataFrame([])
    return df.dropna(subset=["lat","lng"]).reset_index(drop=True)

df = load_data(CSV_PATH)
reviews_df = load_reviews(REVIEWS_CSV)
neg_df = load_reviews(NEGATIVE_CSV)

# --------------------------
# Sidebar filters
# --------------------------
with st.sidebar:
    logo_path = Path("lazeo_logo.png")
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown("<div style='font-weight:700; font-size:26px; color:#29b6f6;'>Lazeo</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("Filters")
    min_reviews = st.slider("Minimum reviews", 0, int(df["reviewsCount"].max()), 0)
    cities = sorted(df["city"].dropna().unique().tolist())
    city_filter = st.multiselect("City", options=cities, default=cities)
    score_min, score_max = st.slider("Score range", 0.0, 5.0, (0.0, 5.0), step=0.1)

filtered = df[(df["reviewsCount"] >= min_reviews) & (df["totalScore"].between(score_min, score_max))]
if city_filter:
    filtered = filtered[filtered["city"].isin(city_filter)]
filtered = filtered.reset_index(drop=True)

# --------------------------
# Helpers & parsing utils
# --------------------------
_count_re = re.compile(r'^(.*?)\s*\((\d+)\)\s*$')
to_remove = {'aspect', 'count', 'actionable', 'action', 'point'}

def parse_negatives(neg_str):
    out = []
    for n in str(neg_str).split(";"):
        n = n.strip()
        if not n: continue
        base = n.split("->")[0].strip()
        count = 1
        if "(" in base:
            try: count = int(base.split("(")[1].split(")")[0])
            except Exception: count = 1
            base = base.split("(")[0].strip()
        out.append((base, count))
    return out

def parse_phrase_count_list(phrase_str):
    out = []
    for p in str(phrase_str).split(";"):
        p = p.strip()
        if not p: continue
        m = _count_re.match(p)
        if m: phrase, cnt = m.group(1).strip(), int(m.group(2))
        else: phrase, cnt = p.split("(")[0].strip(), 1
        out.append((phrase, cnt))
    return out

def parse_staff_list(staff_str):
    out = []
    for s in str(staff_str).split(";"):
        s = s.strip()
        if s:
            m = re.match(r"^(.*?)\s*\((\d+)\)$", s)
            if m: out.append(m.group(1).strip())
            else: out.append(s)
    return out

def sentence_case(text):
    text = str(text).strip()
    if not text: return text
    return text[0].upper() + text[1:].lower()

def _norm(s):
    try:
        s = str(s).strip().lower()
        s = unicodedata.normalize("NFKD", s)
        s = "".join([c for c in s if not unicodedata.combining(c)])
        return re.sub(r'\s+', ' ', s)
    except Exception: return ""

def safe_key(s):
    return re.sub(r'\W+', '_', str(s))


def render_styled_table_with_scroll(styler, height=360,font_family='"Inter", "Helvetica Neue", Arial, sans-serif'):
    html_table = styler.to_html()
    wrapper = f"""
    <div style="width:100%; box-sizing:border-box; padding:6px; background:#000; font-family:{font_family};">
      <style>
        table {{ width: 100% !important; table-layout: auto !important; border-collapse: collapse;font-family: {font_family} !important; }}
        table thead th {{ background: #111 !important; color: #fff !important; text-align: left !important; font-size: 24px !important; padding: 10px !important; position: sticky; top: 0; z-index: 2; }}
        table tbody td {{ background: #0b0b0b !important; color: #e0e0e0 !important; padding: 8px !important; vertical-align: middle; white-space: normal !important; word-wrap: break-word; font-size: 20px !important; font-family: {font_family} !important; }}
        table tbody th {{ background: #0b0b0b !important; color: #cfcfcf !important; padding: 8px !important; font-family: {font_family} !important; }}
        .table-scroll-wrapper {{ height: {height}px; overflow: auto; border: 1px solid #222; border-radius: 6px; padding: 6px; box-sizing: border-box; background:#000; }}
        table tbody tr:nth-child(even) td {{ background: #0f0f0f !important; }}
      </style>
      <div class="table-scroll-wrapper">{html_table}</div>
    </div>
    """
    components.html(wrapper, height=height + 24, scrolling=True)

# --------------------------
# Initialize Session State for All Tabs
# --------------------------
if 'store_2_selection' not in st.session_state:
    st.session_state.store_2_selection = None
if 'store_a_selection' not in st.session_state:
    st.session_state.store_a_selection = "-- Select --"
if 'store_b_selection' not in st.session_state:
    st.session_state.store_b_selection = "-- Select --"

# --------------------------
# Tabs: Country vs Store vs Comparison
# --------------------------
tab1, tab2 = st.tabs(["🌍 Country Level Stats", "🏬 Store Level Stats"])

with tab1:
    st.header("Country Level Reviews Summary")
    if not filtered.empty:
        total_reviews = int(filtered["reviewsCount"].sum())
        avg_score = round(filtered["totalScore"].mean(), 2)
        positives_counter = Counter()
        negatives_counter = Counter()

        for pts in filtered["positive_points"].dropna():
            for p in pts.split(";"):
                s = p.strip()
                if not s: continue
                m = _count_re.match(s)
                if m: name, cnt = m.group(1).strip(), int(m.group(2))
                else: name, cnt = s.split("(")[0].strip(), 1
                if name: positives_counter[sentence_case(name)] += cnt

        for pts in filtered["negative_points"].dropna():
            for p in pts.split(";"):
                s = p.strip()
                if not s: continue
                left = s.split("->")[0].strip()
                m = _count_re.match(left)
                if m: name, cnt = m.group(1).strip(), int(m.group(2))
                else: name, cnt = left.split("(")[0].strip(), 1
                if not name or name.lower() in to_remove: continue
                negatives_counter[sentence_case(name)] += cnt

        most_common_pos = ", ".join([f"{p} ({c})" for p, c in positives_counter.most_common(5)])

 
        most_common_neg = ", ".join([f"{n} ({c})" for n, c in negatives_counter.most_common(5)])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div style='background:#111111; padding:20px; border-radius:12px; text-align:center; box-shadow: 2px 2px 8px rgba(0,0,0,0.6);'>
                    <div style='font-size:18px; font-weight:600; color:#76ff03;'>🏥 Total Stores Scraped</div>
                    <div style='font-size:28px; font-weight:700; color:#29b6f6;'>{len(filtered)}</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div style='background:#111111; padding:20px; border-radius:12px; text-align:center; box-shadow: 2px 2px 8px rgba(0,0,0,0.6);'>
                    <div style='font-size:18px; font-weight:600; color:#29b6f6;'>📝 Total Reviews</div>
                    <div style='font-size:28px; font-weight:700; color:#76ff03;'>{total_reviews}</div></div>""", unsafe_allow_html=True)
        with col3:
            score_color = "#76ff03" if avg_score >= 4.5 else "#ff9800" if avg_score >= 3.5 else "#f44336"
            st.markdown(f"""<div style='background:#111111; padding:20px; border-radius:12px; text-align:center; box-shadow: 2px 2px 8px rgba(0,0,0,0.6);'>
                    <div style='font-size:18px; font-weight:600; color:#29b6f6;'>⭐ Average Rating</div>
                    <div style='font-size:28px; font-weight:700; color:{score_color};'>{avg_score}</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
        if most_common_pos:
            st.markdown(f"""
                <div style='background:#0b3b0b; padding:15px; border-radius:10px; 
                            box-shadow:1px 1px 6px rgba(0,0,0,0.6); margin-bottom:15px;'>
                    <div style='font-size:18px; font-weight:600; color:#ffffff; margin-bottom:8px;'>
                        ✅ Most Common Positive Points
                    </div>
                    <div style='font-size:16px; color:#ffffff;'>{most_common_pos}</div>
                </div>
                """, unsafe_allow_html=True)
        
        if most_common_neg:
            st.markdown(f"""
                <div style='background:#3b0b0b; padding:15px; border-radius:10px; 
                            box-shadow:1px 1px 6px rgba(0,0,0,0.6); margin-bottom:15px;'>
                    <div style='font-size:18px; font-weight:600; color:#ffffff; margin-bottom:8px;'>
                        ❌ Most Common Negative Points
                    </div>
                    <div style='font-size:16px; color:#ffffff;'>{most_common_neg}</div>
                </div>
                """, unsafe_allow_html=True)

        # if most_common_pos:
        #     st.markdown(f"""<div style='background:#111111; padding:15px; border-radius:10px; box-shadow:1px 1px 6px rgba(0,0,0,0.6); margin-bottom:15px;'>
        #             <div style='font-size:18px; font-weight:600; color:#76ff03; margin-bottom:8px;'>✅ Most Common Positive Points</div>
        #             <div style='font-size:16px; color:#a5d6a7;'>{most_common_pos}</div></div>""", unsafe_allow_html=True)
        # if most_common_neg:
        #     st.markdown(f"""<div style='background:#111111; padding:15px; border-radius:10px; box-shadow:1px 1px 6px rgba(0,0,0,0.6); margin-bottom:15px;'>
        #             <div style='font-size:18px; font-weight:600; color:#f44336; margin-bottom:8px;'>❌ Most Common Negative Points</div>
        #             <div style='font-size:16px; color:#ef9a9a;'>{most_common_neg}</div></div>""", unsafe_allow_html=True)

        st.subheader("⭐ Overall Star Distribution (All Stores Shown)")
        star_totals = {
            "5★": filtered["5_star"].sum() if "5_star" in filtered.columns else 0,
            "4★": filtered["4_star"].sum() if "4_star" in filtered.columns else 0,
            "3★": filtered["3_star"].sum() if "3_star" in filtered.columns else 0,
            "2★": filtered["2_star"].sum() if "2_star" in filtered.columns else 0,
            "1★": filtered["1_star"].sum() if "1_star" in filtered.columns else 0,
        }
        fig_country = go.Figure(go.Bar(x=list(star_totals.keys()), y=list(star_totals.values()), marker_color=["green","lightgreen","orange","red","darkred"]))
        fig_country.update_layout(template="plotly_dark", plot_bgcolor="black", paper_bgcolor="black", font=dict(color="white"),    xaxis=dict(
        title="Stars",
        showgrid=False,   # 🔴 Remove vertical gridlines
        zeroline=False,
        linecolor="#444"  # keep axis line
    ),
    yaxis=dict(
        title="Count",
        showgrid=False,   # 🔴 Remove horizontal gridlines
        zeroline=False,
        linecolor="#444"  # keep axis line
    ),
    margin=dict(t=40, b=60, l=60, r=40),
    height=380
)
        st.plotly_chart(fig_country, use_container_width=True, height=300)

        st.subheader("🏆 Store Ranking")
        ranking = filtered.sort_values(by=["totalScore", "reviewsCount"], ascending=[False, False])[["title", "city", "totalScore", "reviewsCount"]]
        ranking.columns = ["Store Name", "City", "Ratings", "ReviewsCount"]
        styled_rank = ranking.style.set_table_styles([])
        render_styled_table_with_scroll(styled_rank, height=400)

        st.subheader("👩‍⚕️ Staff Mentions Leaderboard (Overall)")
        staff_liked_records = []
        staff_disliked_records = []
        for _, row in filtered.iterrows():
            store = row["title"]
            for s in str(row.get("staff_liked", "")).split(";"):
                s = s.strip()
                if s:
                    match = re.match(r"^(.*?)\s*\((\d+)\)$", s)
                    if match: name, count = match.group(1).strip(), int(match.group(2))
                    else: name, count = s, 1
                    staff_liked_records.append((name, store, count))
            for s in str(row.get("staff_disliked", "")).split(";"):
                s = s.strip()
                if not s: continue
                match = re.match(r"^(.*?)\s*\((\d+)\)$", s)
                if match: name, count = match.group(1).strip(), int(match.group(2))
                else: name, count = s, 1
                if any(kw in name.lower() for kw in ["no specific", "unnamed", "unspecified", "none"]): continue
                staff_disliked_records.append((name, store, count))

        df_liked = (pd.DataFrame(staff_liked_records, columns=["Staff", "Store", "Mentions"])
                    .groupby(["Staff", "Store"], as_index=False)["Mentions"].sum().sort_values("Mentions", ascending=False))
        df_disliked = (pd.DataFrame(staff_disliked_records, columns=["Staff", "Store", "Mentions"])
                       .groupby(["Staff", "Store"], as_index=False)["Mentions"].sum().sort_values("Mentions", ascending=False))

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**💙 Most Praised Staff (by Store)**")
            if not df_liked.empty:
                styled_pos_staff = df_liked.head(10).style.set_table_styles([])
                render_styled_table_with_scroll(styled_pos_staff, height=400)
        with c2:
            st.markdown("**⚠️ Most Criticized Staff (by Store)**")
            if not df_disliked.empty:
                styled_neg_staff = df_disliked.head(10).style.set_table_styles([])
                render_styled_table_with_scroll(styled_neg_staff, height=400)

with tab2:
    st.header("Store Level Reviews Summary")

    # --- The render function is defined first, so it's available later ---
    def render_star_chart_and_reviews(row, reviews_df_local):
        # Build store_reviews robustly
        store_reviews = pd.DataFrame()
        if not reviews_df_local.empty:
            target = _norm(row.get("title", ""))
            candidate_cols = [c for c in ["title", "store_name", "place_name", "google_place_id"] if c in reviews_df_local.columns]
            for col in candidate_cols:
                try:
                    left = reviews_df_local[col].astype(str).apply(_norm)
                    matched = reviews_df_local[left == target]
                    if not matched.empty:
                        store_reviews = matched.copy()
                        break
                except Exception:
                    pass
            if store_reviews.empty and "title" in reviews_df_local.columns:
                try:
                    left = reviews_df_local["title"].astype(str).apply(_norm)
                    matched = reviews_df_local[left.str.contains(target, na=False)]
                    if not matched.empty:
                        store_reviews = matched.copy()
                except Exception:
                    pass
    
        # Normalize stars
        if not store_reviews.empty and "stars" in store_reviews.columns:
            store_reviews["stars"] = pd.to_numeric(store_reviews["stars"], errors="coerce").fillna(0).astype(int)
        else:
            store_reviews["stars"] = pd.Series(dtype=int)
    
        # star counts
        star_counts = store_reviews["stars"].value_counts().reindex([5,4,3,2,1], fill_value=0).astype(int)
    
        # fallback to aggregated row counts if reviews missing
        if int(star_counts.sum()) == 0:
            if any(c in row.index for c in ["5_star", "4_star", "3_star", "2_star", "1_star"]):
                def _get_agg(col):
                    try:
                        return int(pd.to_numeric(row.get(col, 0), errors="coerce") or 0)
                    except Exception:
                        return 0
                star_counts = pd.Series({
                    5: _get_agg("5_star"),
                    4: _get_agg("4_star"),
                    3: _get_agg("3_star"),
                    2: _get_agg("2_star"),
                    1: _get_agg("1_star"),
                }).reindex([5,4,3,2,1], fill_value=0).astype(int)
    
        # Prepare bar chart
        ordered = [5,4,3,2,1]
        x_vals = [f"{s}★" for s in ordered]
        y_vals = [int(star_counts.get(s,0)) for s in ordered]
    
        colors = {"5★":"green","4★":"lightgreen","3★":"orange","2★":"red","1★":"darkred"}
        bar_colors = [colors.get(x, "grey") for x in x_vals]
    
        y_max = max(3, int(max(y_vals) * 1.15)) if len(y_vals) > 0 else 3
    
        fig = go.Figure(
            data=[go.Bar(
                x=x_vals,
                y=y_vals,
                text=y_vals,
                textposition="outside",
                textfont=dict(color="#FFFFFF", size=12),
                marker=dict(color=bar_colors, line=dict(width=0, color="#000000")),
                hovertemplate="%{x}<br>Count: %{y}<extra></extra>"
            )]
        )
        fig.update_layout(
            showlegend=False,
            autosize=True,
            height=380,
            margin=dict(t=40, b=80, l=60, r=40),
            plot_bgcolor="#000000",
            paper_bgcolor="#000000",
            font=dict(color="#FFFFFF", family="Inter, Helvetica, Arial, sans-serif"),
            xaxis=dict(title="Stars", tickfont=dict(size=14, color="#FFFFFF"), showline=True, linecolor="#444", showgrid=False),
            yaxis=dict(title="Count", tickfont=dict(size=14, color="#FFFFFF"), showline=True, linecolor="#444", showgrid=False, range=[0, y_max]),
            bargap=0.25
        )
    
        # Capture click events
        try:
            selected = plotly_events(fig, click_event=True, select_event=False,
                                     override_height=380, override_width="100%",
                                     key=safe_key(f"star_click_{row.get('title','')}"))
        except Exception:
            #st.plotly_chart(fig, width="stretch", height=420)
            st.plotly_chart(fig, use_container_width=True, height=420)

            selected = None
    
        if selected is None:
            #st.plotly_chart(fig, width="stretch", height=420)
            st.plotly_chart(fig, use_container_width=True, height=420)

    
        # --- Show reviews ---
        # Default = 5★ if no click
        if selected and len(selected) > 0:
            clicked_x = selected[0].get("x")
            try:
                star_num = int(str(clicked_x).replace("★", ""))
            except Exception:
                star_num = 5  # fallback to 5★
        else:
            star_num = 5  # default
    
        st.subheader(f"{star_num}★ Reviews — {row.get('title','')}")
    
        if "stars" in store_reviews.columns:
            star_reviews = store_reviews[store_reviews["stars"] == star_num].copy()
        else:
            star_reviews = pd.DataFrame()
    
        if star_reviews.empty:
            st.info(f"No {star_num}★ reviews found for this store.")
        else:
            time_cols = [c for c in ["publishedAtDate","created_at","published_at","date"] if c in star_reviews.columns]
            if time_cols:
                try:
                    tc = time_cols[0]
                    star_reviews[tc] = pd.to_datetime(star_reviews[tc], errors="coerce")
                    star_reviews = star_reviews.sort_values(tc, ascending=False)
                except Exception:
                    pass
    
            max_to_show = min(50, len(star_reviews))
            n = st.slider("Number of reviews to display", 1, max_to_show, min(5, max_to_show),
                          key=safe_key(f"rev_slider_{row.get('title','')}_{star_num}"))
            for _, r in star_reviews.head(n).iterrows():
                time_str = ""
                for tcol in ["publishedAtDate","created_at","published_at","date"]:
                    if tcol in r.index and pd.notna(r[tcol]):
                        time_str = str(r[tcol]); break
                st.markdown(
                    f"<div style='background:#111111; padding:10px; margin:6px 0; border-radius:8px; color:#e0e0e0;'>"
                    f"<b>{time_str}</b><br>{r.get('textTranslated', r.get('text', '—'))}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # --- Main layout for Tab 2 ---
    left_col, right_col = st.columns([2, 1.5])
    map_output = None

    with left_col:
        st.subheader("France Map — click a bubble to view insights")
        if filtered.empty:
            st.error("No rows to plot after filtering.")
        else:
            m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="CartoDB positron")
            try:
                folium.GeoJson("https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson", name="Regions", style_function=lambda x: {"color": "black", "weight": 1, "fillOpacity": 0.03}).add_to(m)
            except Exception: pass
            max_reviews = filtered["reviewsCount"].max() or 1
            def score_color(score):
                try: s = float(score)
                except Exception: s = 0.0
                if s >= 4.5: return "green"
                elif s >= 4.0: return "orange"
                else: return "red"
            for _, row in filtered.iterrows():
                radius = 6 + (row["reviewsCount"]/max_reviews) * 12
                folium.CircleMarker(location=[row["lat"], row["lng"]], radius=radius, color=score_color(row["totalScore"]), fill=True, fill_color=score_color(row["totalScore"]), fill_opacity=0.8, tooltip=f"{row['title']} — ⭐ {row['totalScore']} ({row['reviewsCount']} reviews)", popup=row["title"]).add_to(m)
# Replace your existing legend_html with this dark-styled legend
            legend_html = """
            <div class="map-legend" style="
                position: fixed;
                bottom: 50px;
                left: 50px;
                width: 190px;
                background-color: rgba(0,0,0,0.75);
                color: #ffffff;
                border: 1px solid #444;
                z-index:9999;
                font-size:13px;
                padding: 10px;
                border-radius:8px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.5);
            ">
              <div style="font-weight:700; margin-bottom:6px; color:#ffffff;">Legend</div>
              <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span style="display:inline-block; width:14px; height:14px; background:green; border-radius:2px; border:1px solid rgba(255,255,255,0.05);"></span>
                <span style="color:#ffffff; font-size:12px;">High (≥4.5)</span>
              </div>
              <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span style="display:inline-block; width:14px; height:14px; background:orange; border-radius:2px; border:1px solid rgba(255,255,255,0.05);"></span>
                <span style="color:#ffffff; font-size:12px;">Medium (4.0–4.4)</span>
              </div>
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="display:inline-block; width:14px; height:14px; background:red; border-radius:2px; border:1px solid rgba(255,255,255,0.05);"></span>
                <span style="color:#ffffff; font-size:12px;">Low (&lt;4.0)</span>
              </div>
            </div>
            """
            m.get_root().html.add_child(folium.Element(legend_html))
            #m.get_root().html.add_child(folium.Element(legend_html))
            map_output = st_folium(m, width="100%", height=420)

        st.markdown("<hr/>", unsafe_allow_html=True)
        st.subheader("Star Distribution (click a bar to view reviews)")
        star_container = st.container()

    with right_col:
        st.subheader("Selected Store")
        store_options = filtered["title"].tolist() if not filtered.empty else []

        selected_store_name = None
        if map_output and map_output.get("last_object_clicked_popup"):
            selected_store_name = map_output["last_object_clicked_popup"]
            st.session_state.store_2_selection = selected_store_name
        elif st.session_state.store_2_selection in store_options:
            selected_store_name = st.session_state.store_2_selection
        elif store_options:
            selected_store_name = store_options[0]
            st.session_state.store_2_selection = selected_store_name

        if store_options:
            st.selectbox("Choose a Store:", options=store_options, key="store_2_selection")
            # #selected_store_name = custom_store_selector("Choose a Store:", store_options, key="store_2_selection")
            # #st.session_state["store_2_selection"] = selected_store_name
            # selected_store_name = compact_dropdown("Choose a Store:", store_options, key="store_2_selection", placeholder="-- Select --", max_show=12, panel_height=220)
            # if selected_store_name:
            #     st.session_state.store_2_selection = selected_store_name

# <<< FIX: Use session state key

        selected_row = None
        if selected_store_name:
            selected_row_df = filtered[filtered["title"] == selected_store_name]
            if not selected_row_df.empty:
                selected_row = selected_row_df.iloc[0]

        if selected_row is not None:
            st.markdown(f"### {selected_row['title']} ({selected_row.get('city','')})")
            st.markdown(f"**Recommendation:** {selected_row.get('recommendation','—')}")
            k1, k2, k3 = st.columns(3)
            k1.metric("⭐ Rating", selected_row.get("totalScore", "-"))
            k2.metric("📝 Reviews", selected_row.get("reviewsCount", 0))
            k3.metric("📍 City", selected_row.get("city", "—"))

            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
            st.subheader("✅ Key Positives")

            # --- Key Positives (collapsible) ---
            pos_points = sorted(
                parse_phrase_count_list(selected_row.get("positive_points","")),
                key=lambda x: x[1], reverse=True
            )
            
            #with st.expander(f"✅ Key Positives ({len(pos_points)})", expanded=False):
            with st.expander(f"✅ Expand to See Customer Praises", expanded=False):
                if not pos_points:
                    st.info("No positive points found for this store.")
                else:
                    # pastel chip style (optional)
                    st.markdown("""
                    <style>
                    .chip-pos { background:#2e7d32; color:#fff; padding:8px 10px; margin:6px 6px 0 0; 
                                display:inline-block; border-radius:8px; font-size:14px; }
                    </style>
                    """, unsafe_allow_html=True)
                    for phrase, num in pos_points:
                        st.markdown(f"<span class='chip-pos'>✅ {sentence_case(phrase)} ({num})</span>", unsafe_allow_html=True)


            
            # pos_points = sorted(parse_phrase_count_list(selected_row.get("positive_points","")), key=lambda x: x[1], reverse=True)
            # for phrase, num in pos_points:
            #     st.markdown(f"<div style='background:#0b3b0b; padding:8px; margin:5px; border-radius:8px; color:#a5d6a7;'>✅ {sentence_case(phrase)} ({num})</div>", unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
            if not neg_df.empty:
                st.subheader("❌ Key Negatives")

                # --- Key Negatives (collapsible with per-issue breakdown) ---
                with st.expander("❌ Expand to See Customer Concerns", expanded=False):
                    if neg_df is None or neg_df.empty:
                        st.info("No negative issues dataset available.")
                    else:
                        # filter this store, be robust to stray spaces/case
                        store_title = str(selected_row.get("title","")).strip()
                        store_neg = neg_df[neg_df["title"].astype(str).str.strip() == store_title].copy()
                
                        if store_neg.empty:
                            st.info("No negative issues found for this store in the dataset.")
                        else:
                            # normalize issue text a bit
                            store_neg["issue"] = store_neg["issue"].astype(str).str.strip()
                            store_neg = store_neg[store_neg["issue"] != ""]
                
                            # summary chips
                            issue_counts = (store_neg["issue"]
                                            .value_counts(dropna=False)
                                            .reset_index())
                            issue_counts.columns = ["Issue", "Count"]
                
                            # optional red chips for quick glance
                            st.markdown("""
                            <style>
                              .chip-neg { background:#c62828; color:#fff; padding:8px 10px; margin:6px 6px 0 0;
                                          display:inline-block; border-radius:8px; font-size:14px; }
                            </style>
                            """, unsafe_allow_html=True)
                            #for _, row_issue in issue_counts.iterrows():
                                #st.markdown(f"<span class='chip-neg'>❌ {row_issue['Issue']} ({row_issue['Count']})</span>",unsafe_allow_html=True)
                
                            #st.markdown("---")
                
                            # detailed breakdown per issue (like your old code)
                            for _, row_issue in issue_counts.iterrows():
                                issue = row_issue["Issue"]
                                count = int(row_issue["Count"])
                
                                with st.expander(f"{issue} ({count})", expanded=False):
                                    reviews_for_issue = store_neg[store_neg["issue"] == issue].copy()
                
                                    if reviews_for_issue.empty:
                                        st.info("No reviews captured for this issue.")
                                        continue
                
                                    max_to_show = len(reviews_for_issue)
                                    if max_to_show > 1:
                                        n = st.slider(
                                            f"Number of reviews to display for {issue}",
                                            1, max_to_show, min(5, max_to_show),
                                            key=f"tab2_neg_slider_{safe_key(store_title)}_{safe_key(issue)}"
                                        )
                                        reviews_to_show = reviews_for_issue.head(n)
                                    else:
                                        reviews_to_show = reviews_for_issue.head(1)
                
                                    for _, r in reviews_to_show.iterrows():
                                        txt = r.get("textTranslated", r.get("text", "—"))
                                        st.markdown(
                                            "<div style='background:#1e1e1e; padding:10px; margin:6px 0; border-radius:8px;"
                                            " white-space:pre-wrap; word-break:break-word; line-height:1.4;'>"
                                            f"{txt}</div>",
                                            unsafe_allow_html=True
                                        )

                # store_neg = neg_df[neg_df["title"] == selected_row["title"]].copy()
                # if store_neg.empty:
                #     st.info("No negative issues found for this store in the new dataset.")
                # else:
                #     issue_counts = store_neg["issue"].value_counts().reset_index()
                #     issue_counts.columns = ["Issue", "Count"]
                #     for _, row_issue in issue_counts.iterrows():
                #         issue, count = row_issue["Issue"], row_issue["Count"]
                #         with st.expander(f"{issue} ({count})", expanded=False):
                #             reviews_for_issue = store_neg[store_neg["issue"] == issue]
                #             if not reviews_for_issue.empty:
                #                 max_to_show = len(reviews_for_issue)
                #                 # <<< FIX: Only show slider if there is more than one review.
                #                 if max_to_show > 1:
                #                     n = st.slider(
                #                         f"Number of reviews to display for {issue}", 1, max_to_show, min(5, max_to_show),
                #                         key=f"tab2_neg_slider_{safe_key(selected_row['title'])}_{safe_key(issue)}" # <<< FIX: Unique key
                #                     )
                #                     reviews_to_show = reviews_for_issue.head(n)
                #                 else:
                #                     reviews_to_show = reviews_for_issue.head(1)
                #                 for _, r in reviews_to_show.iterrows():
                #                     st.markdown(f"<div style='background:#111111; padding:10px; margin:6px 0; border-radius:8px; color:#ef9a9a;white-space:pre-wrap; word-break:break-word; line-height:1.4;'>{r.get('textTranslated','—')}</div>", unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
            st.markdown("**Staff Liked:**")
            for s in str(selected_row.get("staff_liked","")).split(";"):
                if s.strip(): st.markdown(f"<div style='background:#081a2b; padding:8px; margin:5px; border-radius:8px; color:#90caf9;'>💙 {s.strip()}</div>", unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
            st.markdown("**Staff Disliked:**")
            for s in str(selected_row.get("staff_disliked","")).split(";"):
                if s.strip(): st.markdown(f"<div style='background:#111111; padding:8px; margin:5px; border-radius:8px; color:#e0e0e0;'>⚠️ {s.strip()}</div>", unsafe_allow_html=True)
        else:
            st.markdown("No store selected")

    with star_container:
        if selected_row is not None:
            render_star_chart_and_reviews(selected_row, reviews_df)
        elif not filtered.empty:
            render_star_chart_and_reviews(filtered.iloc[0], reviews_df)
# --------------------------
# Tab3: Store Comparison (A vs B vs Competitor)
# --------------------------
# ------------- Tab3: Store Comparison (with Competitor) -------------
#with tab3:
    st.header("🔁 Store Comparison View")

    # Load competitor dataset
    COMP_PATH = "competitor_store_insight.csv"
    try:
        competitor_df = pd.read_csv(COMP_PATH,  encoding="latin1")
    except FileNotFoundError:
        competitor_df = pd.DataFrame()

    store_options = sorted(filtered["title"].dropna().unique().tolist())
    comp_options = sorted(competitor_df["title"].dropna().unique().tolist()) if not competitor_df.empty else []

    placeholder = "-- Select --"

    cmp_col1, cmp_col2, cmp_col3 = st.columns(3)

    with cmp_col1:
        store_a = st.selectbox("Select Store A", options=[placeholder] + store_options, index=0, key="cmp3_store_a")
        #selected_store_name = custom_store_selector("Choose a Store:", store_options, key="store_2_selection")
        #st.session_state["store_2_selection"] = selected_store_name


    with cmp_col2:
        store_b = st.selectbox("Select Store B (Optional)", options=[placeholder] + store_options, index=0, key="cmp3_store_b")

    with cmp_col3:
        comp_store = st.selectbox("Select Competitor Store (Optional)", options=[placeholder] + comp_options, index=0, key="cmp3_comp_store")

    compare_clicked = st.button("🔍 Compare Stores", key="cmp3_button")

    if compare_clicked:
        if store_a == placeholder:
            st.warning("Please select at least Store A.")
        else:
            sa = filtered[filtered["title"] == store_a].iloc[0]

            # Store B and competitor optional
            sb = None
            sc = None
            if store_b != placeholder:
                sb = filtered[filtered["title"] == store_b].iloc[0]
            if comp_store != placeholder and not competitor_df.empty:
                sc = competitor_df[competitor_df["title"] == comp_store].iloc[0]

            cols = [st.columns(3) if sb is not None and sc is not None else st.columns(2)][0]

            # --- Store A ---
            with cols[0]:
                st.markdown(f"### {sa['title']} — {sa.get('city','')}")
                st.metric("Rating", sa.get("totalScore", "N/A"))
                st.metric("Reviews", sa.get("reviewsCount", "N/A"))
                st.markdown("**Top Positives**")
                for phrase, num in sorted(parse_phrase_count_list(sa.get("positive_points","")), key=lambda x: x[1], reverse=True)[:5]:
                    st.write(f"- ✅ {sentence_case(phrase)} ({num})")
                st.markdown("**Top Negatives**")
                for phrase, num in sorted(parse_negatives(sa.get("negative_points","")), key=lambda x: x[1], reverse=True)[:5]:
                    st.write(f"- ❌ {sentence_case(phrase)} ({num})")

            # --- Store B (if selected) ---
            if sb is not None:
                with cols[1]:
                    st.markdown(f"### {sb['title']} — {sb.get('city','')}")
                    st.metric("Rating", sb.get("totalScore", "N/A"))
                    st.metric("Reviews", sb.get("reviewsCount", "N/A"))
                    st.markdown("**Top Positives**")
                    for phrase, num in sorted(parse_phrase_count_list(sb.get("positive_points","")), key=lambda x: x[1], reverse=True)[:5]:
                        st.write(f"- ✅ {sentence_case(phrase)} ({num})")
                    st.markdown("**Top Negatives**")
                    for phrase, num in sorted(parse_negatives(sb.get("negative_points","")), key=lambda x: x[1], reverse=True)[:5]:
                        st.write(f"- ❌ {sentence_case(phrase)} ({num})")

            # --- Competitor (if selected) ---
            if sc is not None:
                with cols[-1]:
                    st.markdown(f"### {sc['title']} — Competitor")
                    # Competitor dataset might not have rating/reviews
                    rating = sc["totalScore"] if "totalScore" in sc else "N/A"
                    reviews = sc["reviewsCount"] if "reviewsCount" in sc else "N/A"
                    st.metric("Rating", rating)
                    st.metric("Reviews", reviews)
                    st.markdown("**Top Positives**")
                    for phrase, num in sorted(parse_phrase_count_list(sc.get("positive_points","")), key=lambda x: x[1], reverse=True)[:5]:
                        st.write(f"- ✅ {sentence_case(phrase)} ({num})")
                    st.markdown("**Top Negatives**")
                    for phrase, num in sorted(parse_negatives(sc.get("negative_points","")), key=lambda x: x[1], reverse=True)[:5]:
                        st.write(f"- ❌ {sentence_case(phrase)} ({num})")

