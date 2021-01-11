import os
import sqlite3


class Record:
    """Класс для работы со временем поездки пользователя"""

    def __init__(self):
        self.path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\'
        self.connect = sqlite3.connect(self.path + '\\game_data\\users_info.db')
        self.connect.cursor().execute('''CREATE TABLE IF NOT EXISTS "record" (
                                        "id"	INTEGER,
                                        "score"	INTEGER,
                                        "player" TEXT,
                                        PRIMARY KEY("id" AUTOINCREMENT)
                                        );''')
        self.col = 1

    def read_records(self):
        cur = self.connect.cursor()
        score = cur.execute('''SELECT * FROM record''').fetchall()
        return score

    def add_record(self, score, user, music):
        if self.col == 1:
            music.play()
            self.col += 1
            cur = self.connect.cursor()
            cur.execute('''INSERT INTO record VALUES (?, ?, ?)''', (None, score, user))
            self.connect.commit()

    def clear_records(self, user):
        cur = self.connect.cursor()
        cur.execute('''DELETE FROM record WHERE player=?''', user)
        self.connect.commit()
