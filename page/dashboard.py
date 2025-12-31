import streamlit as st
from snowflake.snowpark.functions import col, count

def dashboard():
    session = st.session_state.session
    DB_SCHEMA = st.session_state.db_schema
    
    st.title("🛡️ Data Quality Hub: All-in-One Editor")
    st.markdown("Cortex AIとルールベースで検知された、修正が必要なアクティブな通知を管理します。")
    
    # データの取得
    log_table = session.table(f"{DB_SCHEMA}.ANOMALY_LOGS")
    unresolved_filter = (col("IS_RESOLVED") == False)
    
    # KPIエリア (色のCSSが適用されます)
    total_anomalies = log_table.filter(unresolved_filter).count()
    rule_anomalies = log_table.filter(unresolved_filter & (col("ISSUE_TYPE") == "Rule-based")).count()
    ai_anomalies = log_table.filter(unresolved_filter & (col("ISSUE_TYPE") == "AI-based")).count()

    m1, m2, m3 = st.columns(3)
    m1.metric("未対応総数", f"{total_anomalies}件")
    m2.metric("ルール検知", f"{rule_anomalies}件")
    m3.metric("AI(Cortex)検知", f"{ai_anomalies}件")

    st.divider()

    # --- 4. 【要件】オブジェクトごとのタブ化とフィルタ機能付与 ---
    # オブジェクトごとの未対応件数をクエリで取得 (GROUP BY)
    object_counts = session.table(f"{DB_SCHEMA}.ANOMALY_LOGS") \
        .filter(col("IS_RESOLVED") == False) \
        .group_by(col("TABLE_NAME")).agg(count("*").as_("count")) \
        .to_pandas().set_index("TABLE_NAME")["COUNT"].to_dict()

    # タブ名に件数を動的に追加してリスト化
    tables = ["LEADS", "OPPORTUNITIES", "ACCOUNTS", "PRODUCTS2"]
    tab_names = []
    for t in tables:
        cnt = object_counts.get(t, 0)
        tab_names.append(f"{t} (⬆️ {cnt}件)") # 件数を表示

    # その他、修正済みデータをまとめるタブ名を追加
    tables.append("OTHER")
    tab_names.append("その他")
    
    # --- 【要件】修正済みのデータを表示するタブ ---
    tables.append("✅ 修正済み")
    tab_names.append("✅ 解決済み（履歴）") 

    # タブを描画
    st.subheader("📌 タスク一覧")
    tabs = st.tabs(tab_names)
    
    # 各タブの中身
    for i, tab_content in enumerate(tabs):
        with tab_content:
            t_name = tables[i]
            
            if t_name == "✅ 修正済み":
                # 修正済みデータの表示 (フィルタ付きデータフレーム)
                df_resolved = log_table.filter(col("IS_RESOLVED") == True).to_pandas()
                st.dataframe(df_resolved, use_container_width=True, hide_index=True) # デフォルトでフィルタ機能あり
                
            else:
                # 未対応データの表示（テーブルごとにフィルタ）
                if t_name == "OTHER":
                    filter_cond = (col("IS_RESOLVED") == False) & (~col("TABLE_NAME").in_(*tables[:-2])) # それ以外
                else:
                    filter_cond = (col("IS_RESOLVED") == False) & (col("TABLE_NAME") == t_name)
                
                # 該当データを取得
                df_anomalies = log_table.filter(filter_cond).order_by(col("DETECTED_AT").desc()).to_pandas()
                
                # データフレーム選択（ここからは既存の修正フォームのロジックを流用）
                selected_event = st.dataframe(
                    df_anomalies, 
                    use_container_width=True, 
                    hide_index=True, 
                    on_select="rerun", 
                    selection_mode="single-row"
                )

                if selected_event and len(selected_event["selection"]["rows"]) > 0:
                    # ... (以前のコードの修正エディタ表示とUPDATEのロジック) ...
                    pass