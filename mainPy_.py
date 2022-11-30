import sys
from PyQt5 import QtWidgets
from mainPy import Ui_IPB2D
from main import run


class ExampleApp(QtWidgets.QMainWindow, Ui_IPB2D):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.newField.clicked.connect(self.sf)

    def sf(self):
        self.close()
        run()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
