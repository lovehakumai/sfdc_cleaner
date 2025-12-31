import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, count
from page.dashboard import dashboard

# ページ設定 (ワイドモードを適用)
st.set_page_config(layout="wide", page_title="SFDC Cleaner Dashboard")
session = get_active_session()

# --- 1. 定数の定義 (完全修飾名のためのパス) ---
DB_SCHEMA = "SFDC_CLEANER_DEV.RAW_DATA"

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

# --- 3. 【要件】サイドバーによるページ切り替え（画面だけ実装） ---
st.sidebar.title("🧭 ナビゲーション")
st.sidebar.markdown("フェーズごとの機能を選択してください。")
page = st.sidebar.radio(
    "ページを選択",
    ["📊 ダッシュボード", "⚙️ 初期設定", "🛡️ 検知のカスタム", "🤖 AIエージェント"]
)

# =========================================
# ページ1: ダッシュボード（現在のメイン画面）
# =========================================
dashboard();

# =========================================
# ページ2〜4: その他のページ（画面だけ実装）
# =========================================
elif page == "⚙️ 初期設定":
    st.title("⚙️ 初期設定")
    st.info("Salesforce接続情報や同期スケジュールの設定画面です。(機能は後で実装)")
    # ここに設定用フォームなどを配置予定

elif page == "🛡️ 検知のカスタム":
    st.title("🛡️ 検知のカスタム")
    st.info("異常検知のルールベース閾値や、AIへの指示(Prompt)をカスタマイズする画面です。(機能は後で実装)")
    # ここにスライダーやテキストエリアなどを配置予定

elif page == "🤖 AIエージェント":
    st.title("🤖 AIエージェント")
    st.info("自動修正を行うAIエージェントの設定、および修正履歴の確認画面です。(機能は後で実装)")
    # ここに実行ログなどを配置予定