import streamlit as st


def filter_dict(old_dict, callback):
    new_dict = dict()
    for (key, value) in old_dict.items():
        if callback((key, value)):
            new_dict[key] = value
    return new_dict


def init_session_state():
    st.session_state['small_mistakes'] = 0
    st.session_state['big_mistakes'] = 0
    st.session_state['falls'] = 0
    st.session_state['connections'] = 0

    if 'state' not in st.session_state.keys():
        st.session_state['state'] = 'choose_elements'
    if 'current_element' not in st.session_state.keys():
        st.session_state['current_element'] = 0


def hard_reset_session_state():
    st.session_state['small_mistakes'] = 0
    st.session_state['big_mistakes'] = 0
    st.session_state['falls'] = 0
    st.session_state['connections'] = 0

    st.session_state['state'] = 'choose_elements'
    st.session_state['current_element'] = 0
    st.session_state['selected_elements'] = []
    st.session_state['general_mistakes'] = []
    st.session_state['artistry_mistakes'] = []
    st.experimental_rerun()
