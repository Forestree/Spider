from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Chat.chat
import sys
import socket
import threading
from colorama import Fore, Style
import subprocess

HOST = '127.0.0.1'
LISTEN_PORT = 8900        # Port to listen on (non-privileged ports are > 1023)
CONNECT_PORT = 8901
client_ip = "127.0.0.1"
is_working = True
messages = []


def is_ip(ip):
    ip = ip.split('.')
    if len(ip) != 4:
        return False
    for x in ip:
        try:
            x = int(x)
        except ValueError:
            return False
    return True


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(580, 507)
        MainWindow.setMinimumSize(QtCore.QSize(580, 507))
        MainWindow.setMaximumSize(QtCore.QSize(580, 507))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("QWidget{\n"
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
                    "}"
                    "QPushButton:hover{"
                    "    background-color:#438542;"
                    "}"
                    "QPushButton:pressed{"
                    "    background-color:#3d7b3d;"
                    "}")

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
        # self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit.setGeometry(QtCore.QRect(201, 171, 178, 43))
        # self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(201, 232, 178, 43))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.centralwidget_chat = QtWidgets.QWidget(MainWindow)
        self.centralwidget_chat.setObjectName("centralwidget_chat")
        self.centralwidget_chat.setStyleSheet("QWidget{\n"
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
        self.widget = QtWidgets.QWidget(self.centralwidget_chat)
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
                              "}"
                              "QPushButton:hover{"
                              "    background-color: #F0F0F0;"
                              "}"
                              "QPushButton:pressed{"
                              "    background-color: #BEBEBE;"
                              "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget_chat)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 580, 391))
        self.listWidget.setStyleSheet("border:none;")
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSpacing(5)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("MainWindow", "Connect"))
        self.label.setText(_translate("MainWindow", "Your ip is " + HOST))
        # self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter your username"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Enter your friend ip:port"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Type text to send here"))
        self.pushButton_2.setText(_translate("MainWindow", "Send"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.send)
        self.is_working = False
        self.th = None

    def listen_in_thread(self):
        if not self.is_working:
            self.th = threading.Thread(target=self.listen)
            self.is_working = True
            self.th.start()

    def connect(self):
        global CONNECT_PORT
        global client_ip
        ip_port = self.lineEdit_2.text()
        client_ip, port = ip_port.split(':')
        CONNECT_PORT = int(port)
        self.connect_to()

    def connect_to(self):
        global client_ip, is_working
        # client_ip = self.lineEdit_2.text()
        print(client_ip)
        self.setCentralWidget(self.centralwidget_chat)
        # self.listen_in_thread()

    def send(self, message=''):
        if not message:
            message = self.textEdit.toPlainText()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print((client_ip, CONNECT_PORT))
            s.connect((client_ip, CONNECT_PORT))
            s.sendall(message.encode(encoding="utf-8"))
            # data = s.recv(4096*4096)
            data = s.recv(4096*4)

        print(Fore.RED + 'Received', repr(data))
        print(Style.RESET_ALL)
        item = QtWidgets.QListWidgetItem()
        # item.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        item.setFont(font)
        item.setText(message)
        self.listWidget.addItem(item)
        self.textEdit.setText("")

    def show_data(self, data):
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)

        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        item.setFont(font)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setText(data)
        self.listWidget.addItem(item)


    def listen(self):
        global is_working
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, LISTEN_PORT))
            while True:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    self.setCentralWidget(self.centralwidget_chat)
                    print('Connected by', addr)
                    while True and is_working:
                        # data = conn.recv(4096*4096).decode()
                        data = conn.recv(4096*4).decode()
                        if not data:
                            break
                        else:
                            messages.append(data)
                            self.show_data(data)
                            # self.listWidget.addItem(item)
                        print(Fore.GREEN + data)
                        print(Style.RESET_ALL)
                        conn.sendall(data.encode(encoding="utf-8"))


