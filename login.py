
from database import Database

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                              QPushButton, QMessageBox, QHBoxLayout)
from PySide6.QtGui import QIcon, QFont, QPixmap, QFontDatabase
from PySide6.QtCore import Qt, Signal

from database import Database

class LoginWindow(QWidget):
    login_successful = Signal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetris - Login")
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
            color: #2fe617;
            text-align: center;
            font-family: 'Press Start 2P';
            margin-bottom: 10px;
            text-shadow: 3px 3px 0 #2c2c7f;
        """)
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Subtitle
        subtitle = QLabel("LOGIN TO PLAY")
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
            border: 3px solid #3b55a2;
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

        layout.addWidget(input_container)

        # Login Button
        btn_login = QPushButton("LOGIN")
        btn_login.setStyleSheet("""
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
        btn_login.clicked.connect(self.handle_login)
        layout.addWidget(btn_login, alignment=Qt.AlignCenter)

        # Register link
        register_link = QLabel("<a href='signup' style='text-decoration: none; color: (237, 234, 4);'>Don't have an account? Register</a>")
        register_link.setStyleSheet("""
            font-size: 12px;
            font-family: 'Press Start 2P';
            margin-top: 10px;
            text-align: center;
        """)
        register_link.setOpenExternalLinks(False)
        register_link.linkActivated.connect(self.open_signup)
        layout.addWidget(register_link, alignment=Qt.AlignCenter)

        # Guest divider
        divider = QLabel("───── OR ─────")
        divider.setStyleSheet("""
            color:(255, 255, 255);
            font-family: 'Press Start 2P';
            font-size: 12px;
            text-align: center;
            margin: 15px 0;
        """)
        layout.addWidget(divider , alignment=Qt.AlignCenter )

        # Guest Button
        btn_guest = QPushButton("PLAY AS GUEST")
        btn_guest.setStyleSheet("""
            QPushButton {
                background-color: #2fe617;
                color: #0d40d8 ;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                font-family: 'Press Start 2P';
                border: 2px solid #2c2c7f;
                min-width: 150px;
            }
            QPushButton:hover {
                 background-color: #15ccd1;
                color: #1a1f28;
            }
            QPushButton:pressed {
                background-color: (21, 204, 209);
            }
        """)
        btn_guest.clicked.connect(self.play_as_guest)
        layout.addWidget(btn_guest, alignment=Qt.AlignCenter)

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
        font_id = QFontDatabase.addApplicationFont("Press_Start_2P/PressStart2P-Regular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            pixel_font = QFont(font_family, 8)
            self.setFont(pixel_font)

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        if self.db.check_user(username, password):
            self.login_successful.emit(username)
            self.authenticated_username = user['username']
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")

    def play_as_guest(self):
        self.login_successful.emit("Guest")  # ✅ signal envoyé
        self.close()

    def open_signup(self):
        from signup import SignupWindow
        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.close()
