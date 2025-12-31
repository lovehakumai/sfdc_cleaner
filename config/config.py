from snowflake.snowpark.context import get_active_session
import streamlit as st

def config():
    st.session_state.session = get_active_session()
    st.session_state.db_schema = "SFDC_CLEANER_DEV.RAW_DATA"