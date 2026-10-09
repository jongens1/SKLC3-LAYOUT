import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Layout Skladu", layout="wide")
st.title("📦 Layout Skladu")

# Jednotná farba pre všetky stanice
STATION_COLOR = "#2b3e6b"  # Jednotná modrá farba staníc
INFRA_COLOR = "#475569"  # Farba pre doplňujúce prvky (schody/výťahy)

# Zoznam staníc a ich pozícií
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

# Doplnky (Výťahy, Schody, Predák)
infra = [
    {"name": "Výťah", "x0": 9, "y0": 28, "x1": 12, "y1": 31},
    {"name": "Výťah", "x0": 91, "y0": 22, "x1": 93, "y1": 24},
    {"name": "Výťah", "x0": 92, "y0": 45, "x1": 94, "y1": 48},
    {"name": "Schody", "x0": 15, "y0": 13, "x1": 17, "y1": 16},
    {"name": "Schody", "x0": 15, "y0": 42, "x1": 17, "y1": 44},
    {"name": "Schody", "x0": 60, "y0": 44, "x1": 63, "y1": 46},
    {"name": "Schody", "x0": 58, "y0": 18, "x1": 60, "y1": 21},
    {"name": "Schody", "x0": 91, "y0": 15, "x1": 93, "y1": 18},
    {"name": "Schody", "x0": 95, "y0": 45, "x1": 97, "y1": 48},
    {"name": "Predák", "x0": 49, "y0": 25, "x1": 52, "y1": 26},
    {"name": "Predák", "x0": 76, "y0": 12, "x1": 79, "y1": 13},
]

fig = go.Figure()

# 1. Vykreslenie všetkých STANÍC (Jednotná farba)
for s in stations:
    fig.add_shape(
        type="rect",
        x0=s["x0"],
        y0=s["y0"],
        x1=s["x1"],
        y1=s["y1"],
        fillcolor=STATION_COLOR,
        line=dict(color="#ffffff", width=1.5),
    )

    # Názov stanice presne do stredu štvorca
    cx = (s["x0"] + s["x1"]) / 2
    cy = (s["y0"] + s["y1"]) / 2

    fig.add_trace(
        go.Scatter(
            x=[cx],
            y=[cy],
            text=[f"<b>{s['id']}</b>"],
            mode="text",
            textfont=dict(color="white", size=14),
            hoverinfo="none",
            showlegend=False,
        )
    )

# 2. Vykreslenie doplnkov (Schody / Výťahy / Predák)
for item in infra:
    fig.add_shape(
        type="rect",
        x0=item["x0"],
        y0=item["y0"],
        x1=item["x1"],
        y1=item["y1"],
        fillcolor=INFRA_COLOR,
        line=dict(color="#ffffff", width=1),
    )
    cx = (item["x0"] + item["x1"]) / 2
    cy = (item["y0"] + item["y1"]) / 2

    fig.add_trace(
        go.Scatter(
            x=[cx],
            y=[cy],
            text=[item["name"]],
            mode="text",
            textfont=dict(color="white", size=8),
            hoverinfo="none",
            showlegend=False,
        )
    )

# 3. Ulička / Dopravník
conveyor_x = [18, 18, 20, 80, 80, 80, 90, 90, 80, 80, 20, 20, 18]
conveyor_y = [24, 36, 36, 36, 36, 13, 13, 11, 11, 13, 13, 24, 24]

fig.add_trace(
    go.Scatter(
        x=conveyor_x,
        y=conveyor_y,
        mode="lines",
        line=dict(color="#64748b", width=4),
        hoverinfo="skip",
        showlegend=False,
    )
)

# 4. Čistý vzhľad (Tmavšie pozadie pre lepšiu čitateľnosť)
fig.update_layout(
    plot_bgcolor="#0f172a",
    paper_bgcolor="#0f172a",
    xaxis=dict(
        showgrid=False, zeroline=False, showticklabels=False, range=[0, 102]
    ),
    yaxis=dict(
        showgrid=False, zeroline=False, showticklabels=False, range=[0, 52]
    ),
    height=680,
    margin=dict(l=10, r=10, t=10, b=10),
)

st.plotly_chart(fig, use_container_width=True)
