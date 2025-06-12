import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QHBoxLayout
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

HIGH_SCORES_FILE = "high_scores.json"


class HighScoresWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tetris - High Scores")
        self.setFixedSize(500, 620)
        self.setup_ui()
        self.load_scores()

    def setup_ui(self):
        self.setStyleSheet("background-color: #1a1f28;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        title = QLabel("HIGH SCORES")
        title.setStyleSheet("""
            font-size: 28px;
            color: #e81212;
            font-family: 'Press Start 2P';
            text-align: center;
            text-shadow: 2px 2px 0 #2c2c7f;
        """)
        layout.addWidget(title)

        # Scores table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Rank", "Player", "Score", "Diff"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2c2c7f;
                color: white;
                border: 3px solid #3b55a2;
                font-family: 'Press Start 2P';
                font-size: 12px;
                gridline-color: #3b55a2;
            }
            QHeaderView::section {
                background-color: #0d40d8;
                color: white;
                padding: 5px;
                font-family: 'Press Start 2P';
                font-size: 14px;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()

        close_btn = QPushButton("BACK")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e81212;
                color: white;
                font-family: 'Press Start 2P';
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #2c2c7f;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #e27411;
            }
        """)
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        reset_btn = QPushButton("RESET SCORES")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #a600f7;
                color: white;
                font-family: 'Press Start 2P';
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #2c2c7f;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #e81212;
            }
        """)
        reset_btn.clicked.connect(self.reset_scores)
        btn_layout.addWidget(reset_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_scores(self):
        try:
            if not os.path.exists(HIGH_SCORES_FILE):
                self.scores = []
                return

            with open(HIGH_SCORES_FILE, 'r') as f:
                self.scores = json.load(f)
                self.scores.sort(key=lambda x: x['score'], reverse=True)
                self.display_scores()
        except Exception as e:
            self.scores = []
            print(f"Error loading scores: {e}")

    def display_scores(self):
        self.table.setRowCount(min(10, len(self.scores)))
        for i, entry in enumerate(self.scores[:10]):
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 1, QTableWidgetItem(entry['player']))
            self.table.setItem(i, 2, QTableWidgetItem(str(entry['score'])))
            self.table.setItem(i, 3, QTableWidgetItem(entry.get('difficulty', 'N/A')))

            # Color top 3 scores
            if i < 3:
                for col in range(4):
                    item = self.table.item(i, col)
                    item.setForeground(QColor("#edea04" if i == 0 else "#15ccd1" if i == 1 else "#e81212"))

    def reset_scores(self):
        self.scores = []
        try:
            with open(HIGH_SCORES_FILE, 'w') as f:
                json.dump([], f)
            self.display_scores()
        except Exception as e:
            print(f"Error resetting scores: {e}")