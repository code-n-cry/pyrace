from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
import os
import sys


class InfoWindow(QMainWindow):
    def __init__(self, image):
        super().__init__()
        self.path = '\\'.join(os.getcwd().split('\\')[:-1])
        self.str_img = image
        uic.loadUi(self.path + '\\menu_and_game\\menu_data\\info_window.ui', self)
        self.setWindowIcon(QIcon(self.path + '\\menu_and_game\\menu_data\\icon.png'))
        pixmap = QPixmap(self.path + f'\\menu_and_game\\game_data\\{image}.png')
        self.load_data()
        scaled_pixmap = pixmap.scaled(120, 200)
        self.img_label.setPixmap(scaled_pixmap)
        self.close_btn.clicked.connect(self.quit)
        self.show()

    def load_data(self):
        need_data = None
        with open(self.path + '\\menu_and_game\\menu_data\\data.txt', encoding='utf-8') as data:
            all_data = data.read().split('\n')
        for i in all_data:
            if i.split(':')[0] == self.str_img:
                need_data = i
        self.name_label.setText(need_data.split(':')[1].split(',')[0][2:-1])
        self.speed_label.setText(need_data.split(':')[1].split(',')[1])
        self.price_label.setText(need_data.split(':')[1].split(',')[2])

    def quit(self):
        self.close()


app = QApplication(sys.argv)
info = InfoWindow(sys.argv[1])
sys.exit(app.exec())
