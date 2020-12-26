from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import sqlite3


class RegWindow(QWidget):
    def __init__(self, parent=None):
        super(RegWindow, self).__init__(parent, Qt.Window)
        uic.loadUi('data/Reg.ui', self)
        self.setWindowIcon(QIcon('../login&register/data/reg.png'))
        self.db = sqlite3.connect('data/accounts.db')
        self.cur = self.db.cursor()
        self.regButton.clicked.connect(self.reg)
        self.pasEdit.setEchoMode(QLineEdit.Password)
        self.pasEdit2.setEchoMode(QLineEdit.Password)
    def reg(self):
        self.errors.clear()
        login = self.logEdit.text()
        email = self.mailEdit.text()
        pas = self.pasEdit.text()
        repeat_pas = self.pasEdit2.text()
        if login and email and pas and repeat_pas and repeat_pas == pas:
            if not self.check_login(login):
                self.errors.setText('В логине не должно быть русских букв!')
            elif not self.check_email(email):
                if self.check_email(email) == 1:
                    self.errors.setText('Введите email корректно!')
                if self.check_email(email) == 2:
                    self.errors.setText('Введите существующий email!')
                if self.check_email(email) == 3:
                    self.errors.setText('Аккаунт, зарегистрированный на эту почту, уже существует!')
            elif not self.checking_password(pas):
                self.errors.setText(self.checking_password(pas))
            else:
                logins = [i[0] for i in self.cur.execute("""SELECT login FROM users""").fetchall()]
                if login not in logins:
                    pas = ' '.join(format(ord(x), 'b') for x in pas)[::-1]
                    self.cur.execute("""INSERT INTO users  VALUES (?, ?, ?)""", (login, email, pas))
                    self.db.commit()
                    self.hide()
                else:
                    self.errors.setText('Пользователь с таким логином уже существует!')
        elif not login:
            self.errors.setText('Введите логин!')
        elif not email:
            self.errors.setText('Введите e-mail!')
        elif not pas or not repeat_pas:
            self.errors.setText('Введите пароль в оба поля!')
        elif pas != repeat_pas:
            self.errors.setText('Пароли должны совпадать!')

    def check_login(self, login):
        login = login.lower()
        cyrillic = 'йцукенгшщзхъёфывапролджэячсмитьбю'
        for i in cyrillic:
            if i in login:
                return False
        return True

    def check_email(self, email):
        emails = self.cur.execute("""SELECT email FROM users""").fetchall()
        for i in emails:
            if email == i[0]:
                return 3
        if '@' not in email:
            return 1
        elif not email.endswith('gmail.com') or not \
                email.endswith('yandex.ru') or not email.endswith('icloud.com') or \
                email.endswith('outlook.com'):
            return 2
        return True

    def checking_password(self, password):
        digits = '1234567890'
        fst_line = 'qwertyuiopйцукенгшщзхъ'
        sec_line = 'asdfghjklфывапролджэ'
        th_line = 'zxcvbnmячсмитьбю'
        fst_macline = 'asdfghjklфывапролджэё'
        pc_clava = fst_line + sec_line + th_line
        try:
            password = password.lower()
            assert len(password) > 8
            assert any([i in password for i in digits])
            assert any([j in password for j in pc_clava])
            for i in range(2, len(password)):
                assert password[i - 2] + password[i - 1] + password[i] not in fst_line
                assert password[i - 2] + password[i - 1] + password[i] not in sec_line
                assert password[i - 2] + password[i - 1] + password[i] not in th_line
                assert password[i - 2] + password[i - 1] + password[i] not in fst_macline
                assert password[i - 2] + password[i - 1] + password[i] not in sec_line
                assert password[i - 2] + password[i - 1] + password[i] not in th_line
            return True
        except Exception as e:
            return e
