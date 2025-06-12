import sys
from PySide6.QtWidgets import QApplication
from login import LoginWindow
from main_menu import MainMenu
from game_controller import GameController

def run_app():
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    def on_login_success(username):
        main_menu = MainMenu(username)

        def on_start_game(speed, difficulty_name, username):
            controller = GameController(speed=speed, difficulty_name=difficulty_name, username=username)
            controller.start_game()

        main_menu.start_game_signal.connect(on_start_game)
        main_menu.show()


    login_window.login_successful.connect(on_login_success)

    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
