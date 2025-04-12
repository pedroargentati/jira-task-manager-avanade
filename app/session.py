import streamlit as st

def get(key, default=None):
    return st.session_state.get(key, default)

def set(key, value):
    st.session_state[key] = value

def exists(key):
    return key in st.session_state

def remove(key):
    if key in st.session_state:
        del st.session_state[key]

def set_many(data: dict):
    for key, value in data.items():
        st.session_state[key] = value

def get_all(keys: list):
    return {key: st.session_state.get(key) for key in keys}

def clear_all():
    st.session_state.clear()

def page_to(name: str):
    st.session_state.page = name
    st.rerun()
