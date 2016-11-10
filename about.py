# Author: Mohan Ravi
# Vesrion: 1.0
# Dependencies: PyQt5, Xlib, Python3.5
# Description: Caps and Num lock indicator using python
# License: GPL Version 3 https://www.gnu.org/licenses/gpl-3.0.txt
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 325)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "About - CapsNumLockIndicator"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/images/logo.png\"/></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">About CapsNumLockIndicator</span></p><p align=\"justify\">Version: <span style=\" font-size:10pt; font-weight:600; color:#0000ff;\">1.0</span></p><p align=\"justify\">Caps Num Lock indicator helps you to identify present status of caps and Numpad. This software is created because in some keyboards you cannot see led indicators to show the status of caps and numpad ON or OFF. I have created this software because am facing the same problem and decided to share it with everyone. </p><p align=\"justify\"><br/>This Software comes with absolutely no warranty.</p><p align=\"justify\">For More details visit <a href=\"http://www.gnu.org/licenses/gpl-3.0.html\"><span style=\" text-decoration: underline; color:#0000ff;\">GNU GPL License</span></a></p><p align=\"justify\">For Source code please Visit <a href=\"https://github.com/immohanravi/CapsNumLockIndicator\"><span style=\" text-decoration: underline; color:#0000ff;\">Github</span></a></p></body></html>"))

import images_rc