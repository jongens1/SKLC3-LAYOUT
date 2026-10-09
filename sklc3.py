import plotly.graph_objects as go
import streamlit as st

# Nastavenie stránky Streamlit
st.set_page_config(
    page_title="Layout Skladu - Mapa", layout="wide", initial_sidebar_state="expanded"
)

st.title("📦 Mapa a Layout Skladu")

# -----------------------------------------------------------------------------
# 1. DÁTOVÝ MODEL ZÓN (Súradnice X, Y, rozmery, farba, stav)
# -----------------------------------------------------------------------------
zones = [
    # --- ŽLTÉ ZÓNY (Hore) ---
    {
        "id": "S16",
        "x0": 11,
        "y0": 38,
        "x1": 27,
        "y1": 48,
        "color": "#ffe600",
        "category": "Žltá zóna",
        "capacity": "85%",
    },
    {
        "id": "S18",
        "x0": 28,
        "y0": 38,
        "x1": 37,
        "y1": 48,
        "color": "#ffe600",
        "category": "Žltá zóna",
        "capacity": "40%",
    },
    {
        "id": "S20",
        "x0": 38,
        "y0": 38,
        "x1": 47,
        "y1": 48,
        "color": "#ffe600",
        "category": "Žltá zóna",
        "capacity": "92%",
    },
    {
        "id": "S22",
        "x0": 50,
        "y0": 38,
        "x1": 61,
        "y1": 48,
        "color": "#ffe600",
        "category": "Žltá zóna",
        "capacity": "60%",
    },
    {
        "id": "S24",
        "x0": 61,
        "y0": 38,
        "x1": 71,
        "y1": 48,
        "color": "#ffe600",
        "category": "Žltá zóna",
        "capacity": "75%",
    },
    {
        "id": "S26",
        "x0": 72,
        "y0": 38,
        "x1": 81,
        "y1": 48,
        "color": "#ffe600",
        "category": "Žltá zóna",
        "capacity": "15%",
    },
    # --- ZELENÉ ZÓNY (Stred hore) ---
    {
        "id": "S13",
        "x0": 21,
        "y0": 26,
        "x1": 29,
        "y1": 35,
        "color": "#a1d99b",
        "category": "Zelená zóna",
        "capacity": "50%",
    },
    {
        "id": "S15",
        "x0": 30,
        "y0": 26,
        "x1": 38,
        "y1": 35,
        "color": "#a1d99b",
        "category": "Zelená zóna",
        "capacity": "90%",
    },
    {
        "id": "S17",
        "x0": 39,
        "y0": 26,
        "x1": 47,
        "y1": 35,
        "color": "#a1d99b",
        "category": "Zelená zóna",
        "capacity": "30%",
    },
    {
        "id": "S19",
        "x0": 50,
        "y0": 26,
        "x1": 59,
        "y1": 35,
        "color": "#a1d99b",
        "category": "Zelená zóna",
        "capacity": "65%",
    },
    {
        "id": "S21",
        "x0": 60,
        "y0": 26,
        "x1": 69,
        "y1": 35,
        "color": "#a1d99b",
        "category": "Zelená zóna",
        "capacity": "80%",
    },
    {
        "id": "S23",
        "x0": 70,
        "y0": 26,
        "x1": 79,
        "y1": 35,
        "color": "#a1d99b",
        "category": "Zelená zóna",
        "capacity": "45%",
    },
    # --- MODRÉ ZÓNY (Stred dole) ---
    {
        "id": "S11",
        "x0": 21,
        "y0": 14,
        "x1": 29,
        "y1": 23,
        "color": "#9ecae1",
        "category": "Modrá zóna",
        "capacity": "70%",
    },
    {
        "id": "S09",
        "x0": 30,
        "y0": 14,
        "x1": 38,
        "y1": 23,
        "color": "#9ecae1",
        "category": "Modrá zóna",
        "capacity": "88%",
    },
    {
        "id": "S07",
        "x0": 39,
        "y0": 14,
        "x1": 47,
        "y1": 23,
        "color": "#9ecae1",
        "category": "Modrá zóna",
        "capacity": "20%",
    },
    {
        "id": "S05",
        "x0": 50,
        "y0": 14,
        "x1": 59,
        "y1": 23,
        "color": "#9ecae1",
        "category": "Modrá zóna",
        "capacity": "95%",
    },
    {
        "id": "S03",
        "x0": 60,
        "y0": 14,
        "x1": 69,
        "y1": 23,
        "color": "#9ecae1",
        "category": "Modrá zóna",
        "capacity": "10%",
    },
    {
        "id": "S01",
        "x0": 70,
        "y0": 14,
        "x1": 79,
        "y1": 23,
        "color": "#9ecae1",
        "category": "Modrá zóna",
        "capacity": "60%",
    },
    # --- PURPUROVÉ ZÓNY (Dole) ---
    {
        "id": "S10",
        "x0": 4,
        "y0": 3,
        "x1": 29,
        "y1": 10,
        "color": "#6a5acd",
        "category": "Purpurová zóna",
        "capacity": "55%",
    },
    {
        "id": "S08",
        "x0": 30,
        "y0": 3,
        "x1": 38,
        "y1": 10,
        "color": "#6a5acd",
        "category": "Purpurová zóna",
        "capacity": "40%",
    },
    {
        "id": "S06",
        "x0": 39,
        "y0": 3,
        "x1": 47,
        "y1": 10,
        "color": "#6a5acd",
        "category": "Purpurová zóna",
        "capacity": "78%",
    },
    {
        "id": "S04",
        "x0": 50,
        "y0": 3,
        "x1": 70,
        "y1": 10,
        "color": "#6a5acd",
        "category": "Purpurová zóna",
        "capacity": "90%",
    },
    {
        "id": "S02",
        "x0": 73,
        "y0": 3,
        "x1": 97,
        "y1": 10,
        "color": "#6a5acd",
        "category": "Purpurová zóna",
        "capacity": "33%",
    },
    # --- ĽAVÝ BLOK (Červená / Oranžová) ---
    {
        "id": "S14",
        "x0": 4,
        "y0": 26,
        "x1": 17,
        "y1": 36,
        "color": "#cc0000",
        "category": "Červená zóna",
        "capacity": "100%",
    },
    {
        "id": "S12",
        "x0": 4,
        "y0": 19,
        "x1": 17,
        "y1": 24,
        "color": "#f39c12",
        "category": "Oranžová zóna",
        "capacity": "50%",
    },
    {
        "id": "S12_dole",
        "x0": 4,
        "y0": 11,
        "x1": 14,
        "y1": 17,
        "color": "#f39c12",
        "category": "Oranžová zóna",
        "capacity": "50%",
    },
    # --- PRAVÝ BLOK (Sivá) ---
    {
        "id": "S28",
        "x0": 82,
        "y0": 26,
        "x1": 98,
        "y1": 44,
        "color": "#888888",
        "category": "Sivá zóna",
        "capacity": "82%",
    },
    {
        "id": "S30",
        "x0": 82,
        "y0": 11,
        "x1": 98,
        "y1": 24,
        "color": "#888888",
        "category": "Sivá zóna",
        "capacity": "64%",
    },
]

# Prvky infraštruktúry (Schody, Výťahy, Predák)
infra = [
    # Výťahy
    {
        "name": "Výťah",
        "x0": 9,
        "y0": 28,
        "x1": 12,
        "y1": 31,
        "color": "#0044cc",
        "text_color": "white",
    },
    {
        "name": "Výťah",
        "x0": 91,
        "y0": 22,
        "x1": 93,
        "y1": 24,
        "color": "#0044cc",
        "text_color": "white",
    },
    {
        "name": "Výťah",
        "x0": 92,
        "y0": 45,
        "x1": 94,
        "y1": 48,
        "color": "#0044cc",
        "text_color": "white",
    },
    # Schody
    {
        "name": "Schody",
        "x0": 15,
        "y0": 13,
        "x1": 17,
        "y1": 16,
        "color": "#cc0000",
        "text_color": "white",
    },
    {
        "name": "Schody",
        "x0": 15,
        "y0": 42,
        "x1": 17,
        "y1": 44,
        "color": "#cc0000",
        "text_color": "white",
    },
    {
        "name": "Schody",
        "x0": 60,
        "y0": 44,
        "x1": 63,
        "y1": 46,
        "color": "#cc0000",
        "text_color": "white",
    },
    {
        "name": "Schody",
        "x0": 58,
        "y0": 18,
        "x1": 60,
        "y1": 21,
        "color": "#cc0000",
        "text_color": "white",
    },
    {
        "name": "Schody",
        "x0": 91,
        "y0": 15,
        "x1": 93,
        "y1": 18,
        "color": "#cc0000",
        "text_color": "white",
    },
    {
        "name": "Schody",
        "x0": 95,
        "y0": 45,
        "x1": 97,
        "y1": 48,
        "color": "#cc0000",
        "text_color": "white",
    },
    # Predák
    {
        "name": "Predák",
        "x0": 49,
        "y0": 25,
        "x1": 52,
        "y1": 26,
        "color": "#ffff00",
        "text_color": "black",
    },
    {
        "name": "Predák",
        "x0": 76,
        "y0": 12,
        "x1": 79,
        "y1": 13,
        "color": "#ffff00",
        "text_color": "black",
    },
]

# -----------------------------------------------------------------------------
# 2. SIDEBAR (Ovládanie a Filtre)
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 Filtre & Vyhľadávanie")

# Vyhľadávanie konkrétnej zóny
search_query = (
    st.sidebar.text_input("Nájdi zónu (napr. S05, S14):", "").strip().upper()
)

# Filter podľa kategórie
categories = list(set([z["category"] for z in zones]))
selected_categories = st.sidebar.multiselect(
    "Zobraziť kategórie:", categories, default=categories
)

# -----------------------------------------------------------------------------
# 3. VYKRESLENIE MAPY CEZ PLOTLY
# -----------------------------------------------------------------------------
fig = go.Figure()

# Vykreslenie ZÓN
for z in zones:
    # Ak je zapnutý filter kategórií
    if z["category"] not in selected_categories:
        continue

    # Zvýraznenie vyhľadanej zóny
    is_searched = search_query and search_query in z["id"]
    border_color = "#ff0000" if is_searched else "#000000"
    border_width = 4 if is_searched else 1.5

    # Nakresli obdĺžnik zóny
    fig.add_shape(
        type="rect",
        x0=z["x0"],
        y0=z["y0"],
        x1=z["x1"],
        y1=z["y1"],
        fillcolor=z["color"],
        line=dict(color=border_color, width=border_width),
        opacity=1.0 if (not search_query or is_searched) else 0.3,
    )

    # Pridaj textový štítok zóny + Hover info
    if "S12_dole" not in z["id"]:  # Preskočiť text pre spodnú časť S12
        cx = (z["x0"] + z["x1"]) / 2
        cy = (z["y0"] + z["y1"]) / 2

        fig.add_trace(
            go.Scatter(
                x=[cx],
                y=[cy],
                text=[f"<b>{z['id']}</b>"],
                mode="text",
                textfont=dict(color="black", size=15),
                hoverinfo="text",
                hovertext=f"<b>Zóna {z['id']}</b><br>Kategória: {z['category']}<br>Zaplnenosť: {z['capacity']}",
                showlegend=False,
            )
        )

# Vykreslenie INFRAŠTRUKTÚRY (Výťahy, Schody, Predák)
for item in infra:
    fig.add_shape(
        type="rect",
        x0=item["x0"],
        y0=item["y0"],
        x1=item["x1"],
        y1=item["y1"],
        fillcolor=item["color"],
        line=dict(color="#000000", width=1),
    )

    cx = (item["x0"] + item["x1"]) / 2
    cy = (item["y0"] + item["y1"]) / 2

    fig.add_trace(
        go.Scatter(
            x=[cx],
            y=[cy],
            text=[item["name"]],
            mode="text",
            textfont=dict(color=item["text_color"], size=7),
            hoverinfo="text",
            hovertext=f"Infraštruktúra: {item['name']}",
            showlegend=False,
        )
    )

# Vykreslenie TRASE / ULIČIEK (Modrá čiara s dráhou dopravníka)
conveyor_x = [
    18,
    18,
    20,
    80,
    80,
    80,
    90,
    90,
    80,
    80,
    20,
    20,
    18,
]
conveyor_y = [24, 36, 36, 36, 36, 13, 13, 11, 11, 13, 13, 24, 24]

fig.add_trace(
    go.Scatter(
        x=conveyor_x,
        y=conveyor_y,
        mode="lines",
        line=dict(color="#5c7599", width=6),
        hoverinfo="skip",
        showlegend=False,
    )
)

# -----------------------------------------------------------------------------
# 4. NASTAVENIE DIZAJNU MAPY (Pozadie ako na obrázku)
# -----------------------------------------------------------------------------
fig.update_layout(
    plot_bgcolor="#f4e8c1",  # Svetložltá farba podlahy zo záberu
    paper_bgcolor="#1e1e1e",
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[0, 102],
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[0, 52],
    ),
    height=650,
    margin=dict(l=10, r=10, t=10, b=10),
)

# Zobrazenie v aplikácii
st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# 5. SPODNÝ DETAIL (Prehľad a Metriky)
# -----------------------------------------------------------------------------
st.subheader("📊 Rýchly prehľad skladu")
col1, col2, col3 = st.columns(3)
col1.metric(label="Celkový počet zón", value=len(zones) - 1)
col2.metric(label="Priemerná zaplnenosť", value="62 %")
col3.metric(label="Kriticky plné zóny (>90%)", value="S14, S05, S20")
