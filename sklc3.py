import streamlit as st
from excel_renderer import build_floor_figure, sheet_names
from map_objects import normalize_floor, search_objects
from map_renderer import build_map_figure

st.set_page_config(page_title='WMS Layout Skladu',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
.stApp {background-color:#0b0f19;color:#f8fafc;}
h1 {color:#f8fafc;font-family:'Segoe UI',sans-serif;font-weight:600;}
</style>''',unsafe_allow_html=True)
st.title('🏭 Layout Skladu – SKLC3')
with st.sidebar:
    floor=st.selectbox('Poschodie',sheet_names())
    mode=st.radio('Zobrazenie',['Mapa','Excel debug'])
    query=st.text_input('Vyhľadať lokáciu alebo stanicu',placeholder='BPO30, 4F-12, WC…')
    objects=normalize_floor(floor)['objects']
    matches=search_objects(objects,query)
    selected_id=None
    if query:
        if not matches:
            st.info('Nenašla sa žiadna lokácia na tomto poschodí.')
        else:
            st.caption(f'Nájdené objekty: {len(matches)}')
            selected_id=st.selectbox('Výsledok', [o['id'] for o in matches],
                                     format_func=lambda value:next(o['hover'] for o in matches if o['id']==value))
    fit=st.checkbox('Fit to screen',value=True)
    if st.button('Reset view',use_container_width=True):
        st.session_state['view_revision']=st.session_state.get('view_revision',0)+1
        st.session_state['reset_search']=query
    helpers=st.checkbox('Zobraziť pomocné číselné značky',value=False) if mode=='Excel debug' else False
revision=st.session_state.get('view_revision',0)
reset_query=st.session_state.get('reset_search')
active_query='' if reset_query==query else query
if reset_query is not None and reset_query!=query:
    st.session_state.pop('reset_search',None)
if mode=='Mapa':
    figure=build_map_figure(floor,active_query,selected_id,revision,fit)
else:
    figure=build_floor_figure(floor,helpers)
    figure.update_layout(uirevision=f'{floor}:debug:{revision}:{fit}:{active_query}:{selected_id}',height=600 if fit else 850)
    figure.update_xaxes(fixedrange=False)
    figure.update_yaxes(fixedrange=False)
    if active_query and matches:
        selected=next((o for o in matches if o['id']==selected_id),matches[0])
        x,y,w,h=selected['x'],selected['y'],selected['w'],selected['h']
        padding=max(w,h,normalize_floor(floor)['width']*.025)*.45
        figure.add_shape(type='rect',x0=x,y0=-y-h,x1=x+w,y1=-y,
                         fillcolor='rgba(0,0,0,0)',line=dict(color='#facc15',width=3))
        figure.update_xaxes(range=[x-padding,x+w+padding])
        figure.update_yaxes(range=[-y-h-padding,-y+padding])
st.caption('Koliesko: zoom · potiahnutie: posun · detaily objektov: hover · Reset view: celé poschodie')
st.plotly_chart(figure,width='stretch',key=f'layout-{floor}-{mode}',
                config={'scrollZoom':True,'displayModeBar':True,'displaylogo':False,
                        'modeBarButtonsToRemove':['select2d','lasso2d']})
