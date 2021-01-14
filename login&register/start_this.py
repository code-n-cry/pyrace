from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from register import RegWindow
import os
import subprocess
import sqlite3
import sys
import datetime


class LoginWindow(QMainWindow):
    """Окно для входа пользователя"""

    def __init__(self):
        super().__init__()
        uic.loadUi('data/Login.ui', self)
        if 8 <= datetime.datetime.now().hour <= 21:
            self.pasEdit.setStyleSheet('''border: 1px solid gray; border-radius: 5px''')
            self.loginEdit.setStyleSheet('''border: 1px solid gray; border-radius: 5px''')
            self.logButton.setStyleSheet('''border: 1px solid gray; border-radius: 5px;''')
            self.regButton.setStyleSheet('''border: 1px solid gray; border-radius: 5px''')
            self.error.setStyleSheet('color: black')
        else:
            self.label_2.setStyleSheet('color: #a1a7ba')
            self.label.setStyleSheet('color: #a1a7ba')
            self.error.setStyleSheet('color: #a1a7ba')
            self.pasEdit.setStyleSheet('''background-color: #0d0505;
                         color: #a1a7ba;
                          border: 1px solid gray; border-radius: 5px''')
            self.loginEdit.setStyleSheet('''background-color: #0d0505;
                         color: #a1a7ba;
                          border: 1px solid gray; border-radius: 5px''')
            self.logButton.setStyleSheet('''color: #a1a7ba; background-color: #0d0505;
                        border: 1px solid gray; border-radius: 5px;''')
            self.regButton.setStyleSheet('''color: #a1a7ba; background-color: #0d0505;
                                    border: 1px solid gray; border-radius: 5px''')
            self.setStyleSheet("""QMainWindow {background-color: #0d0505}""")
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
            true_password = self.cur.execute("""SELECT password FROM users WHERE 
            login=?""", (login,)).fetchone()
            if true_password:
                if true_password[0] == ' '.join(format(ord(x), 'b') for x in password)[::-1]:
                    self.hide()
                    path = '/'.join(os.getcwd().replace('\\', '/').split('/')[:-1])
                    directory = '/menu_and_game/game_startup.py'
                    way_to_menu_file = path + directory
                    print(path + directory)
                    subprocess.call(f'python "{way_to_menu_file}" {login}', shell=True)
                    exit()
                else:
                    self.error.setText('Неправильный пароль!')
            else:
                self.error.setText('Пользователя с таким логином нет!')
        else:
            if not login and not password:
                self.error.setText('Введите логин и пароль!')
            elif not login:
                self.error.setText('Введите логин!')
            elif not password:
                self.error.setText('Введите пароль!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = LoginWindow()
    m.show()
    sys.exit(app.exec())
