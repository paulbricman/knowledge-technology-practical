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
    notes_section(cols[2])

    if 'difficulty' not in st.session_state.keys():
        st.session_state['difficulty'] = 0

    st.session_state['selected_elements'][st.session_state['current_element']
                                          ][1]['valid'] = 1

    cols[0].header(element[0])
    st.session_state['selected_elements'][st.session_state['current_element']
                                          ][1]['info_element_questions'] = []
    difficulty = st.session_state['selected_elements'][st.session_state['current_element']][1].get(
        'difficulty', None)

    for question in element[1].get('element_questions', []):
        if isinstance(question['options'], list):
            option = cols[0].radio(question['question'],
                                   question['options'], key=element[0])
        else:
            option = cols[0].radio(question['question'],
                                   question['options'].keys(), key=element[0])

        st.session_state['selected_elements'][st.session_state['current_element']
                                              ][1]['info_element_questions'] += [[question['question'], option]]

        difficulty = question['options'][option].get('difficulty', difficulty)

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
            option = cols[0].checkbox(mistake[0], key=element[0])
            if option:
                option = mistake[1]
                if mistake[0] == 'Help from trainer':
                    st.session_state['selected_elements'][st.session_state['current_element']][1]['valid'] = 0
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
            option = cols[1].checkbox(mistake[0], key=element[0])
            if option:
                option = mistake[1]
            else:
                option = 'none'
        st.session_state['selected_elements'][st.session_state['current_element']
                                              ][1]['info_landing_mistakes'] += [[mistake[0], option]]

    # Specific code for falls
    check = cols[1].checkbox("Fall", key=element[0])
    if check:
        nstd_check = cols[1].checkbox("Element not landed on feet first")
        if nstd_check:
            # -1 and no DS CB and SR
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


def general_mistakes():
    st.subheader('General mistakes')
    mistakes = kb['general_mistakes']
    st.session_state['general_mistakes'] = []

    for mistake in mistakes.items():
        # option = st.radio(mistake[0], ['none'] + mistake[1])
        # st.session_state['general_mistakes'] += [[mistake[0], option]]

        # @paul can you check whether here the correct value is deducted?
        # As in: if the duration is longer than 1:20 it should deduct small and help from trainer
        # is -1 + no DS/CB/SR etc
        option = st.checkbox(mistake[0])
        if option:
            option = mistake[1]
        else:
            option = 'none'
        st.session_state['general_mistakes'] += [[mistake[0], option]]

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


def compute_skill_requirements(all_CB):
    elems = st.session_state['selected_elements']
    srs = [None] * 4

    srs[0] = False
    for combo in all_CB:
        elem1 = get_element_by_name(combo[0])
        elem2 = get_element_by_name(combo[1])
        if elem1['element_type'] == ('dance' or 'jump') and elem2['element_type'] == ('dance' or 'jump'):
            # The combo consists of
            if elem1['element_type'] == 'jump'

    for elem in elems:
        # go through all elements
        if elem[1]['info_combo'] != 'none' and elem[1]['element_type'] == ('dance' or 'jump') and elem[1]['valid'] == 1:
            # if element is a turn or a jump check if a combination is done
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
                    e for e in elems if e[0] == elem[1]['info_combo'] and e[1]['valid'] == 1][0]
                if comboed_elem[1]['element_type'] == ('dance' or 'jump'):
                    # 2nd element follows dance requirement
                    flag1 = 0
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
                                if q[0] == 'What was the deviation from a 180º splits?' and q[1] == '0º':
                                    srs[0] = True
                                    break
                        if comboed_elem[1]['element_type'] == ('Split jump' or 'Split leap'):
                            for q in elem[1]['info_element_questions']:
                                if q[0] == 'What was the deviation from a 180º splits?' and q[1] == '0º':
                                    srs[0] = True
                                    break

    srs[1] = len([e for e in elems if 'Turn' in e[0]]) > 0
    srs[2] = len([e for e in elems if e[1]['element_type'] ==
                  'acro' and e[1]['difficulty'] in ['A', 'B']]) > 0

    relevant_elems = [e for e in elems if e[0] in ['Handstand',
                                                   'Cartwheel', 'Roundoff', 'Handstand to forward roll']]
    for e in relevant_elems:
        if e[0] == 'Handstand':
            for q in e[1]["info_element_questions"]:
                if q[0] == "Did the handstand reach vertical (90º)?":
                    if q[1] != "Yes":
                        relevant_elems.remove(e)

    srs[3] = len([e for e in relevant_elems]) > 0

    return round(sum(srs) * 0.5, 2), srs


def compute_combo_bonus():
    cb = 0
    counting_cbs = []
    all_cbs = []

    for elem in st.session_state['selected_elements']:
        if elem[1]['info_combo'] != 'none' and elem[1]['valid'] == 1:
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
                    e for e in st.session_state['selected_elements'] if e[0] == elem[1]['info_combo'] and e[1]['valid'] == 1][0]

                # Check whether this combo was not already calculated or is a combination with itself
                for comb in all_cbs:
                    if (comb[0] == comboed_elem[0] and comb[1] == elem[0]) or (comboed_elem[0] == elem[0]):
                        flag = 1

                if flag == 0:
                    for l in comboed_elem[1]['info_landing_mistakes']:
                        # check whether the second element of the combination has a
                        # fall (the combo doesn't count then)
                        if l[1] == 'very big':
                            # there was a fall so combo doesnt count
                            flag = 1

                    if flag == 0:
                        # 2nd element counts towards combo now check element difficulty to find bonus
                        all_cbs += [[elem[0], comboed_elem[0]]]

                        sorted_combo_elems = sorted(
                            [elem[1]['difficulty'], comboed_elem[1]['difficulty']])
                        if sorted_combo_elems == ['A', 'B']:
                            cb += 0.2
                            counting_cbs += [[[elem[0],
                                               comboed_elem[0]], ['A', 'B']]]
                        elif sorted_combo_elems == ['A', 'A']:
                            cb += 0.1
                            counting_cbs += [[[elem[0],
                                               comboed_elem[0]], ['A', 'A']]]

    return round(cb, 2), counting_cbs, all_cbs


def compute_difficulty_score():
    elems = [[e[0], e[1]['difficulty']]
             for e in st.session_state['selected_elements'] if e[1]['valid'] == 1]

    counted_elems = []
    difficulty = 0
    counter = [0, 0, 0]  # idx0=TA, idx1=A, idx2=B
    total_cnt = 0

    for elem in elems:
        if total_cnt != 7:
            if elem[1] == 'B':
                difficulty += 0.2
                counter[2] += 1
                total_cnt += 1
                counted_elems.append(elem)
    for elem in elems:
        if total_cnt != 7:
            if elem[1] == 'A':
                difficulty += 0.1
                counter[1] += 1
                total_cnt += 1
                counted_elems.append(elem)
    for elem in elems:
        if total_cnt != 7:
            if elem[1] == 'TA':
                difficulty += 0.1
                counter[0] += 1
                total_cnt += 1
                counted_elems.append(elem)

    return round(difficulty, 2), counted_elems, counter


def compute_artistry():
    artistry = 0
    mistakes = st.session_state['artistry_mistakes']

    for mistake in mistakes:
        if mistake[1] == True:
            artistry -= 0.1

    return round(artistry, 2), [e[0] for e in mistakes if e[1] == True]


def compute_execution():
    general_mistakes = st.session_state['general_mistakes']
    element_mistakes = []
    execution = 0

    for mistake in general_mistakes:
        if mistake[1] == 'small':
            execution -= 0.1
        elif mistake[1] == 'middle':
            execution -= 0.3
        elif mistake[1] == 'zero':
            execution = 10  # positive number should not be accessible normally, this routine is not valid

    if execution <= 0:
        for elem in st.session_state['selected_elements']:
            for answer in elem[1]['info_element_questions']:
                if answer[0] == "What was the deviation from a 180º splits?":
                    if answer[1] == "0-90°" or "<20°":
                        execution -= 0.1
                    elif answer[1] == ">90º(under horizontal)" or "20º - 45º":
                        execution -= 0.3
                if answer[0] == "Were both legs above horizontal?":
                    if answer[1] == "No, one/both legs were under horizontal":
                        execution -= 0.3
                    elif answer[1] == "No, one/both legs were on horizontal":
                        execution -= 0.1

            for mistake in elem[1]['info_execution_mistakes']:
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

            landing_ex = 0
            fall = 0
            for mistake in elem[1]['info_landing_mistakes']:
                if mistake[1] != 'none':
                    element_mistakes += [[elem[0], mistake[0], mistake[1]]]

                if mistake[1] == 'small':
                    landing_ex += 0.1
                elif mistake[1] == 'middle':
                    landing_ex += 0.3
                elif mistake[1] == 'big':
                    landing_ex += 0.5
                elif mistake[1] == 'very big':
                    landing_ex = 1.0
                    fall = 1
            # capped deduction at 0.8 if there was no fall
            if fall == 0 and landing_ex > 0.8:
                execution -= 0.8
            else:
                execution -= landing_ex

    return round(execution, 2), [e[0] for e in general_mistakes if e[1] != 'none'], element_mistakes


def compute_n_score():
    elem_count = len(st.session_state['selected_elements'])
    if elem_count in [4, 5]:
        return 4
    elif elem_count in [2, 3]:
        return 6
    elif elem_count == 1:
        return 8
    elif elem_count == 0:
        return 10
    else:
        return 0


def get_element_by_name(name):
    return [e for e in st.session_state['selected_elements'] if e[0] == name]


def results():
    cols = st.columns(20)
    with cols[0]:
        st.header('Results')

        st.subheader('D-Score')
        diff, d_elems, counter = compute_difficulty_score()
        CB_score, counting_CB, all_CB = compute_combo_bonus()
        SR_score, SR = compute_skill_requirements(all_CB)

        d_score = round(diff+SR_score+CB_score, 2)

        st.text("Difficulty ({}".format(counter[0]) + "TA + {}".format(counter[1]) + "A + {}".format(counter[2]) + "B)                                                                                +{}P. \n".format(diff) +
                "Composition Requirements                                                                                  +{}P. \n".format(SR_score) +
                "Connection Value                                                                                          +{}P. \n".format(CB_score))
        st.markdown('---')
        st.text("D-score                                                                                                   ={}P.".format(d_score))

        with st.expander('Difficulty Details'):
            # [[elem name 1, A], [elem name 2, TA]]
            for e in sorted(d_elems, key=lambda x: {'TA': 0, 'A': 1, 'B': 2}[x[1]]):
                st.markdown('- ' + e[0] + ' **' + e[1] + '**')

        with st.expander('Requirements Details'):
            for e_idx, e in enumerate(SR):
                st.markdown('- Requirement ' + str(e_idx + 1) +
                            ': **' + str(e) + '**')

        with st.expander('Connection Details'):
            for e_idx, e in enumerate(counting_CB):
                st.markdown(str(e_idx + 1) + '.' +
                            ': **' + e[0] + ' + ' + e[1] + '**')

        st.subheader(
            'E-Score')
        art_score, art_mistakes = compute_artistry()
        ex_score, gen_mistakes, ex_mistakes = compute_execution()
        n_score = compute_n_score()
        e_score = round(10.00+ex_score+art_score, 2)

        st.text("E-score                                                                                                   10.0P.\n" +
                "Execution                                                           {}P.".format(ex_score) + "                    \n" +
                "Artistry                                                            {}P.".format(art_score) + "                                {}P.\n".format(ex_score+art_score))
        st.markdown('---')
        st.text("E-score                                                                                                   ={}P.".format(e_score))

        with st.expander('Execution Details'):
            st.markdown('#### General mistakes')
            for e_idx, e in enumerate(gen_mistakes):
                st.markdown(str(e_idx + 1) + '. ' + e)

            st.markdown('#### Execution mistakes')
            for e_idx, e in enumerate(ex_mistakes):
                st.markdown(str(e_idx + 1) + '. ' + e)

        with st.expander('Artistry Details'):
            for e_idx, e in enumerate(art_mistakes):
                st.markdown(str(e_idx + 1) + '. ' + e)

        st.metric(label="Final score", value=e_score+d_score)
        if n_score != 0:
            st.text("Final score after neutral deduction for short exercise applied \n" +
                    "{}P.".format(e_score+d_score) + " - {}P.(short exercise)".format(n_score) + " = {}P.".format(round(e_score + d_score - n_score, 2)))
