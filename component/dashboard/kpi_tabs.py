import streamlit as st
from snowflake.snowpark.functions import col

def kpi_tabs():
    session = st.session_state.session
    DB_SCHEMA = st.session_state.db_schema

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