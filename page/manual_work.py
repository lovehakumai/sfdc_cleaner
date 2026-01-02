import streamlit as st
def manual_work():
    session = st.session_state.session
    DB_SCHEMA = st.session_state.db_schema
    
    st.title("✒️ マニュアル修正")
    
    # --- 検証実行セクション ---
    st.subheader("🔍 データ整合性チェックの実行")
    st.write("ボタンを押すと、定義されたルールに基づき全てのオブジェクトを検証します。")
    
    if st.button("🚀 今すぐ検証を開始する", type="primary"):
        with st.spinner("Cortex AIとルールエンジンを起動中..."):
            try:
                # ストアドプロシージャの呼び出し
                result = session.call(f"{DB_SCHEMA}.RUN_DATA_VALIDATION")
                st.success(f"完了: {result}")
                # ダッシュボードの数字を更新するためにリロードを促す
                if st.button("結果をダッシュボードで確認する"):
                    st.session_state.current_page = "📊 ダッシュボード"
                    st.rerun()
            except Exception as e:
                st.error(f"実行中にエラーが発生しました: {e}")
    
    st.divider()
    # --- 設定画面 ---
    st.subheader("⚙️ 既存のルール")
    create_manual_rule = st.button(" + マニュアルルールから作成")
    create_business_rule = st.button(" + ビジネスルールから作成")