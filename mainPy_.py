import sys
from PyQt5 import QtWidgets
from mainPy import Ui_IPB2D
from main import run
from openUI_ import loadf


class ExampleApp(QtWidgets.QMainWindow, Ui_IPB2D):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.newField.clicked.connect(self.sf)
        self.loadField.clicked.connect(self.loadf)

    def sf(self):
        run("")
        self.close()

    def loadf(self):
        loadf()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    sys.excepthook = except_hook
    app.exec_()
