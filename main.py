import streamlit as st
from components import *
from util import *

# To run code, use: streamlit run main.py

st.set_page_config(
    page_title='gymnastics expert system',
    layout='wide'
)

print('---')

init_session_state()
hero_section()

if st.session_state['state'] == 'choose_elements':
    choose_elements()
else:
    if st.session_state['state'] == 'element_walkthrough':
        if st.session_state['current_element'] < len(st.session_state['selected_elements']):
            element = st.session_state['selected_elements'][st.session_state['current_element']]
            detail_element(element)
        else:
            st.session_state['state'] = 'general_mistakes'
            st.experimental_rerun()
    elif st.session_state['state'] == 'general_mistakes':
        general_mistakes()
    elif st.session_state['state'] == 'artistry':
        artistry()
    elif st.session_state['state'] == 'results':
        results()
