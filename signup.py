from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                              QPushButton, QMessageBox)
from PySide6.QtGui import QIcon, QFont, QFontDatabase
from PySide6.QtCore import Qt

from database import Database
class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetris - Register")
        self.setFixedSize(500, 620)  # Matches game screen size
        self.setWindowIcon(QIcon("ui/block_tetris.jpg"))
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        self.setStyleSheet("""
            background-color: #1a1f28;
        """)

        # Tetris title
        title = QLabel("TETRIS")
        title.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #15ccd1;
            text-align: center;
            font-family: 'Press Start 2P';
            margin-bottom: 10px;
            text-shadow: 3px 3px 0 #2c2c7f;
        """)
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Subtitle
        subtitle = QLabel("CREATE ACCOUNT")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: (255, 255, 255);
            text-align: center;
            margin-bottom: 30px;
            font-family: 'Press Start 2P';
        """)
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        # Input fields container
        input_container = QWidget()
        input_container.setStyleSheet("""
            background-color: #2c2c7f;
            border: 3px solid #15ccd1;
            border-radius: 8px;
            padding: 20px;
        """)
        input_layout = QVBoxLayout(input_container)
        input_layout.setSpacing(15)

        # Username
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("""
            QLineEdit {
                background-color: #1a1f28;
                color: #ffffff;
                border: 2px solid #0d40d8;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Press Start 2P';
            }
            QLineEdit:focus {
                border: 2px solid #15ccd1;
            }
        """)
        input_layout.addWidget(self.username)

        # Password
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: #1a1f28;
                color: #ffffff;
                border: 2px solid #0d40d8;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Press Start 2P';
            }
            QLineEdit:focus {
                border: 2px solid #15ccd1;
            }
        """)
        input_layout.addWidget(self.password)

        # Confirm Password
        self.password2 = QLineEdit()
        self.password2.setPlaceholderText("Confirm Password")
        self.password2.setEchoMode(QLineEdit.Password)
        self.password2.setStyleSheet("""
            QLineEdit {
                background-color: #1a1f28;
                color: #ffffff;
                border: 2px solid #0d40d8;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-family: 'Press Start 2P';
            }
            QLineEdit:focus {
                border: 2px solid #15ccd1;
            }
        """)
        input_layout.addWidget(self.password2)

        layout.addWidget(input_container)

        # Register Button
        btn_register = QPushButton("REGISTER")
        btn_register.setStyleSheet("""
            QPushButton {
                background-color: #0d40d8;
                color: #ffffff;
                font-size: 16px;
                padding: 12px;
                border-radius: 5px;
                font-weight: bold;
                font-family: 'Press Start 2P';
                border: 2px solid #2c2c7f;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #15ccd1;
                color: #1a1f28;
            }
            QPushButton:pressed {
                background-color: #3b55a2;
            }
        """)
        btn_register.clicked.connect(self.handle_signup)
        layout.addWidget(btn_register, alignment=Qt.AlignCenter)

        # Back to Login link
        login_link = QLabel("<a href='login' style='text-decoration: none; color: (237, 234, 4);'>Already have an account? Login</a>")
        login_link.setStyleSheet("""
            font-size: 12px;
            font-family: 'Press Start 2P';
            margin-top: 20px;
            text-align: center;
        """)
        login_link.setOpenExternalLinks(False)
        login_link.linkActivated.connect(self.back_to_login)
        layout.addWidget(login_link, alignment=Qt.AlignCenter)

        # Footer
        footer = QLabel("© 2025 TETRIS")
        footer.setStyleSheet("""
            color: #3b55a2;
            font-family: 'Press Start 2P';
            font-size: 10px;
            text-align: center;
            margin-top: 30px;
        """)
        layout.addWidget(footer)

        self.setLayout(layout)

        # Load pixel font
        self.load_pixel_font()

    def load_pixel_font(self):
        font_id = QFontDatabase.addApplicationFont("ui/press-start-2p.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            pixel_font = QFont(font_family, 8)
            self.setFont(pixel_font)

    # Keep all existing methods unchanged
    def handle_signup(self):
        username = self.username.text()
        password = self.password.text()
        password2 = self.password2.text()

        if not username or not password or not password2:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        if password != password2:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        # Password complexity checks
        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters long.")
            return

        if not any(char.isdigit() for char in password):
            QMessageBox.warning(self, "Error", "Password must contain at least one number.")
            return

        if not any(char.isupper() for char in password):
            QMessageBox.warning(self, "Error", "Password must contain at least one uppercase letter.")
            return

        if not any(char.islower() for char in password):
            QMessageBox.warning(self, "Error", "Password must contain at least one lowercase letter.")
            return

        # Special character check (optional)
        special_chars = "!@#$%^&*()-+?_=,<>/"
        if not any(char in special_chars for char in password):
            QMessageBox.warning(self, "Error", "Password must contain at least one special character.")
            return

        if self.db.add_user(username, password):
            self.open_main_menu(username)
        else:
            QMessageBox.warning(self, "Error", "Username already exists or other error")
    def back_to_login(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_main_menu(self, username):
        from main_menu import MainMenu
        self.main_menu = MainMenu(username)
        self.main_menu.show()
        self.close()