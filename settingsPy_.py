import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from settingsPy import Ui_Form
from main import run




class ExampleApp(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
