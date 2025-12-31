from page import dashboard, initialize, customize, AI_chat

def routing(page, session, DB_SCHEMA):
    if page == "📊 ダッシュボード":
        dashboard(session, DB_SCHEMA)

    elif page == "⚙️ 初期設定":
        initialize(session, DB_SCHEMA)

    elif page == "🛡️ 検知のカスタム":
        customize(session, DB_SCHEMA)

    elif page == "🤖 AIエージェント":
        AI_chat(session, DB_SCHEMA)