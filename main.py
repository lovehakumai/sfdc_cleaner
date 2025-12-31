from config import config
import streamlit as st
from layout import main_screen, header

def main():
# --- 1. 設定の取得 ---
    session, DB_SCHEMA = config()
# --- 画面表示 ---
    header()
    main_screen(session, DB_SCHEMA)

if __name__ == "__main__":
    main()