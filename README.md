# SKLC3 warehouse layout

Streamlit/Plotly viewer for the four floors in `data/layout.xlsx`.

```bash
python -m pip install -r requirements.txt
python -m streamlit run sklc3.py --server.headless=true --browser.gatherUsageStats=false
python -m unittest discover -s tests -v
```

Select a floor, zoom with the mouse wheel, drag to pan, and double-click to reset.
The app keeps a dark background; floor colors and labels come from Excel.

## Data and rendering

`tools/import_excel.py` uses the Python standard library to compile the workbook:

```bash
python tools/import_excel.py
```

Commit the regenerated `data/floors.json` together with the source workbook.
The exporter preserves text, merged ranges, row heights, column widths, font
colors, bold text, rotations, and borders. It resolves Excel theme colors and
tints. Coordinates use approximate Excel pixels at 96 DPI, with a common
Calibri-width conversion; they are not measurements in meters. Chart axes are
hidden and locked to an equal scale to preserve the floor aspect ratio.
Tiny Excel handwriting objects are not rendered; floor geometry comes from cells.

Adjacent cells with the same fill become larger rectangles. Border intervals are
coalesced independently, preserving station boundaries and irregular silhouettes.
Empty cells produce no shapes. Formatting-only trailing rows/columns are excluded.
`excel_renderer.render_excel_floor(sheet_name)` handles every floor with Plotly
rectangle/line shapes and text annotations. JSON parsing is cached with
`st.cache_data`; file modification timestamps invalidate that cache. Excel is
only read when regenerating the data, never during an ordinary app rerun.

## Manual additions

`data/overrides.json` holds all manual changes separately from source data:

- 2NP upper-row labels are shortened to BPO20–BPO28.
- The nine 3K blocks are labeled BPO30–BPO38.
- Blocks 3A–3I get vertical center dividers and BPO01–BPO18 labels.
- Unmerged helper values `1` are hidden by default; the checkbox restores them.

Everything else keeps the workbook labels. No missing locations are invented:
4C-14, 4C-15, and 4H-08 are absent from XPO. The old manually drawn map is
replaced by the workbook renderer.
