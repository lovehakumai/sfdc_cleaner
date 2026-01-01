import streamlit as st

def sidebar():
    # session_state を更新する。keyを指定すると自動で保持される
    st.sidebar.radio(
        "ページを選択",
        ["📊 ダッシュボード","🤖 AIと修正", "🛡️ 検知のカスタム",  "⚙️ 設定"],
        key="current_page" # これで st.session_state.current_page に保存される
    )