import streamlit as st
import json
from util import *
import pandas as pd


kb = json.load(open('kb.json', 'r'))


def hero_section():
    st.markdown('# 🤸 gymnastics expert system')
    st.markdown('')
    st.info(
        'This project has been implemented in the context of [Knowledge Technology Practical](https://www.rug.nl/ocasys/fwn/vak/show?code=WBAI014-05).')
    st.markdown('---')


def notes_section(parent):
    parent.markdown('### notes')
    st.session_state['small_mistakes'] = parent.number_input(
        'small mistakes', step=1, value=st.session_state['small_mistakes'])
    st.session_state['big_mistakes'] = parent.number_input(
        'big mistakes', step=1, value=st.session_state['big_mistakes'])
    st.session_state['falls'] = parent.number_input(
        'falls', step=1, value=st.session_state['falls'])
    st.session_state['connections'] = parent.number_input(
        'connections', step=1, value=st.session_state['connections'])


def choose_elements():
    elements = kb['apparatuses']['beam']['elements']
    mounts = filter_dict(elements, lambda x: x[1]['element_type'] == 'mount')
    jumps = filter_dict(elements, lambda x: x[1]['element_type'] == 'jump')
    dances = filter_dict(elements, lambda x: x[1]['element_type'] == 'dance')
    acros = filter_dict(elements, lambda x: x[1]['element_type'] == 'acro')
    dismounts = filter_dict(elements, lambda x: ' dismount' in x[0])

    col1, col2, col3 = st.columns([1, 1, 1])
    selected_mount = col1.radio(
        'What mount element is the gymnast performing?', mounts)

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

    selected_dismount = col2.radio(
        'What dismount is the gymnast performing?', dismounts)

    st.session_state['selected_elements'] = [selected_mount] + \
        selected_jumps + selected_dances + selected_acros + [selected_dismount]
    st.session_state['selected_elements'] = [
        (e, elements[e]) for e in st.session_state['selected_elements']]

    notes_section(col3)

    missed_elements = 6 - (2 + len(selected_jumps) +
                           len(selected_dances) + len(selected_acros))

    st.markdown('---')
    if st.button('Next'):
        st.session_state['state'] = 'element_walkthrough'
        st.experimental_rerun()


def detail_element(element):
    if 'difficulty' not in st.session_state.keys():
        st.session_state['difficulty'] = 0

    st.subheader(element[0])
    difficulty = element[1].get('difficulty', None)
    if difficulty is not None:
        if difficulty in ['TA', 'A']:
            st.session_state['difficulty'] += 0.1
        elif difficulty == 'B':
            st.session_state['difficulty'] += 0.2

    for question in element[1]['element_questions']:
        option = st.radio(question['question'], question['options'].keys())
        difficulty = question['options'][option].get('difficulty', None)
        if difficulty is not None:
            if difficulty in ['TA', 'A']:
                st.session_state['difficulty'] += 0.1
            elif difficulty == 'B':
                st.session_state['difficulty'] += 0.2

    st.session_state['selected_elements'][st.session_state['current_element']
                                          ][1]['difficulty'] = difficulty

    if st.button('Next'):
        st.session_state['current_element'] += 1
        st.experimental_rerun()


def apparatus_mistakes():
    if 'execution' not in st.session_state.keys():
        st.session_state['execution'] = 0

    mistakes = kb['apparatuses']['beam']['mistakes']
    st.subheader('apparatus mistakes')
    for question in mistakes:
        option = st.radio(question['question'], question['options'].keys())
        if option == 'small':
            st.session_state['execution'] -= 0.1
        elif option == 'medium':
            st.session_state['execution'] -= 0.3
        elif option == 'big':
            st.session_state['execution'] -= 0.5
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
    if 'artistry' not in st.session_state.keys():
        st.session_state['artistry'] = 0

    st.subheader('artistry')
    mistakes = kb['artistry']

    for mistake in mistakes:
        option = st.checkbox(mistake)
        if option:
            st.session_state['artistry'] -= 0.1

    if st.button('Next'):
        st.session_state['state'] = 'combos'
        st.experimental_rerun()


def combos():
    if 'combo' not in st.session_state.keys():
        st.session_state['combo'] = 0

    elems = st.session_state['selected_elements']
    st.subheader('element combinations')

    for elem in elems:
        other_elems = [e for e in elems if e != elem]

        option = st.radio(elem[0], ['none'] + [e[0] for e in other_elems])
        if option != 'none':
            if 'B' in [elem[0], [other_elem for other_elem in other_elems if other_elem[0] == option]]:
                st.session_state['combo'] += 0.2
            else:
                st.session_state['combo'] += 0.1

    if st.button('Next'):
        st.session_state['state'] = 'results'
        st.experimental_rerun()


def skill_requirements():
    if 'reqs' not in st.session_state.keys():
        st.session_state['reqs'] = 0

    elems = st.session_state['selected_elements']
    srs = 0

    srs += len([e for e in elems if 'turn' in e[0]]) > 0
    srs += len([e for e in elems if e[1]['element_type'] ==
               'acro' and e[1]['difficulty'] in ['A', 'B']]) > 0
    srs += len([e for e in elems if e[0] in ['handstand (1 sec)', 'handstand (2 sec)',
               'cartwheel', 'roundoff', 'handstand to forward roll']]) > 0

    st.session_state['reqs'] = srs * 0.5


def results():
    skill_requirements()

    st.subheader('results')
    dscore = st.session_state['difficulty'] + \
        st.session_state['combo'] + st.session_state['reqs']
    escore = 10 + st.session_state['execution'] + st.session_state['artistry']

    results = pd.DataFrame([
        ['difficulty score (DS)', st.session_state['difficulty']],
        ['combo bonus (CB)', st.session_state['combo']],
        ['skill requirements (SR)', st.session_state['reqs']],
        ['execution', st.session_state['execution']],
        ['artistry', st.session_state['artistry']],
        ['D-score', dscore],
        ['E-score', escore],
    ], columns=['rubric', 'score'])

    st.dataframe(results)
