from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import sqlite3
import datetime


class RegWindow(QWidget):
    """Окно регистрации"""

    def __init__(self, parent=None):
        super(RegWindow, self).__init__(parent, Qt.Window)
        uic.loadUi('data/Reg.ui', self)
        if 8 <= datetime.datetime.now().hour <= 21:
            self.pasEdit.setStyleSheet('''border: 1px solid gray; border-radius: 5px''')
            self.logEdit.setStyleSheet('''border: 1px solid gray; border-radius: 5px''')
            self.mailEdit.setStyleSheet('''border: 1px solid gray; border-radius: 5px''')
            self.pasEdit2.setStyleSheet('''border: 1px solid gray; border-radius: 5px''')
            self.regButton.setStyleSheet('''border: 1px solid gray; border-radius: 5px''')
        else:
            self.label.setStyleSheet('color: #a1a7ba')
            self.label_2.setStyleSheet('color: #a1a7ba')
            self.label_3.setStyleSheet('color: #a1a7ba')
            self.label_4.setStyleSheet('color: #a1a7ba')
            self.errors.setStyleSheet('color: #a1a7ba')
            self.logEdit.setStyleSheet('''background-color: #0d0505;
                                     color: #a1a7ba;
                                      border: 1px solid gray; border-radius: 5px''')
            self.mailEdit.setStyleSheet('''background-color: #0d0505;
                                     color: #a1a7ba;
                                      border: 1px solid gray; border-radius: 5px''')
            self.pasEdit.setStyleSheet('''background-color: #0d0505;
                                     color: #a1a7ba;
                                      border: 1px solid gray; border-radius: 5px''')
            self.pasEdit2.setStyleSheet('''background-color: #0d0505;
                                     color: #a1a7ba;
                                      border: 1px solid gray; border-radius: 5px''')
            self.regButton.setStyleSheet('''color: #a1a7ba; background-color: #0d0505;
                                                border: 1px solid gray; border-radius: 5px''')
            self.setStyleSheet("""QWidget {background-color: #0d0505}""")
        self.setWindowIcon(QIcon('../login&register/data/reg.png'))
        self.db = sqlite3.connect('data/accounts.db')
        self.cur = self.db.cursor()
        self.regButton.clicked.connect(self.reg)
        self.pasEdit.setEchoMode(QLineEdit.Password)
        self.pasEdit2.setEchoMode(QLineEdit.Password)

    def reg(self):
        """Проверка всех данных"""

        self.errors.clear()
        login = self.logEdit.text()
        email = self.mailEdit.text()
        password = self.pasEdit.text()
        repeat_password = self.pasEdit2.text()
        if login and email and password and repeat_password and repeat_password == password:
            if not self.check_login(login):
                self.errors.setText('В логине не должно быть русских букв!')
            if not self.check_email(email):
                if self.check_email(email) == 0:
                    self.errors.setText('Введите email корректно!')
                if self.check_email(email) == '':
                    self.errors.setText('Введите существующий email!')
                if self.check_email(email) == []:
                    self.errors.setText(
                        'Аккаунт, зарегистрированный на эту почту, уже существует!')
            if self.checking_password(password):
                self.errors.setText(str(self.checking_password(password)))
            else:
                logins = [i[0] for i in
                          self.cur.execute("""SELECT login FROM users""").fetchall()]
                if login not in logins:
                    pas = ' '.join(format(ord(x), 'b') for x in password)[::-1]
                    self.cur.execute("""INSERT INTO users  VALUES (?, ?, ?)""",
                                     (login, email, pas))
                    self.db.commit()
                    self.close()
                else:
                    self.errors.setText('Пользователь с таким логином уже существует!')
        elif not login:
            self.errors.setText('Введите логин!')
        elif not email:
            self.errors.setText('Введите e-mail!')
        elif not password or not repeat_password:
            self.errors.setText('Введите пароль в оба поля!')
        elif password != repeat_password:
            self.errors.setText('Пароли должны совпадать!')

    def check_login(self, login):
        """Логин не должен быть в базе данных(условие в функции check) и должен быть из
        некириллических символов """

        login = login.lower()
        cyrillic = 'йцукенгшщзхъёфывапролджэячсмитьбю'
        for i in cyrillic:
            if i in login:
                return False
        return True

    def check_email(self, email):
        """Проверка email производится по наличию символа '@' и  правильному сервису почты"""

        emails = self.cur.execute("""SELECT email FROM users""").fetchall()
        for i in emails:
            if email == i[0]:
                return []
        if '@' not in email:
            return 0
        if not email.endswith('gmail.com') and not \
                email.endswith('yandex.ru') and not email.endswith('icloud.com') and \
                email.endswith('outlook.com'):
            return ''
        return True

    def checking_password(self, password):
        """Проверка пароля производится по длине(>=8), наличию цифр и букв,
        отсутствию трёхзначных сочетаний с клавиатуры в пароле"""

        digits = '1234567890'
        fst_line = 'qwertyuiopйцукенгшщзхъ'
        sec_line = 'asdfghjklфывапролджэ'
        th_line = 'zxcvbnmячсмитьбю'
        fst_macline = 'asdfghjklфывапролджэё'
        pc_clava = fst_line + sec_line + th_line
        password = password.lower()
        if len(password) < 8:
            return 'Длина пароля должа быть больше 8 символов!'
        if not any([i in password for i in digits]) or not any(
                [j in password for j in pc_clava]):
            return 'В пароле должны быть и цифры, и буквы!'
        for i in range(2, len(password)):
            if password[i - 2] + password[i - 1] + password[i] in fst_line or \
                    password[i - 2] + password[i - 1] + password[i] in sec_line or \
                    password[i - 2] + password[i - 1] + password[i] in th_line or \
                    password[i - 2] + password[i - 1] + password[i] in fst_macline:
                return 'Не должно быть клавиатурных сочетаний из трёх букв!(Также на ' \
                       'клавиатуре mac) '
        return None
