import streamlit as st
from app import main_view, story_view

if 'page' not in st.session_state:
    st.session_state.page = 'main'

if st.session_state.page == 'main':
    main_view.show()
elif st.session_state.page == 'story':
    story_view.show()