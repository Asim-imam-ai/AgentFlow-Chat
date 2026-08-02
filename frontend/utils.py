import streamlit as st


def show_error(message: str):
    st.error(f"⚠️ {message}")


def show_info(message: str):
    st.info(message)


def show_success(message: str):
    st.success(message)
