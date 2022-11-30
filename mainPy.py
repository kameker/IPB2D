from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IPB2D(object):
    def setupUi(self, IPB2D):
        IPB2D.setObjectName("IPB2D")
        IPB2D.resize(1120, 801)
        self.centralwidget = QtWidgets.QWidget(IPB2D)
        self.centralwidget.setObjectName("centralwidget")
        self.newField = QtWidgets.QPushButton(self.centralwidget)
        self.newField.setGeometry(QtCore.QRect(450, 290, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.newField.setFont(font)
        self.newField.setObjectName("newField")
        self.loadField = QtWidgets.QPushButton(self.centralwidget)
        self.loadField.setGeometry(QtCore.QRect(470, 370, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.loadField.setFont(font)
        self.loadField.setObjectName("loadField")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 101, 20))
        self.label.setObjectName("label")
        IPB2D.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(IPB2D)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 21))
        self.menubar.setObjectName("menubar")
        IPB2D.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(IPB2D)
        self.statusbar.setObjectName("statusbar")
        IPB2D.setStatusBar(self.statusbar)

        self.retranslateUi(IPB2D)
        QtCore.QMetaObject.connectSlotsByName(IPB2D)

    def retranslateUi(self, IPB2D):
        _translate = QtCore.QCoreApplication.translate
        IPB2D.setWindowTitle(_translate("IPB2D", "MainWindow"))
        self.newField.setText(_translate("IPB2D", "Создать новое поле"))
        self.loadField.setText(_translate("IPB2D", "Загрузить поле"))
        self.label.setText(_translate("IPB2D", "IPB2D - 1.0"))
