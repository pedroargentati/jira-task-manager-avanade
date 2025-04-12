import streamlit as st
from app import main_view, story_view

import os
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"


if 'page' not in st.session_state:
    st.session_state.page = 'main'

if st.session_state.page == 'main':
    main_view.show()
elif st.session_state.page == 'story':
    story_view.show()