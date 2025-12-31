from page import header, main_screen, config
import streamlit as st

current_page = st.session_state.current_page

session, DB_SCHEMA = config.session, config.DB_SCHEMA

header()
main_screen()