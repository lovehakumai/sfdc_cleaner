from page import dashboard, initialize, customize, AI_chat
import streamlit as st

def routing():
    page = st.session_state.get("current_page", "📊 ダッシュボード")

    if page == "📊 ダッシュボード":
        dashboard()

    elif page == "⚙️ 初期設定":
        initialize( )

    elif page == "🛡️ 検知のカスタム":
        customize()

    elif page == "🤖 AIエージェント":
        AI_chat()