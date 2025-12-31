from page import dashboard, initialize, customize, AI_chat
import streamlit as st

def routing(session, DB_SCHEMA):

    page = st.session_state.get("current_page", "📊 ダッシュボード")

    if page == "📊 ダッシュボード":
        dashboard(session, DB_SCHEMA)

    elif page == "⚙️ 初期設定":
        initialize(session, DB_SCHEMA)

    elif page == "🛡️ 検知のカスタム":
        customize(session, DB_SCHEMA)

    elif page == "🤖 AIエージェント":
        AI_chat(session, DB_SCHEMA)