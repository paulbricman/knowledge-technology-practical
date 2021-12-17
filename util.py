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