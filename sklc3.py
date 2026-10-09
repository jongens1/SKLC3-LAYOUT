import plotly.graph_objects as go
import streamlit as st

# Nastavenie aplikácie
st.set_page_config(
    page_title="WMS Layout Skladu", layout="wide", initial_sidebar_state="collapsed"
)

# Custom CSS pre temný moderný vzhľad stránky
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0b0f19;
        }
        h1 {
            color: #f8fafc;
            font-family: 'Segoe UI', Roboto, sans-serif;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🏭 Layout Skladu – SKLC3")

# -----------------------------------------------------------------------------
# 1. ZOZNAM STANÍC
# -----------------------------------------------------------------------------
stations = [
    # Horný rad
    {"id": "S16", "x0": 11, "y0": 38, "x1": 27, "y1": 48},
    {"id": "S18", "x0": 28, "y0": 38, "x1": 37, "y1": 48},
    {"id": "S20", "x0": 38, "y0": 38, "x1": 47, "y1": 48},
    {"id": "S22", "x0": 50, "y0": 38, "x1": 61, "y1": 48},
    {"id": "S24", "x0": 61, "y0": 38, "x1": 71, "y1": 48},
    {"id": "S26", "x0": 72, "y0": 38, "x1": 81, "y1": 48},
    # Stredný blok - horné stanice
    {"id": "S13", "x0": 21, "y0": 26, "x1": 29, "y1": 35},
    {"id": "S15", "x0": 30, "y0": 26, "x1": 38, "y1": 35},
    {"id": "S17", "x0": 39, "y0": 26, "x1": 47, "y1": 35},
    {"id": "S19", "x0": 50, "y0": 26, "x1": 59, "y1": 35},
    {"id": "S21", "x0": 60, "y0": 26, "x1": 69, "y1": 35},
    {"id": "S23", "x0": 70, "y0": 26, "x1": 79, "y1": 35},
    # Stredný blok - dolné stanice
    {"id": "S11", "x0": 21, "y0": 14, "x1": 29, "y1": 23},
    {"id": "S09", "x0": 30, "y0": 14, "x1": 38, "y1": 23},
    {"id": "S07", "x0": 39, "y0": 14, "x1": 47, "y1": 23},
    {"id": "S05", "x0": 50, "y0": 14, "x1": 59, "y1": 23},
    {"id": "S03", "x0": 60, "y0": 14, "x1": 69, "y1": 23},
    {"id": "S01", "x0": 70, "y0": 14, "x1": 79, "y1": 23},
    # Spodný rad
    {"id": "S10", "x0": 4, "y0": 3, "x1": 29, "y1": 10},
    {"id": "S08", "x0": 30, "y0": 3, "x1": 38, "y1": 10},
    {"id": "S06", "x0": 39, "y0": 3, "x1": 47, "y1": 10},
    {"id": "S04", "x0": 50, "y0": 3, "x1": 70, "y1": 10},
    {"id": "S02", "x0": 73, "y0": 3, "x1": 97, "y1": 10},
    # Ľavá strana
    {"id": "S14", "x0": 4, "y0": 26, "x1": 17, "y1": 36},
    {"id": "S12", "x0": 4, "y0": 19, "x1": 17, "y1": 24},
    {"id": "S12", "x0": 4, "y0": 11, "x1": 14, "y1": 17},
    # Pravá strana
    {"id": "S28", "x0": 82, "y0": 26, "x1": 98, "y1": 44},
    {"id": "S30", "x0": 82, "y0": 11, "x1": 98, "y1": 24},
]

# Prvky infraštruktúry
infra = [
    # Výťahy (Modré)
    {
        "name": "VÝŤAH",
        "x0": 9,
        "y0": 28,
        "x1": 12,
        "y1": 31,
        "color": "#0284c7",
    },
    {
        "name": "VÝŤAH",
        "x0": 91,
        "y0": 22,
        "x1": 93,
        "y1": 24,
        "color": "#0284c7",
    },
    {
        "name": "VÝŤAH",
        "x0": 92,
        "y0": 45,
        "x1": 94,
        "y1": 48,
        "color": "#0284c7",
    },
    # Schody (Červené)
    {
        "name": "SCHODY",
        "x0": 15,
        "y0": 13,
        "x1": 17,
        "y1": 16,
        "color": "#e11d48",
    },
    {
        "name": "SCHODY",
        "x0": 15,
        "y0": 42,
        "x1": 17,
        "y1": 44,
        "color": "#e11d48",
    },
    {
        "name": "SCHODY",
        "x0": 60,
        "y0": 44,
        "x1": 63,
        "y1": 46,
        "color": "#e11d48",
    },
    {
        "name": "SCHODY",
        "x0": 58,
        "y0": 18,
        "x1": 60,
        "y1": 21,
        "color": "#e11d48",
    },
    {
        "name": "SCHODY",
        "x0": 91,
        "y0": 15,
        "x1": 93,
        "y1": 18,
        "color": "#e11d48",
    },
    {
        "name": "SCHODY",
        "x0": 95,
        "y0": 45,
        "x1": 97,
        "y1": 48,
        "color": "#e11d48",
    },
    # Predáci (Žlté)
    {
        "name": "PREDÁK",
        "x0": 49,
        "y0": 25,
        "x1": 52,
        "y1": 26,
        "color": "#ca8a04",
    },
    {
        "name": "PREDÁK",
        "x0": 76,
        "y0": 12,
        "x1": 79,
        "y1": 13,
        "color": "#ca8a04",
    },
]

fig = go.Figure()

# -----------------------------------------------------------------------------
# 2. VYKRESLENIE STANÍC + TEXTOV (LAYER = BELOW zaručuje, že text bude Navrchu)
# -----------------------------------------------------------------------------
for s in stations:
    cx = (s["x0"] + s["x1"]) / 2
    cy = (s["y0"] + s["y1"]) / 2

    # Obdĺžnik stanice
    fig.add_shape(
        type="rect",
        x0=s["x0"],
        y0=s["y0"],
        x1=s["x1"],
        y1=s["y1"],
        fillcolor="#1e293b",
        line=dict(color="#3b82f6", width=2),
        layer="below",  # Dôležité: Tvar je POD textom
    )

    # Nápis v strede štvorca (vynútené Plotly Anotáciou)
    if not (s["id"] == "S12" and cy < 18):  # Duplicitný nápis pre S12 vynecháme
        fig.add_annotation(
            x=cx,
            y=cy,
            text=f"<b>{s['id']}</b>",
            showarrow=False,
            font=dict(color="#ffffff", size=15, family="Consolas, monospace"),
            align="center",
        )

# -----------------------------------------------------------------------------
# 3. VYKRESLENIE INFRAŠTRUKTÚRY
# -----------------------------------------------------------------------------
for item in infra:
    cx = (item["x0"] + item["x1"]) / 2
    cy = (item["y0"] + item["y1"]) / 2

    fig.add_shape(
        type="rect",
        x0=item["x0"],
        y0=item["y0"],
        x1=item["x1"],
        y1=item["y1"],
        fillcolor=item["color"],
        line=dict(color="#ffffff", width=1),
        layer="below",
    )

    # Nápisy pre výťahy/schody
    fig.add_annotation(
        x=cx,
        y=cy,
        text=f"<b>{item['name']}</b>",
        showarrow=False,
        font=dict(
            color="#ffffff", size=8, family="Segoe UI, sans-serif"
        ),
        align="center",
    )

# -----------------------------------------------------------------------------
# 4. TRASA / DOPRAVNÍK (Svietivá azúrová čiara)
# -----------------------------------------------------------------------------
conveyor_x = [18, 18, 20, 80, 80, 80, 90, 90, 80, 80, 20, 20, 18]
conveyor_y = [24, 36, 36, 36, 36, 13, 13, 11, 11, 13, 13, 24, 24]

fig.add_trace(
    go.Scatter(
        x=conveyor_x,
        y=conveyor_y,
        mode="lines",
        line=dict(color="#06b6d4", width=3.5),
        hoverinfo="skip",
        showlegend=False,
    )
)

# -----------------------------------------------------------------------------
# 5. DIZAJN MAPY (CAD Blueprint grid)
# -----------------------------------------------------------------------------
fig.update_layout(
    plot_bgcolor="#0b0f19",
    paper_bgcolor="#0b0f19",
    xaxis=dict(
        showgrid=True,
        gridcolor="#1e293b",
        gridwidth=1,
        zeroline=False,
        showticklabels=False,
        range=[0, 102],
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#1e293b",
        gridwidth=1,
        zeroline=False,
        showticklabels=False,
        range=[0, 52],
    ),
    height=720,
    margin=dict(l=10, r=10, t=10, b=10),
)

st.plotly_chart(fig, use_container_width=True)
