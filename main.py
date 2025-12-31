from config import config
import streamlit as st
from layout import main_screen, header

session, DB_SCHEMA = config.session, config.DB_SCHEMA

header()
main_screen(session, DB_SCHEMA)