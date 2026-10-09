"""One Plotly renderer for all workbook floors, with isolated manual overrides."""
from copy import deepcopy
import html
import json
import math
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).resolve().parent / 'data'


@st.cache_data(show_spinner=False)
def load_layout(data_version, overrides_version):
    """Cache parsed data; file timestamps invalidate the cache after regeneration."""
    return (json.loads((DATA / 'floors.json').read_text()),
            json.loads((DATA / 'overrides.json').read_text()))


def layout_data():
    return load_layout((DATA / 'floors.json').stat().st_mtime_ns,
                       (DATA / 'overrides.json').stat().st_mtime_ns)


def sheet_names():
    return list(layout_data()[0]['sheets'])


def range_box(floor, address):
    from tools.import_excel import bounds
    r0, c0, r1, c1 = bounds(address)
    widths = [math.floor(w * 7 + 5) if w else 0 for w in floor['column_widths_excel']]
    heights = [h * 4 / 3 for h in floor['row_heights_points']]
    return [sum(widths[:c0 - 1]), sum(heights[:r0 - 1]),
            sum(widths[:c1]), sum(heights[:r1])]


def floor_content(sheet_name, show_helper_values=False):
    data, overrides = layout_data()
    floor = data['sheets'][sheet_name]
    custom = overrides.get('sheets', {}).get(sheet_name, {})
    replacements = custom.get('text_replacements', {})
    pairs = custom.get('vertical_station_pairs', [])
    removed = {pair['label_cell'] for pair in pairs}
    hidden = set() if show_helper_values else set(overrides.get('hide_unmerged_values', []))
    texts = []
    for original in floor['texts']:
        if original['cell'] in removed:
            continue
        if not original['merged'] and original['text'] in hidden:
            continue
        text = deepcopy(original)
        text['text'] = replacements.get(text['cell'], text['text'])
        texts.append(text)
    split_lines = []
    originals = {text['cell']: text for text in floor['texts']}
    for pair in pairs:
        x0, y0, x1, y1 = range_box(floor, pair['range'])
        center = (x0 + x1) / 2
        split_lines.append([center, y0, center, y1, 'medium', '#000000'])
        for label, left, right in zip(pair['labels'], [x0, center], [center, x1]):
            text = deepcopy(originals[pair['label_cell']])
            text.update(text=label, box=[left, y0, right, y1], manual=True)
            text['alignment'] = {'horizontal': 'center', 'vertical': 'center'}
            texts.append(text)
    return floor, texts, split_lines


def build_floor_figure(sheet_name, show_helper_values=False):
    floor, texts, split_lines = floor_content(sheet_name, show_helper_values)
    shapes = [dict(type='rect', x0=x0, y0=-y1, x1=x1, y1=-y0,
                   fillcolor=color, line=dict(width=0), layer='below')
              for x0, y0, x1, y1, color in floor['rectangles']]
    for x0, y0, x1, y1, kind, color in floor['lines'] + split_lines:
        width = 3 if kind in ('thick', 'double') else 2 if kind.startswith('medium') else 1
        dash = 'dot' if kind in ('dotted', 'hair') else 'dash' if 'dash' in kind.lower() else 'solid'
        shapes.append(dict(type='line', x0=x0, y0=-y0, x1=x1, y1=-y1,
                           line=dict(color=color, width=width, dash=dash), layer='below'))
    annotations = []
    overview_scale = 1500 / floor['width']
    for item in texts:
        x0, y0, x1, y1 = item['box']
        align = item['alignment']
        horizontal = align.get('horizontal', 'center')
        vertical = align.get('vertical', 'center')
        x = x0 if horizontal == 'left' else x1 if horizontal == 'right' else (x0 + x1) / 2
        y = y0 if vertical == 'top' else y1 if vertical == 'bottom' else (y0 + y1) / 2
        rotation = int(align.get('textRotation', 0))
        angle = -rotation if rotation <= 90 else 180 - rotation if rotation <= 180 else 0
        value = html.escape(item['text']).replace('\n', '<br>')
        if item['font']['bold']:
            value = '<b>' + value + '</b>'
        annotations.append(dict(x=x, y=-y, text=value, showarrow=False,
                                textangle=angle, align=horizontal if horizontal in ('left', 'right') else 'center',
                                xanchor=horizontal if horizontal in ('left', 'right') else 'center',
                                yanchor=vertical if vertical in ('top', 'bottom') else 'middle',
                                font=dict(color=item['font']['color'], family=item['font']['family'],
                                          size=max(5, min(18, item['font']['size'] * 4 / 3 * overview_scale)))))
    figure = go.Figure()
    figure.update_layout(
        shapes=shapes, annotations=annotations, showlegend=False,
        paper_bgcolor='#0b0f19', plot_bgcolor='#0b0f19',
        margin=dict(l=5, r=5, t=5, b=5),
        height=max(380, round(1500 * floor['height'] / floor['width']) + 10),
        xaxis=dict(visible=False, showgrid=False, zeroline=False,
                   range=[0, floor['width']], constrain='domain'),
        yaxis=dict(visible=False, showgrid=False, zeroline=False,
                   range=[-floor['height'], 0], scaleanchor='x', scaleratio=1,
                   constrain='domain'),
        dragmode='pan', uirevision=sheet_name,
    )
    return figure


def render_excel_floor(sheet_name, show_helper_values=False):
    figure = build_floor_figure(sheet_name, show_helper_values)
    st.plotly_chart(figure, width='stretch', key=f'floor-{sheet_name}',
                    config={'scrollZoom': True, 'displaylogo': False,
                            'modeBarButtonsToRemove': ['select2d', 'lasso2d']})
    return figure
