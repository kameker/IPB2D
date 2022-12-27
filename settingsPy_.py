import json
import math
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QButtonGroup

from settingsPy import Ui_Form


class Class_settings(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.save.clicked.connect(self.fsave)
        self.gb = QButtonGroup()
        self.gb.addButton(self.static_b)
        self.gb.addButton(self.dynamic_b)
        self.objects = []

    def show_settings(self, objects):
        f = str(objects[0])[15:str(objects[0]).index(' ')]
        if f == "Circle":
            size = objects[0].radius
            h = 0
            self.height.hide()
            self.label_2.hide()
            self.label.setText("Радиус")
        elif f == "Poly":
            size = abs(objects[0].get_vertices()[0][0])
            h = abs(objects[0].get_vertices()[0][1])
        self.objects = objects
        self.line_mass.setText(str(objects[0].mass))
        self.line_friction.setText(str(objects[0].friction))
        self.line_elasticity.setText(str(objects[0].elasticity))
        self.line_color.setText(str(objects[0].color))
        self.angle.setText(str(float(str(objects[1]._get_angle())[0:10]) * 180 / 3.1415926535)[0:7])
        self.wr.setText(str(size))
        self.height.setText(str(h))
        self.X.setText(str(objects[1].position[0])[0:6])
        self.Y.setText(str(objects[1].position[1])[0:6])
        if objects[1].body_type == 1:
            self.static_b.setChecked(True)
        else:
            self.dynamic_b.setChecked(True)

    def save_so(self):
        color = [int(i) for i in self.line_color.text()[1:-1].split(", ")]
        f = str(self.objects[0])[15:str(self.objects[0]).index(' ')]
        if f == "Circle":
            t = 0
            size = float(self.wr.text())
            size2 = float(self.wr.text())
            s = self.objects[0].radius
        elif f == "Poly":
            t = 4
            size = [float(self.wr.text()), float(self.height.text())]
            size2 = float(self.wr.text())
            s = abs(self.objects[0].get_vertices()[0][0])
            h = abs(self.objects[0].get_vertices()[0][1])
        if self.static_b.isChecked():
            print(1)
            btype = 1
        else:
            btype = 0
            print(0)
        d = {0: {
            "mass": float(self.line_mass.text()),
            "friction": float(self.line_friction.text()),
            "elasticity": float(self.line_elasticity.text()),
            "color": color,
            'position': [float(self.X.text()), float(self.Y.text())],
            'shape': t,
            'body_type': btype,
            'args': size,
            'angle': float(self.angle.text()) * 3.1415926535 / 180
        }}
        data = json.dumps(d)
        data = json.loads(str(data))
        with open('object.json', "w") as file:
            json.dump(data, file, indent=4)
    def fsave(self):
        self.save_so()
        print('save')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def start(objects):
    app = QtWidgets.QApplication(sys.argv)
    window4 = Class_settings()
    window4.show()
    window4.show_settings(objects)
    sys.excepthook = except_hook
    app.exec_()
