import streamlit as st

from excel_renderer import render_excel_floor, sheet_names

st.set_page_config(page_title='WMS Layout Skladu', layout='wide',
                   initial_sidebar_state='collapsed')
st.markdown('''
<style>
.stApp { background-color: #0b0f19; color: #f8fafc; }
h1 { color: #f8fafc; font-family: 'Segoe UI', Roboto, sans-serif;
     font-weight: 600; letter-spacing: -0.5px; }
</style>
''', unsafe_allow_html=True)
st.title('🏭 Layout Skladu – SKLC3')
floor = st.radio('Poschodie', sheet_names(), horizontal=True)
show_helpers = st.checkbox('Zobraziť pomocné číselné značky', value=False)
st.caption('Kolieskom myši priblížiš mapu, potiahnutím ju posunieš. Dvojklik obnoví celkový pohľad.')
render_excel_floor(floor, show_helpers)
