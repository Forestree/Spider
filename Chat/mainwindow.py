# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(580, 507)
        MainWindow.setMinimumSize(QtCore.QSize(580, 507))
        MainWindow.setMaximumSize(QtCore.QSize(580, 507))
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color:#FFF;\n"
"}\n"
"QLineEdit {\n"
"    border: 1px solid #B1B1B1;\n"
"    border-radius:8px;\n"
"    background-color: #F0F0F0;\n"
"    color: #6F6F6F;\n"
"    font-family: \"Helvetica\";\n"
"    font-size: 16px;\n"
"    padding:5px;\n"
"}\n"
"QPushButton{\n"
"    border: 1px solid #DADADA;\n"
"    border-radius: 8px;\n"
"    background-color: #488E46;\n"
"    color: #FFF;\n"
"    font-family: \"Helvetica\";\n"
"    font-size: 16px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(201, 293, 178, 38))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(195, 134, 191, 19))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(201, 171, 178, 43))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(201, 232, 178, 43))
        self.lineEdit_2.setObjectName("lineEdit_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Messenger"))
        self.pushButton.setText(_translate("MainWindow", "Connect"))
        self.label.setText(_translate("MainWindow", "Your ip is 255.255.255.255"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter your username"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Enter your friend ip"))

