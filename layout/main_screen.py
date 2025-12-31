from component import sidebar, routing

def main_screen(session, DB_SCHEMA):
    sidebar()
    routing(session, DB_SCHEMA)