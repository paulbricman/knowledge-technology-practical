import streamlit as st
import json
from util import *


kb = json.load(open('kb.json', 'r'))

def hero_section():
    st.markdown('# 🤸 gymnastics expert system')
    st.markdown('')
    st.info('This project has been implemented in the context of [Knowledge Technology Practical](https://www.rug.nl/ocasys/fwn/vak/show?code=WBAI014-05).')
    st.markdown('---')


def choose_elements():
    elements = kb['beam']
    mounts = filter_dict(elements, lambda x: x[1]['element_type'] == 'mount')
    jumps = filter_dict(elements, lambda x: x[1]['element_type'] == 'jump')
    dances = filter_dict(elements, lambda x: x[1]['element_type'] == 'dance')
    acros = filter_dict(elements, lambda x: x[1]['element_type'] == 'acro')
    dismounts = filter_dict(elements, lambda x: ' dismount' in x[0])

    col1, col2, col3 = st.columns([1, 1, 1])
    selected_mount = col1.radio('What mount element is the gymnast performing?', mounts)

    col1.caption('What jump elements is the gymnast performing?')
    selected_jumps = []
    for jump in jumps:
        if col1.checkbox(jump):
            selected_jumps += [jump]

    col1.caption('What dance elements is the gymnast performing?')
    selected_dances = []
    for dance in dances:
        if col1.checkbox(dance):
            selected_dances += [dance]

    col2.caption('What acro elements is the gymnast performing?')
    selected_acros = []
    for acro in acros:
        if col2.checkbox(acro):
            selected_acros += [acro]

    selected_dismount = col2.radio('What dismount is the gymnast performing?', dismounts)

    
    
    col3.markdown('### notes')
    small_mistakes = col3.number_input('small mistakes', step=1)
    big_mistakes = col3.number_input('big mistakes', step=1)
    falls = col3.number_input('falls', step=1)
    connections = col3.number_input('connections', step=1)

    missed_elements = 6 - (2 + len(selected_jumps) + len(selected_dances) + len(selected_acros))
    
    st.markdown('---')
    if st.button('Next'):
        st.balloons()