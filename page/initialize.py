import streamlit as st

def initialize():
    session = st.session_state.session
    DB_SCHEMA = st.session_state.db_schema
    
    st.title("⚙️ 設定")
    st.info("Salesforce接続情報や同期スケジュールの設定画面です。(機能は後で実装)")
    