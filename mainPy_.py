import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from mainPy import Ui_IPB2D
from main import run


def set_new_field():
    run()


class ExampleApp(QtWidgets.QMainWindow, Ui_IPB2D):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.newField.clicked.connect(set_new_field)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
