# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(580, 507)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color:#FFF;\n"
"}\n"
"QTextEdit {\n"
"    border: 1px solid #B1B1B1;\n"
"    border-radius:8px;\n"
"    background-color: #F0F0F0;\n"
"    color: #6F6F6F;\n"
"    font-family: \"Helvetica\";\n"
"    font-size: 16px;\n"
"    padding:5px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 426, 580, 81))
        self.widget.setStyleSheet("background-color:#EEE;")
        self.widget.setObjectName("widget")
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setGeometry(QtCore.QRect(12, 15, 441, 54))
        self.textEdit.setStyleSheet("background-color:#D8D8D8;")
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(469, 16, 96, 54))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"    margin:0;\n"
"    width:100%;\n"
"    height:100%;\n"
"    border: 1px solid #979797;\n"
"    border-radius: 8px;\n"
"    background-color: #FBFBFB;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #F0F0F0;\n"
"}\n"
"QPushbutton:active{\n"
"    background-color: #BEBEBE;\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(436, 2, 138, 31))
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 35, 580, 391))
        self.listWidget.setStyleSheet("border:none;")
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        item.setFont(font)
        self.listWidget.addItem(item)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Type text to send here"))
        self.pushButton_2.setText(_translate("MainWindow", "Send"))
        self.pushButton.setText(_translate("MainWindow", "Close connection"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Hallo", "Friend"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Hello"))
        self.listWidget.setSortingEnabled(__sortingEnabled)

