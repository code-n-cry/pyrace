from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from register import RegWindow
import os
import subprocess
import sqlite3
import sys


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/Login.ui', self)
        self.setWindowIcon(QIcon('../login&register/data/logging.jpg'))
        self.db = sqlite3.connect('data/accounts.db')
        self.cur = self.db.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(login, email, password)""")
        self.db.commit()
        self.regButton.clicked.connect(self.register)
        self.logButton.clicked.connect(self.login)
        self.pasEdit.setEchoMode(QLineEdit.Password)
        self.regwindow = RegWindow()

    def register(self):
        self.regwindow.show()

    def login(self):
        login = self.loginEdit.text()
        password = self.pasEdit.text()
        if login and password:
            true_password = self.cur.execute("""SELECT password FROM users WHERE login=?""", (login,)).fetchone()
            if true_password:
                if true_password[0] == ' '.join(format(ord(x), 'b') for x in password)[::-1]:
                    self.hide()
                    path = '/'.join(os.getcwd().replace('\\', '/').split('/')[:-1])
                    directory = '/menu_and_game/menu.py'
                    way_to_menu_file = path + directory
                    subprocess.call(f'python {way_to_menu_file} {login}', shell=True)
                else:
                    self.error.setText('Неправильный пароль!')
            else:
                self.error.setText('Пользователя с таким логином нет!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = LoginWindow()
    m.show()
    sys.exit(app.exec())
