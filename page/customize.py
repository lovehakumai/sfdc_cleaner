import streamlit as st

def customize():
    session = st.session_state.session
    DB_SCHEMA = st.session_state.db_schema
    
    import streamlit as st
    st.title("🛡️ 検知のカスタム")
    st.info("異常検知のルールベース閾値や、AIへの指示(Prompt)をカスタマイズする画面です。(機能は後で実装)")
    # ここにスライダーやテキストエリアなどを配置予定