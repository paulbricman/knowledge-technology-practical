import streamlit as st

def hero_section():
    st.markdown('# 🤖 Expert System')
    st.markdown('This tool has been developed by Elena, Jesse, and Paul in the context of Knowledge Technology Practical.')
    st.warning('While this system automates important parts the tedious thought process an expert typically goes through, it\'s important to consult the actual expert when uncertain.')
    st.markdown('---')

    name = st.text_input('What\'s your name?', help='Please enter your first name for making the interaction more natural.')
    
    if st.button('Next'):
        st.info('Hi there, ' + name + '! Welcome to our expert system.')