import streamlit as st
import json
from util import *


kb = json.load(open('kb.json', 'r'))

def hero_section():
    st.markdown('# 🤸 gymnastics expert system')
    st.markdown('')
    st.info('This project has been implemented in the context of [Knowledge Technology Practical](https://www.rug.nl/ocasys/fwn/vak/show?code=WBAI014-05).')
    st.markdown('---')


def notes_section(parent):
    parent.markdown('### notes')
    st.session_state['small_mistakes'] = parent.number_input('small mistakes', step=1, value=st.session_state['small_mistakes'])
    st.session_state['big_mistakes'] = parent.number_input('big mistakes', step=1, value=st.session_state['big_mistakes'])
    st.session_state['falls'] = parent.number_input('falls', step=1, value=st.session_state['falls'])
    st.session_state['connections'] = parent.number_input('connections', step=1, value=st.session_state['connections'])
    

def choose_elements():
    elements = kb['apparatuses']['beam']['elements']
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

    st.session_state['selected_elements'] = [selected_mount] + selected_jumps + selected_dances + selected_acros + [selected_dismount]
    st.session_state['selected_elements'] = [(e, elements[e]) for e in st.session_state['selected_elements']]

    notes_section(col3)

    missed_elements = 6 - (2 + len(selected_jumps) + len(selected_dances) + len(selected_acros))
    
    st.markdown('---')
    if st.button('Next'):
        st.session_state['state'] = 'element_walkthrough'
        st.experimental_rerun()


def detail_element(element):
    st.subheader(element[0])
    for question in element[1]['element_questions']:
        option = st.radio(question['question'], question['options'].keys())
    if st.button('Next'):
        st.session_state['current_element'] += 1
        st.experimental_rerun()


def apparatus_mistakes():
    mistakes = kb['apparatuses']['beam']['mistakes']
    st.subheader('apparatus mistakes')
    for question in mistakes:
        option = st.radio(question['question'], question['options'].keys())
    if st.button('Next'):
        st.session_state['state'] = 'general_execution_mistakes'
        st.experimental_rerun()


def general_execution_mistakes():
    st.subheader('general execution mistakes')
    mistakes = kb['general_execution_mistakes']
    
    for mistake in mistakes.items():
        option = st.radio(mistake[0], ['none'] + mistake[1])
        if option == 'small':
            st.session_state['execution'] -= 0.1
        elif option == 'medium':
            st.session_state['execution'] -= 0.3
        elif option == 'big':
            st.session_state['execution'] -= 0.5

    if st.button('Next'):
        st.session_state['state'] = 'general_landing_mistakes'
        st.experimental_rerun()


def general_landing_mistakes():
    st.subheader('general landing mistakes')
    mistakes = kb['general_landing_mistakes']
    
    for mistake in mistakes.items():
        option = st.radio(mistake[0], ['none'] + mistake[1])
        if option == 'small':
            st.session_state['execution'] -= 0.1
        elif option == 'medium':
            st.session_state['execution'] -= 0.3
        elif option == 'big':
            st.session_state['execution'] -= 0.5

    if st.button('Next'):
        st.session_state['state'] = 'general_mistakes'
        st.experimental_rerun()


def general_mistakes():
    st.subheader('general mistakes')
    mistakes = kb['general_mistakes']
    
    for mistake in mistakes.items():
        option = st.radio(mistake[0], ['none'] + mistake[1])
        if option == 'small':
            st.session_state['execution'] -= 0.1
        elif option == 'medium':
            st.session_state['execution'] -= 0.3
        elif option == 'big':
            st.session_state['execution'] -= 0.5

    if st.button('Next'):
        st.session_state['state'] = 'artistry'
        st.experimental_rerun()


def artistry():
    st.subheader('artistry')
    mistakes = kb['artistry']
    
    for mistake in mistakes:
        option = st.checkbox(mistake)
        if option:
            st.session_state['execution'] -= 0.1

    if st.button('Next'):
        st.session_state['state'] = 'combos'
        st.experimental_rerun()


def combos():
    st.subheader('element combinations')
    elems = st.session_state['selected_elements']
    
    for elem_idx in range(len(elems) - 1):
        st.radio(elems[elem_idx][0] + ' + ' + elems[elem_idx + 1][0] + '?', ['no', 'yes'])

    if st.button('Next'):
        st.session_state['state'] = 'combos'
        st.experimental_rerun()
