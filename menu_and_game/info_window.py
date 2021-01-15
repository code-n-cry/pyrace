from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
import os
import sys
import json


class InfoWindow(QMainWindow):
    """Информация о машине(изображения, название, скорость, цена)"""

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
        with open(self.path + '\\menu_and_game\\game_data\\cars.json', encoding='utf-8') as data:
            all_data = json.load(data)
        for i in all_data['cars']:
            if i['id'] == self.str_img:
                need_data = i
        self.name_label.setText(need_data['name'])
        self.speed_label.setText(str(need_data['speed']))
        self.price_label.setText(str(need_data['price']))

    def quit(self):
        self.close()


app = QApplication(sys.argv)
info = InfoWindow(sys.argv[1])
sys.exit(app.exec())
