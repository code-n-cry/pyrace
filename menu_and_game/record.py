import os
import sqlite3


class Record:
    def __init__(self):
        self.path = '\\'.join(os.getcwd().split('\\')[:-1]) + '\\menu_and_game\\'
        self.connect = sqlite3.connect(self.path + '\\game_data\\users_info.db')
        self.connect.cursor().execute('''CREATE TABLE IF NOT EXISTS "record" (
                                        "id"	INTEGER,
                                        "score"	INTEGER,
                                        PRIMARY KEY("id" AUTOINCREMENT)
                                        );''')
        self.col = 1

    def read_records(self):
        cur = self.connect.cursor()
        score = cur.execute('''SELECT score FROM record ORDER BY score''').fetchall()
        return [i[0] for i in score]

    def add_record(self, score):
        if self.col == 1:
            self.col += 1
            cur = self.connect.cursor()
            cur.execute('''INSERT INTO record VALUES (?, ?)''', (None, score))
            self.connect.commit()

    def clear_records(self, record_id):
        cur = self.connect.cursor()
        cur.execute('''DELETE FROM record WHERE id=?''', (record_id, ))
        self.connect.commit()

    def get_id(self, score):
        print(score)
        cur = self.connect.cursor()
        need_id = cur.execute('SELECT id FROM record WHERE score=?', (score, )).fetchone()[0]
        return need_id
