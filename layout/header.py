import streamlit as st
from snowflake.snowpark.context import get_active_session

def header():
    # ページ設定 (ワイドモードを適用)
    st.set_page_config(layout="wide", page_title="SFDC Cleaner Dashboard")
    st.sidebar.title("🧭 ナビゲーション")
    st.sidebar.markdown("フェーズごとの機能を選択してください。")
    # --- 2. 【要件】KPIの色を見やすく改善 (カスタムCSS) ---
    st.markdown("""
        <style>
        /* メトリクスコンテナ全体のデザイン */
        div[data-testid="metric-container"] {
            background-color: #E1F5FE;  /* 明るい青色の背景 */
            border: 1px solid #0277BD;  /* 濃い青のボーダー */
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        /* KPIのラベル（文字色と太さ） */
        div[data-testid="stMetricLabel"] > div {
            color: #0277BD; /* 視認性の良い青 */
            font-weight: bold;
            font-size: 1.1rem;
        }
        /* KPIの数値（文字色と太さ） */
        div[data-testid="stMetricValue"] > div {
            color: #01579B; /* さらに濃い青 */
            font-weight: bold;
            font-size: 2.5rem;
        }
        </style>
    """, unsafe_allow_html=True)