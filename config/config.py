from snowflake.snowpark.context import get_active_session
session = get_active_session()
DB_SCHEMA = "SFDC_CLEANER_DEV.RAW_DATA"