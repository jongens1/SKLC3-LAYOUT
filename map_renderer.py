"""Layered warehouse-map rendering, independent of the Excel debug renderer."""
import html
import plotly.graph_objects as go
from map_objects import normalize_floor, search_objects

STYLES = {
    'zone': ('#243449', '#52647c'),
    'station': ('#21485a', '#5ca8bd'),
    'rack': ('#3b344c', '#8d7ba7'),
    'block': ('#303e4b', '#586b7a'),
    'conveyor': ('#367d91', '#64c5d4'),
    'infra': ('#695436', '#d3ae6c'),
}
LAYERS = ['block','zone','rack','station','conveyor','infra']


def rounded_path(x, y, w, h):
    y = -y-h
    r = min(w,h)*0.12
    return (f'M {x+r},{y} L {x+w-r},{y} Q {x+w},{y} {x+w},{y+r} '
            f'L {x+w},{y+h-r} Q {x+w},{y+h} {x+w-r},{y+h} '
            f'L {x+r},{y+h} Q {x},{y+h} {x},{y+h-r} '
            f'L {x},{y+r} Q {x},{y} {x+r},{y} Z')


def object_path(obj):
    if obj.get('parts'):
        return ' '.join(f'M {a},{-b} L {c},{-b} L {c},{-d} L {a},{-d} Z'
                        for a,b,c,d,_ in obj['parts'])
    return rounded_path(obj['x'],obj['y'],obj['w'],obj['h'])


def visible_label(obj, screen_width, x_span):
    label = obj['label']
    if not label:
        return ''
    width_px = obj['w']*screen_width/x_span
    height_px = obj['h']*screen_width/x_span
    if width_px < 22 or height_px < 12:
        return ''
    if obj['type']=='infra':
        label = label.replace('Schody','↗ Schody').replace('SCHODY','↗ SCHODY').replace('Výťah','↕ Výťah')
    if len(label)*6 > width_px:
        if obj['type']=='rack' and width_px >= 26:
            return label[:max(3,int(width_px/6)-1)]+'…'
        return ''
    return label


def build_map_figure(sheet_name, query='', selected_id=None, revision=0, fit=True):
    floor = normalize_floor(sheet_name)
    objects = floor['objects']
    matches = search_objects(objects, query)
    selected = next((o for o in matches if o['id']==selected_id), matches[0] if len(matches)==1 else None)
    highlighted = {o['id'] for o in matches}
    xr,yr = [0,floor['width']],[-floor['height'],0]
    if selected:
        padding=max(selected['w'],selected['h'],floor['width']*.025)*.45
        xr=[selected['x']-padding,selected['x']+selected['w']+padding]
        yr=[-selected['y']-selected['h']-padding,-selected['y']+padding]
    shapes=[dict(type='path',path=rounded_path(0,0,floor['width'],floor['height']),
                 fillcolor='#172331',line=dict(color='#42566b',width=1),layer='below')]
    annotations=[]
    visible=[o for o in objects if not o.get('parent_id') or o['id'] in highlighted]
    ordered=sorted(visible,key=lambda o:LAYERS.index(o['type']))
    for obj in ordered:
        fill,border=STYLES[obj['type']]
        # Source hue is retained as a muted overlay, with a consistent type border.
        source=obj['color'].lstrip('#')
        rgb=[int(source[i:i+2],16) for i in (0,2,4)]
        fill='rgb('+','.join(str(round(v*.25+b*.75)) for v,b in zip(rgb,(30,43,59)))+')'
        if obj['type']=='infra': fill=STYLES['infra'][0]
        if obj['id'] in highlighted: border='#facc15'
        shapes.append(dict(type='path',path=object_path(obj),fillcolor=fill,
                           line=dict(color=border,width=3 if obj['id'] in highlighted else 0 if obj.get('parts') else 1),layer='below'))
        label=visible_label(obj,1300,xr[1]-xr[0])
        if label:
            annotations.append(dict(x=obj['x']+obj['w']/2,y=-obj['y']-obj['h']/2,
                                    text=html.escape(label),showarrow=False,textangle=0,
                                    font=dict(color='#e8eef6',size=14 if obj['id'] in highlighted else 12 if obj['type']=='zone' else 10)))
    fig=go.Figure()
    fig.add_trace(go.Scatter(
        x=[o['x']+o['w']/2 for o in ordered],
        y=[-o['y']-o['h']/2 for o in ordered], mode='markers',
        marker=dict(color='rgba(255,255,255,0.001)',
                    size=[max(18,min(100,min(o['w'],o['h'])*1300/(xr[1]-xr[0]))) for o in ordered]),
        text=[html.escape(o['hover']) for o in ordered],
        hovertemplate='%{text}<extra></extra>',showlegend=False))
    fig.update_layout(shapes=shapes,annotations=annotations,
                      height=600 if fit else 850,margin=dict(l=10,r=10,t=10,b=10),
                      paper_bgcolor='#0b0f19',plot_bgcolor='#0b0f19',showlegend=False,
                      dragmode='pan',uirevision=f'{sheet_name}:map:{revision}:{query}:{selected_id}:{fit}',
                      xaxis=dict(visible=False,showgrid=False,range=xr,fixedrange=False,constrain='domain'),
                      yaxis=dict(visible=False,showgrid=False,range=yr,fixedrange=False,
                                 scaleanchor='x',scaleratio=1,constrain='domain'),
                      hoverlabel=dict(bgcolor='#243449',font_color='#f8fafc'))
    return fig
