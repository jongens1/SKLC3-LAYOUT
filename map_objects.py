"""Normalize spreadsheet geometry into warehouse objects, without cell borders."""
import re
import unicodedata
import streamlit as st
from excel_renderer import DATA, floor_content, layout_data


def fold(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value).casefold()
                   if not unicodedata.combining(c))


def object_type(label):
    value = fold(label)
    if any(word in value for word in ('schody', 'vytah', 'wc', 'dvere', 'vrata', 'vstup', 'turnik')):
        return 'infra'
    if re.match(r'^(S\d+|BPO\d+|XPO-?\d+)$', label):
        return 'station'
    if re.match(r'^(VB\d+|R\d+|4[A-Z]-\d+)', label):
        return 'rack'
    return 'zone'


def color_components(rectangles):
    """Join touching same-color strips; keep separate buildings/blocks separate."""
    groups = {}
    for rectangle in rectangles:
        if rectangle[4] not in ('#000000', '#FFFFFF'):
            groups.setdefault(rectangle[4], []).append(rectangle)
    components = []
    for color, rects in groups.items():
        parent = list(range(len(rects)))
        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
        for i, a in enumerate(rects):
            for j in range(i):
                b = rects[j]
                x_overlap = min(a[2], b[2]) - max(a[0], b[0])
                y_overlap = min(a[3], b[3]) - max(a[1], b[1])
                if (x_overlap > 0 and y_overlap >= -0.01) or (y_overlap > 0 and x_overlap >= -0.01):
                    parent[find(i)] = find(j)
        joined = {}
        for i, rect in enumerate(rects):
            joined.setdefault(find(i), []).append(rect)
        for parts in joined.values():
            components.append({'color': color, 'parts': parts,
                               'box': [min(r[0] for r in parts), min(r[1] for r in parts),
                                       max(r[2] for r in parts), max(r[3] for r in parts)],
                               'area': sum((r[2]-r[0])*(r[3]-r[1]) for r in parts)})
    return components


def contains(component, box):
    x, y = (box[0]+box[2])/2, (box[1]+box[3])/2
    return any(r[0] <= x <= r[2] and r[1] <= y <= r[3] for r in component['parts'])


def normalize_floor(sheet_name):
    data, _ = layout_data()
    return cached_objects(sheet_name, data['source_sha256'],
                          DATA.joinpath('overrides.json').stat().st_mtime_ns)


@st.cache_data(show_spinner=False)
def cached_objects(sheet_name, source_version, overrides_version):
    floor, texts, _ = floor_content(sheet_name)
    components = color_components(floor['rectangles'])
    labels = [t for t in texts if not t['text'].strip().isdigit()
              and t['text'].strip() not in ('←', '↑', '↓', '→')]
    associations = {}
    for index, text in enumerate(labels):
        matches = [(i, c) for i, c in enumerate(components) if contains(c, text['box'])]
        if matches:
            component_index, _ = min(matches, key=lambda pair: pair[1]['area'])
            associations[index] = component_index
    counts = {}
    for index in associations.values():
        counts[index] = counts.get(index, 0)+1
    objects = []
    used = set()
    for index, text in enumerate(labels):
        component_index = associations.get(index)
        component = components[component_index] if component_index is not None else None
        kind = object_type(text['text'])
        box = text['box']
        if component is not None:
            used.add(component_index)
            if counts[component_index] == 1 and not text.get('manual'):
                box = component['box']
        x0, y0, x1, y1 = box
        short = re.split(r'\s*=\s*', text['text'])[0]
        if kind == 'rack':
            short = text['text'].split('=')[0].strip()
        group = ''
        if text.get('manual'):
            group = '3' + chr(ord('A') + (int(text['text'][3:])-1)//2) + ' · '
        objects.append({'id': f"{sheet_name}:{text['cell']}:{text['text']}",
                        'floor': sheet_name, 'type': kind, 'label': short,
                        'x': x0, 'y': y0, 'w': x1-x0, 'h': y1-y0,
                        'color': component['color'] if component else '#64748b',
                        'hover': group + text['text'], 'source_cell': text['cell']})
    floor_area = floor['width']*floor['height']
    for index, component in enumerate(components):
        if index in used or component['area'] < floor_area * 0.00025:
            continue
        color = component['color']
        if color in ('#F7F5BE', '#DEEBF7', '#D9D9D9', '#FBE5D6'):
            continue
        kind = 'conveyor' if color in ('#FF33CC', '#FA00ED') else 'block'
        x0,y0,x1,y1 = component['box']
        objects.append({'id':f'{sheet_name}:area:{index}', 'floor':sheet_name,
                        'type':kind, 'label':'', 'x':x0,'y':y0,'w':x1-x0,'h':y1-y0,
                        'color':color, 'hover':'Dopravník / trasa' if kind=='conveyor' else 'Blok skladu',
                        'parts':component['parts']})
    # A rack row is one overview object; its real locations remain searchable.
    rows = {}
    for obj in objects:
        match = re.match(r'^(4[A-Z])-', obj['label'])
        if obj['type'] == 'rack' and match:
            rows.setdefault(match.group(1), []).append(obj)
    for prefix, members in rows.items():
        x0=min(o['x'] for o in members); y0=min(o['y'] for o in members)
        x1=max(o['x']+o['w'] for o in members); y1=max(o['y']+o['h'] for o in members)
        group_id=f'{sheet_name}:rack-row:{prefix}'
        for member in members: member['parent_id']=group_id
        unique=sorted({o['label'] for o in members})
        objects.append({'id':group_id,'floor':sheet_name,'type':'rack',
                        'label':prefix,'x':x0,'y':y0,'w':x1-x0,'h':y1-y0,
                        'color':members[0]['color'],
                        'hover':prefix+' · '+str(len(unique))+' lokácií', 'overview_group':True})
    return {'width':floor['width'],'height':floor['height'],'objects':objects}


def search_objects(objects, query):
    query = fold(query.strip())
    if not query:
        return []
    exact = [o for o in objects if fold(o['label']) == query]
    return exact or [o for o in objects if query in fold(o['hover']) or query in fold(o['label'])]
