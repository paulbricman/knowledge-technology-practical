import streamlit as st
from components import *
from util import *


st.set_page_config(
        page_title='gymnastics expert system',
        layout='wide'
    )

init_session_state()
hero_section()

if st.session_state['state'] == 'choose_elements':
    choose_elements()
else:
    if st.session_state['current_element'] < len(st.session_state['selected_elements']):
        element = st.session_state['selected_elements'][st.session_state['current_element']]
        if 'element_questions' in element[1].keys():
            detail_element(element)
        else:
            st.session_state['current_element'] += 1
            st.experimental_rerun()
    else:
        if st.session_state['state'] not in ['general_execution_mistakes', 'general_landing_mistakes', 'general_mistakes', 'artistry', 'combos', 'results']:
            apparatus_mistakes()
        elif st.session_state['state'] == 'general_execution_mistakes':
            general_execution_mistakes()
        elif st.session_state['state'] == 'general_landing_mistakes':
            general_landing_mistakes()
        elif st.session_state['state'] == 'general_mistakes':
            general_mistakes()
        elif st.session_state['state'] == 'artistry':
            artistry()
        elif st.session_state['state'] == 'combos':
            combos()
        elif st.session_state['state'] == 'results':
            results()
        