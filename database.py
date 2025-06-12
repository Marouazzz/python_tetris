import pymysql
import hashlib
from PySide6.QtWidgets import QMessageBox

class Database:
    def __init__(self):

        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="tetris_python",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            ''')
            self.conn.commit()

    def hash_password(self, password):

        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def add_user(self, username, password):  # Remove password2 parameter
        hashed_password = self.hash_password(password)

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO users (username, password) VALUES (%s, %s)',
                    (username, hashed_password)
                )
            self.conn.commit()
            return True
        except pymysql.err.IntegrityError:
            QMessageBox.warning(None, "Error", "Username already exists.")
            return False

    def check_user(self, username, password):
        hashed_password = self.hash_password(password)

        with self.conn.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM users WHERE username=%s AND password=%s',
                (username, hashed_password)
            )
            result = cursor.fetchone()
        return result
