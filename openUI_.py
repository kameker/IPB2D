from os import listdir
from os.path import isfile, join
from PyQt5 import QtWidgets
from openUI import Ui_Dialog
from main import run


class ExampleApp(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fields = [f[0:-5] for f in listdir('fields') if isfile(join('fields', f))]
        self.name.setText(self.fields[0])
        self.k = 0
        self.b = 0
        self.right.clicked.connect(self.ToRight)
        self.pushButton_3.clicked.connect(self.ToLeft)
        self.pushButton.clicked.connect(self.openf)


    def ToRight(self):
        if self.k + 1 == len(self.fields):
            self.k = 0
        else:
            self.k += 1
        self.name.setText(self.fields[self.k])

    def ToLeft(self):
        if self.k == 0:
            self.k = len(self.fields) - 1
        else:
            self.k -= 1
        self.name.setText(self.fields[self.k])

    def openf(self):
        run(self.fields[self.k])

def loadf():
    global window2
    window2 = ExampleApp()
    window2.show()
