import streamlit as st
from components import *
from util import *


st.set_page_config(
        page_title='gymnastics expert system',
        layout='wide'
    )

init_session_state()
hero_section()
choose_elements()