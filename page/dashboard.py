import streamlit as st
from snowflake.snowpark.functions import col, count

def dashboard():
    session = st.session_state.session
    DB_SCHEMA = st.session_state.db_schema
    
    st.title("🛡️ Data Quality Hub: All-in-One Editor")
    st.markdown("Cortex AIとルールベースで検知された、修正が必要な通知を管理します。")
    
    # --- データの取得 ---
    log_table = session.table(f"{DB_SCHEMA}.ANOMALY_LOGS")
    unresolved_filter = (col("IS_RESOLVED") == False)
    
    # KPI表示
    total_anomalies = log_table.filter(unresolved_filter).count()
    rulebase_anomalies = log_table.filter(unresolved_filter & (col("ISSUE_TYPE") == "Rule-based")).count()
    ai_anomalies = log_table.filter(unresolved_filter & (col("ISSUE_TYPE") == "AI-based")).count()
    m1, m2, m3 = st.columns(3)      
    m1.metric("未対応総数", f"{total_anomalies}件")
    m2.metric("ルールベース検知", f"{rulebase_anomalies}件")
    m3.metric("AI検知", f"{ai_anomalies}件")
    
    st.divider()

    # タブ生成ロジック
    object_counts = log_table.filter(unresolved_filter) \
        .group_by(col("TABLE_NAME")).agg(count("*").as_("COUNT")) \
        .to_pandas().set_index("TABLE_NAME")["COUNT"].to_dict()

    tables = ["LEADS", "OPPORTUNITIES", "ACCOUNTS", "PRODUCTS2"]
    tab_names = [f"{t} (⬆️ {object_counts.get(t, 0)}件)" for t in tables]
    
    # 履歴タブの追加
    tables.append("✅ 修正済み")
    tab_names.append("✅ 解決済み（履歴）")

    tabs = st.tabs(tab_names)
    
    for i, tab_content in enumerate(tabs):
        with tab_content:
            t_name = tables[i]
            
            if t_name == "✅ 修正済み":
                df_resolved = log_table.filter(col("IS_RESOLVED") == True).to_pandas()
                st.dataframe(df_resolved, use_container_width=True, hide_index=True)
            else:
                # 異常データのフィルタリング
                filter_cond = (col("IS_RESOLVED") == False) & (col("TABLE_NAME") == t_name)
                df_anomalies = log_table.filter(filter_cond).order_by(col("DETECTED_AT").desc()).to_pandas()
                
                # --- インタラクティブ・データフレーム ---
                # 初期状態は未選択 (False)
                selected_event = st.dataframe(
                    df_anomalies, 
                    use_container_width=True, 
                    hide_index=True, 
                    on_select="rerun", # 選択時に再実行
                    selection_mode="single-row", # 単一行選択
                    key=f"df_{t_name}"
                )

                # --- 選択された場合のみ修正画面を表示 ---
                if selected_event and len(selected_event["selection"]["rows"]) > 0:
                    # 選択された行のインデックスを取得
                    row_idx = selected_event["selection"]["rows"][0]
                    anomaly = df_anomalies.iloc[row_idx]
                    
                    st.divider()
                    st.subheader(f"🛠️ 修正画面: {t_name}")
                    
                    # 実際のテーブルからレコードを取得
                    target_table_path = f"{DB_SCHEMA}.{t_name}"
                    source_record = session.table(target_table_path).filter(col("ID") == anomaly['RECORD_ID']).to_pandas()
                    
                    if not source_record.empty:
                        record = source_record.iloc[0]
                        
                        # 修正用フォーム
                        with st.form(key=f"edit_form_{t_name}_{anomaly['RECORD_ID']}"):
                            st.write(f"**対象ID**: `{anomaly['RECORD_ID']}`")
                            st.info(f"**AI指摘**: {anomaly['AI_FEEDBACK']}")
                            
                            # 編集フィールド（例: LEADS）
                            updated_data = {}
                            cols = st.columns(2)
                            
                            # テーブルごとのカラム設定（動的に調整可能）
                            fields_to_edit = [c for c in source_record.columns if c not in ["ID", "CREATED_AT"]]
                            
                            for j, field in enumerate(fields_to_edit):
                                with cols[j % 2]:
                                    updated_data[field] = st.text_input(field, value=str(record[field]))
                            
                            if st.form_submit_button("✅ 変更を保存して解決済みにする", type="primary"):
                                try:
                                    # 1. 元テーブルを更新
                                    session.table(target_table_path).update(updated_data, col("ID") == anomaly['RECORD_ID'])
                                    # 2. ログを解決済みに
                                    session.table(f"{DB_SCHEMA}.ANOMALY_LOGS").update(
                                        {"IS_RESOLVED": True},
                                        (col("TABLE_NAME") == t_name) & (col("RECORD_ID") == anomaly['RECORD_ID'])
                                    )
                                    st.success("更新が完了しました！")
                                    st.rerun() # リストを更新するために再起動
                                except Exception as e:
                                    st.error(f"エラーが発生しました: {e}")
                    else:
                        st.error("レコードが見つかりません。")