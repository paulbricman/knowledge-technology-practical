import streamlit as st
import json
from util import *
import pandas as pd


kb = json.load(open('kb.json', 'r'))


def hero_section():
    st.markdown('# 🤸 Gymnastics Expert System')
    st.markdown('')
    st.info(
        'This project has been implemented in the context of [Knowledge Technology Practical](https://www.rug.nl/ocasys/fwn/vak/show?code=WBAI014-05).')
    st.markdown('---')


def notes_section(parent):
    parent.markdown('### Notes')
    st.session_state['small_mistakes'] = parent.number_input(
        'Small mistakes', min_value=0, step=1, value=st.session_state['small_mistakes'])
    st.session_state['big_mistakes'] = parent.number_input(
        'Big mistakes', min_value=0, step=1, value=st.session_state['big_mistakes'])
    st.session_state['falls'] = parent.number_input(
        'Falls', min_value=0, step=1, value=st.session_state['falls'])
    st.session_state['connections'] = parent.number_input(
        'Connections', min_value=0, step=1, value=st.session_state['connections'])


def choose_elements():
    elements = kb['apparatuses']['beam']['elements']
    mounts = filter_dict(elements, lambda x: x[1]['element_type'] == 'mount')
    jumps = filter_dict(elements, lambda x: x[1]['element_type'] == 'jump')
    dances = filter_dict(elements, lambda x: x[1]['element_type'] == 'dance')
    acros = filter_dict(elements, lambda x: x[1]['element_type'] == 'acro')
    dismounts = filter_dict(elements, lambda x: ' dismount' in x[0])


    col1, col2, col3 = st.columns([1, 1, 1])
    selected_mount = col1.radio(
        'What mount is the gymnast performing?', mounts)

    col1.caption('What jumps is the gymnast performing?')
    selected_jumps = []
    for jump in jumps:
        if col1.checkbox(jump):
            selected_jumps += [jump]

    col1.caption('What turns is the gymnast performing?')
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

    st.markdown('---')
    if st.button('Next'):
        st.session_state['state'] = 'element_walkthrough'
        st.experimental_rerun()


def detail_element(element):
    cols = st.columns([3, 3, 1])
    notes = f'''    - small mistakes: {st.session_state["small_mistakes"]}
    - big mistakes: {st.session_state["big_mistakes"]}
    - falls: {st.session_state["falls"]}
    - connections: {st.session_state["connections"]}
    '''
    cols[2].info(notes)

    if 'difficulty' not in st.session_state.keys():
        st.session_state['difficulty'] = 0
    if 'execution' not in st.session_state.keys():
        st.session_state['execution'] = 0

    st.session_state['selected_elements'][st.session_state['current_element']
    ][1]['valid'] = 1

    cols[0].header(element[0])
    st.session_state['selected_elements'][st.session_state['current_element']
                                          ][1]['info_element_questions'] = []
    difficulty = element[1].get('difficulty', None)

    for question in element[1].get('element_questions', []):
        option = cols[0].radio(question['question'],
                               question['options'].keys(), key=element[0])

        st.session_state['selected_elements'][st.session_state['current_element']
                                              ][1]['info_element_questions'] += [[question['question'], option]]

        difficulty = question['options'][option].get('difficulty', None)

    st.session_state['selected_elements'][st.session_state['current_element']
                                          ][1]['difficulty'] = difficulty

    cols[0].subheader('Execution:')
    mistakes = list(kb['general_execution_mistakes'].items())
    relevant_mistakes = []
    for e_idx in element[1].get('execution_mistakes', []):
        relevant_mistakes += [mistakes[e_idx - 1]]

    st.session_state['selected_elements'][st.session_state['current_element']
                                          ][1]['info_execution_mistakes'] = []

    for mistake in relevant_mistakes:
        if len(mistake[1]) > 1:
            option = cols[0].radio(mistake[0], ['none'] +
                                   mistake[1], key=element[0])
        else:
            option = cols[0].checkbox(mistake[0])
            if option:
                option = mistake[1]
            else:
                option = 'none'

        st.session_state['selected_elements'][st.session_state['current_element']
                                              ][1]['info_execution_mistakes'] += [[mistake[0], option]]

    cols[1].subheader('Landing:')
    mistakes = list(kb['general_landing_mistakes'].items())
    relevant_mistakes = []
    for e_idx in element[1].get('landing_mistakes', []):
        relevant_mistakes += [mistakes[e_idx - 1]]

    st.session_state['selected_elements'][st.session_state['current_element']
                                          ][1]['info_landing_mistakes'] = []

    for mistake in relevant_mistakes:
        if len(mistake[1]) > 1:
            option = cols[1].radio(mistake[0], ['none'] +
                                   mistake[1], key=element[0])
        else:
            option = cols[1].checkbox(mistake[0])
            if option:
                option = mistake[1]
            else:
                option = 'none'
        st.session_state['selected_elements'][st.session_state['current_element']
                                              ][1]['info_landing_mistakes'] += [[mistake[0], option]]

    #Specific code for falls
    check = cols[1].checkbox("Fall")
    if check:
        nstd_check = cols[1].checkbox("Element not landed on feet first")
        if nstd_check:
            #-1 and no DS CB and SR
            st.session_state['selected_elements'][st.session_state['current_element']][1]['valid'] = 0
            st.session_state['selected_elements'][st.session_state['current_element']
            ][1]['info_landing_mistakes'] += [['Fall(not landed)', 'very big']]
        else:
            st.session_state['selected_elements'][st.session_state['current_element']
            ][1]['info_landing_mistakes'] += [['Fall', 'very big']]
    else:
        st.session_state['selected_elements'][st.session_state['current_element']
        ][1]['info_landing_mistakes'] += [['Fall', 'none']]


    cols[0].subheader('Combination:')
    combo_option = cols[0].selectbox('Was this element combined with another one?', [
                                 'none'] + [e[0] for e in st.session_state['selected_elements']], key=element[0])
    st.session_state['selected_elements'][st.session_state['current_element']
                                          ][1]['info_combo'] = combo_option

    if st.button('Next'):
        st.session_state['current_element'] += 1
        st.experimental_rerun()

# This function is unused
'''
def apparatus_mistakes():
    if 'execution' not in st.session_state.keys():
        st.session_state['execution'] = 0

    mistakes = kb['apparatuses']['beam']['mistakes']
    st.subheader('Apparatus specific mistakes')
    for question in mistakes:
        option = st.radio(question['question'], question['options'].keys())
        if option == 'small':
            st.session_state['execution'] -= 0.1
        elif option == 'medium':
            st.session_state['execution'] -= 0.3
        elif option == 'big':
            st.session_state['execution'] -= 0.5
        elif option == 'very big':
            st.session_state['execution'] -= 1.0
    if st.button('Next'):
        st.session_state['state'] = 'general_mistakes'
        st.experimental_rerun()
'''

def general_mistakes():
    st.subheader('General mistakes')
    mistakes = kb['general_mistakes']
    st.session_state['general_mistakes'] = []

    for mistake in mistakes.items():
        #option = st.radio(mistake[0], ['none'] + mistake[1])
        #st.session_state['general_mistakes'] += [[mistake[0], option]]

        #@paul can you check whether here the correct value is deducted?
        #As in: if the duration is longer than 1:20 it should deduct small and help from trainer
        #is -1 + no DS/CB/SR etc
        option = st.checkbox(mistake[0])
        if option:
            option = mistake[1]
        else:
            option = 'none'
        st.session_state['general_mistakes'] += [[mistake[0], option]]

        if option == 'small':
            st.session_state['execution'] -= 0.1
        elif option == 'medium':
            st.session_state['execution'] -= 0.3
        elif option == 'big':
            st.session_state['execution'] -= 0.5
        elif option == 'very big':
            st.session_state['execution'] -= 1.0

    if st.button('Next'):
        st.session_state['state'] = 'artistry'
        st.experimental_rerun()


def artistry():
    if 'artistry' not in st.session_state.keys():
        st.session_state['artistry'] = 0

    st.subheader('Artistry')
    mistakes = kb['artistry']
    st.session_state['artistry_mistakes'] = []

    for mistake in mistakes:
        option = st.checkbox(mistake)
        st.session_state['artistry_mistakes'] += [[mistake, option]]

    if st.button('Next'):
        st.session_state['state'] = 'results'
        st.experimental_rerun()


def compute_skill_requirements():
    elems = st.session_state['selected_elements']
    srs = [None] * 4
    # This requirement is not valid - need comparison with 180º
    srs[0] = False
    for elem in st.session_state['selected_elements']:
        # go through all elements
        if elem[1]['element_type'] == ('dance' or 'jump'):
            # if element is a turn or a jump check if a combination is done
            if elem[1]['info_combo'] != 'none':
                # Combo found
                flag = 0
                for l in elem[1]['info_landing_mistakes']:
                    # check whether this first element of the combination had a
                    # landing mistake(the combo doesn't count then)
                    if l[1] != 'none':
                        # there is a landing mistake so combo doesnt count
                        flag = 1
                if flag == 0:
                    # 1st element counts towards combo, now find 2nd element
                    comboed_elem = [
                        e for e in st.session_state['selected_elements'] if e[0] == elem[1]['info_combo']][0]
                    if comboed_elem[1]['element_type'] == ('dance' or 'jump'):
                        # 2nd element follows dance requirement
                        flag1 == 0
                        for l in comboed_elem[1]['info_landing_mistakes']:
                            # check whether this second element of the combination had a
                            # landing mistake(the combo doesn't count then)
                            if l[1] == 'very big':
                                # there was a fall so combo doesnt count
                                flag1 = 1
                        if flag1 == 0:
                            # 2nd element counts towards combo now check whether there was a jump at 180
                            if elem[1]['element_type'] == ('Split jump' or 'Split leap'):
                                for q in elem[1]['info_element_questions']:
                                    if q[0] == 'What was the deviation from a 180º splits?':
                                        if q[1] == '0º':
                                            srs[0] = True
                                            break
                            if comboed_elem[1]['element_type'] == ('Split jump' or 'Split leap'):
                                for q in elem[1]['info_element_questions']:
                                    if q[0] == 'What was the deviation from a 180º splits?':
                                        if q[1] == '0º':
                                            srs[0] = True
                                            break


    srs[1] = len([e for e in elems if 'turn' in e[0]]) > 0
    srs[2] = len([e for e in elems if e[1]['element_type'] ==
                  'acro' and e[1]['difficulty'] in ['A', 'B']]) > 0
    srs[3] = len([e for e in elems if e[0] in ['handstand (1 sec)', 'handstand (2 sec)',
                                               'cartwheel', 'roundoff', 'handstand to forward roll']]) > 0

    return sum(srs) * 0.5, srs


def compute_combo_bonus():
    cb = []
    cbs = []

    for elem in st.session_state['selected_elements']:
        if elem[1]['info_combo'] != 'none':
            comboed_elem = [
                e for e in st.session_state['selected_elements'] if e[0] == elem[1]['info_combo']][0]
            if ['A', 'B'] == sorted([elem[1]['difficulty'], comboed_elem[1]['difficulty']]):
                cb += [0.2]
                cbs += [[elem[0], comboed_elem[0]]]
            elif ['A', 'A'] == sorted([elem[1]['difficulty'], comboed_elem[1]['difficulty']]):
                cb += [0.1]
                cbs += [[elem[0], comboed_elem[0]]]

    return cb, cbs


def compute_difficulty_score():
    elems = [[e[0], e[1]['difficulty']]
             for e in st.session_state['selected_elements']]

    difficulty = 0
    for elem in elems:
        if elem[1] in ['TA', 'A']:
            difficulty += 0.1
        else:
            difficulty += 0.2

    return difficulty, elems


def compute_artistry():
    artistry = 0
    mistakes = st.session_state['artistry_mistakes']

    for mistake in mistakes:
        if mistake[1] == True:
            artistry -= 0.1

    return artistry, [e[0] for e in mistakes if e[1] == True]


def compute_execution():
    general_mistakes = st.session_state['general_mistakes']
    element_mistakes = []
    execution = 0

    for mistake in general_mistakes:
        if mistake[1] == 'small':
            execution -= 0.1
        elif mistake[1] == 'middle':
            execution -= 0.3
        elif mistake[1] == 'big':
            execution -= 0.5

    for elem in st.session_state['selected_elements']:
        for mistake in elem[1]['info_execution_mistakes']:
            if mistake[1] != 'none':
                element_mistakes += [[elem[0], mistake[0], mistake[1]]]

            if mistake[1] == 'small':
                execution -= 0.1
            elif mistake[1] == 'middle':
                execution -= 0.3
            elif mistake[1] == 'big':
                execution -= 0.5

        for mistake in elem[1]['info_landing_mistakes']:
            if mistake[1] != 'none':
                element_mistakes += [[elem[0], mistake[0], mistake[1]]]

            if mistake[1] == 'small':
                execution -= 0.1
            elif mistake[1] == 'middle':
                execution -= 0.3
            elif mistake[1] == 'big':
                execution -= 0.5
            elif mistake[1] == 'very big':
                execution -= 1.0

    return execution, [e[0] for e in general_mistakes if e[1] != 'none'], element_mistakes


def compute_n_score():
    elem_count = len(st.session_state['selected_elements'])
    if elem_count in [4, 5]:
        return -4
    elif elem_count in [2, 3]:
        return -6
    elif elem_count == 1:
        return -8
    elif elem_count == 0:
        return -10


def results():
    st.header('results')

    st.subheader('DS')
    st.write(compute_difficulty_score())
    st.subheader('SR')
    st.write(compute_skill_requirements())
    st.subheader('CB')
    st.write(compute_combo_bonus())
    st.subheader('artistry')
    st.write(compute_artistry())
    st.subheader('execution')
    st.write(compute_execution())
    st.subheader('n score')
    st.write(compute_n_score())

    # st.subheader('results')
    # dscore = st.session_state['difficulty'] + \
    #     st.session_state['combo'] + st.session_state['reqs']
    # escore = 10 + st.session_state['execution'] + st.session_state['artistry']

    # results = pd.DataFrame([
    #     ['difficulty score (DS)', st.session_state['difficulty']],
    #     ['combo bonus (CB)', st.session_state['combo']],
    #     ['skill requirements (SR)', st.session_state['reqs']],
    #     ['execution', st.session_state['execution']],
    #     ['artistry', st.session_state['artistry']],
    #     ['D-score', dscore],
    #     ['E-score', escore],
    # ], columns=['rubric', 'score'])

    # st.dataframe(results)
