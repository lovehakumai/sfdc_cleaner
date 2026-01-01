from page.dashboard import dashboard
from page.initialize import initialize
from page.customize import customize
from page.AI_chat import AI_chat
import streamlit as st

def routing():
    page = st.session_state.get("current_page", "📊 ダッシュボード")

    if page == "📊 ダッシュボード":
        dashboard()

    elif page == "⚙️ 設定":
        initialize( )

    elif page == "🛡️ 検知のカスタム":
        customize()

    elif page == "🤖 AIと修正":
        AI_chat()