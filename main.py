from config.config import config
from layout.main_screen import main_screen
from layout.header import header

def main():
    header()
    config()
    main_screen()

if __name__ == "__main__":
    main()