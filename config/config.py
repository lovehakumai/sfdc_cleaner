from snowflake.snowpark.context import get_active_session

def config():
    session = get_active_session()
    DB_SCHEMA = "SFDC_CLEANER_DEV.RAW_DATA"
    return session, DB_SCHEMA