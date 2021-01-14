from PyQt5.QtCore import *


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        if self.args and self.kwargs:
            self.fn(*self.args, self.kwargs)
        else:
            self.fn()
