from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                              QFrame, QHBoxLayout)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor, QFont
import os

class MainMenu(QWidget):
    start_game_signal = Signal(int, str, str)  # speed, difficulty_name, username

    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Tetris - {username}" if username else "Tetris")
        self.setWindowIcon(QIcon("ui/block_tetris.jpg"))
        self.setFixedSize(500, 620)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        self.setStyleSheet("background-color: #1a1f28;")
        self.setLayout(main_layout)

        # Header
        header = QLabel()
        header.setAlignment(Qt.AlignCenter)
        header_pixmap = QPixmap("ui/tetris_header.png")
        if not header_pixmap.isNull():
            header.setPixmap(header_pixmap.scaled(400, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            header.setText("TETRIS")
            header.setStyleSheet("""
                font-size: 48px;
                font-weight: bold;
                color: #e81212;
                font-family: 'Press Start 2P';
                text-shadow: 3px 3px 0 #2c2c7f;
            """)
        main_layout.addWidget(header)

        # Player info
        player_label = QLabel(f"PLAYER: {self.username.upper()}" if self.username else "PRESS START")
        player_label.setStyleSheet("""
            font-size: 18px;
            color: #15ccd1;
            font-family: 'Press Start 2P';
            text-align: center;
            margin: 10px 0;
        """)
        main_layout.addWidget(player_label)

        # Level selection (hidden by default)
        self.difficulty_frame = QFrame()
        self.difficulty_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(44, 44, 127, 200);
                border: 3px solid #3b55a2;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        level_layout = QVBoxLayout(self.difficulty_frame)

        level_label = QLabel("SELECT DIFFICULTY")
        level_label.setStyleSheet("""
            font-size: 16px;
            color: white;
            font-family: 'Press Start 2P';
            text-align: center;
            margin-bottom: 15px;
        """)
        level_layout.addWidget(level_label)

        # Level buttons
        levels = [
            ("EASY", "#2fe617", 800),
            ("MEDIUM", "#edea04", 400),
            ("HARD", "#e81212", 200)
        ]

        for text, color, speed in levels:
            btn = QPushButton(text)
            btn.setFixedHeight(50)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: #1a1f28;
                    border: 3px solid #2c2c7f;
                    border-radius: 5px;
                    font-family: 'Press Start 2P';
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    border: 3px solid {color};
                }}
            """)
            btn.clicked.connect(lambda _, s=speed: self.start_game_with_level(s, "Easy" if s == 800 else "Medium" if s == 400 else "Hard"))
            level_layout.addWidget(btn)

        # Back button
        back_btn = QPushButton("BACK TO MAIN MENU")
        back_btn.setFixedHeight(50)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b55a2;
                color: white;
                border: 3px solid #2c2c7f;
                border-radius: 5px;
                font-family: 'Press Start 2P';
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                border: 3px solid #15ccd1;
            }
        """)
        back_btn.clicked.connect(self.show_main_menu)
        level_layout.addWidget(back_btn)

        self.difficulty_frame.hide()
        main_layout.addWidget(self.difficulty_frame)

        # Main button container
        self.main_button_frame = QFrame()
        self.main_button_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(44, 44, 127, 200);
                border: 3px solid #3b55a2;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        button_layout = QVBoxLayout(self.main_button_frame)

        buttons = [
            ("START GAME", "#0d40d8", self.show_difficulty_menu),
            ("HIGH SCORES", "#a600f7", self.show_high_scores),
            ("SETTINGS", "#15ccd1", self.open_settings_window),
            ("QUIT", "#e81212", self.close)
        ]

        for text, color, callback in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(50)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: #1a1f28;
                    border: 3px solid #2c2c7f;
                    border-radius: 5px;
                    font-family: 'Press Start 2P';
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    border: 3px solid {color};
                }}
            """)
            btn.clicked.connect(callback)
            button_layout.addWidget(btn)

        main_layout.addWidget(self.main_button_frame)

        # Footer
        footer = QLabel("© 2025 TETRIS ")
        footer.setStyleSheet("""
            color: #3b55a2;
            font-family: 'Press Start 2P';
            font-size: 10px;
            text-align: center;
            margin-top: 20px;
        """)
        main_layout.addWidget(footer)

    def show_difficulty_menu(self):
        """Show difficulty selection and hide main menu"""
        self.main_button_frame.hide()
        self.difficulty_frame.show()

    def show_main_menu(self):
        """Show main menu and hide difficulty selection"""
        self.difficulty_frame.hide()
        self.main_button_frame.show()

    def start_game_with_level(self, speed, difficulty_name):
        """Start game with selected difficulty"""
        self.start_game_signal.emit(speed, difficulty_name, self.username)
        self.close()

    def show_high_scores(self):
        """Open high scores window"""
        from high_scores import HighScoresWindow
        self.high_scores = HighScoresWindow()
        self.high_scores.show()

    def open_settings_window(self):
        """Open settings window"""
        from settings import SettingsWindow
        self.settings_window = SettingsWindow()
        self.settings_window.show()