import os
import json
import pygame
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSlider, QComboBox,
    QPushButton, QMessageBox, QFrame, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

pygame.mixer.init()

CONFIG_PATH = "settings.json"
DEFAULT_CONFIG = {
    "volume": 0.5,
    "music_file": "Sounds/music.ogg",
    "controls": {
        "left": "left",
        "right": "right",
        "rotate": "up",
        "drop": "space",
        "pause": "p"
    }
}

def load_config():
    """Load configuration from file or return defaults"""
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            # Merge with defaults to ensure all keys exist
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetris - Settings")
        self.setFixedSize(500, 620)
        self.config = load_config()
        self.setup_ui()
        self.play_music(self.config["music_file"])

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        self.setStyleSheet("background-color: #1a1f28;")
        self.setLayout(main_layout)

        # Title
        title = QLabel("GAME SETTINGS")
        title.setStyleSheet("""
            font-size: 28px;
            color: #15ccd1;
            font-family: 'Press Start 2P';
            text-align: center;
            text-shadow: 2px 2px 0 #2c2c7f;
            margin-bottom: 20px;
        """)
        main_layout.addWidget(title)

        # Settings panel
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: rgba(44, 44, 127, 200);
                border: 3px solid #3b55a2;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(25)

        # Volume control
        vol_label = QLabel("VOLUME LEVEL:")
        vol_label.setStyleSheet("""
            font-size: 14px;
            color: #ffffff;
            font-family: 'Press Start 2P';
        """)
        panel_layout.addWidget(vol_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self.config["volume"] * 100))
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 10px;
                background: #1a1f28;
                border: 2px solid #0d40d8;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #15ccd1;
                border: 2px solid #0d40d8;
                width: 20px;
                height: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: #3b55a2;
            }
        """)
        self.volume_slider.valueChanged.connect(self.adjust_volume)
        panel_layout.addWidget(self.volume_slider)

        # Music selection
        music_label = QLabel("GAME MUSIC:")
        music_label.setStyleSheet(vol_label.styleSheet())
        panel_layout.addWidget(music_label)

        self.music_selector = QComboBox()
        self.music_selector.addItems([
            "Sounds/music.ogg",
            "Sounds/Flaming Maple.mp3",
            "Sounds/retro-gaming-271301.mp3"
        ])
        self.music_selector.setCurrentText(self.config["music_file"])
        self.music_selector.setStyleSheet("""
            QComboBox {
                background-color: #1a1f28;
                color: white;
                border: 2px solid #0d40d8;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Press Start 2P';
                font-size: 12px;
                min-height: 30px;
            }
            QComboBox::drop-down {
                width: 25px;
                border-left: 2px solid #0d40d8;
            }
            QComboBox QAbstractItemView {
                background-color: #2c2c7f;
                color: white;
                selection-background-color: #3b55a2;
                font-family: 'Press Start 2P';
            }
        """)
        self.music_selector.currentIndexChanged.connect(self.preview_music)
        panel_layout.addWidget(self.music_selector)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        reset_btn = QPushButton("RESET")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #a600f7;
                color: white;
                font-family: 'Press Start 2P';
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #2c2c7f;
            }
            QPushButton:hover {
                background-color: #e81212;
            }
        """)
        reset_btn.clicked.connect(self.reset_defaults)
        btn_layout.addWidget(reset_btn)

        save_btn = QPushButton("SAVE")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2fe617;
                color: #1a1f28;
                font-family: 'Press Start 2P';
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #2c2c7f;
            }
            QPushButton:hover {
                background-color: #edea04;
            }
        """)
        save_btn.clicked.connect(self.apply_changes)
        btn_layout.addWidget(save_btn)

        panel_layout.addLayout(btn_layout)
        main_layout.addWidget(panel)

    def play_music(self, path):
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.config["volume"])
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            QMessageBox.critical(self, "Error", f"Could not play {path}:\n{e}")

    def adjust_volume(self, value):
        volume = value / 100
        self.config["volume"] = volume
        pygame.mixer.music.set_volume(volume)

    def preview_music(self):
        selected_file = self.music_selector.currentText()
        self.play_music(selected_file)

    def apply_changes(self):
        self.config["music_file"] = self.music_selector.currentText()
        save_config(self.config)
        self.play_music(self.config["music_file"])
        self.close()

    def reset_defaults(self):
        self.config = DEFAULT_CONFIG.copy()
        save_config(self.config)
        self.volume_slider.setValue(int(self.config["volume"] * 100))
        self.music_selector.setCurrentText(self.config["music_file"])
        self.play_music(self.config["music_file"])