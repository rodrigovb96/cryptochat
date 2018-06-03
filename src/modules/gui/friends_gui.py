from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject

import os,sys

from modules.gui.chat_gui import chat_window 
import socket,pickle


class friends_list(QWidget):

    def __init__(self, parent=None):
        super(friends_list,self).__init__()
        self.setWindowTitle("Amigos")
        self.setFixedSize(200,600)

        self.init_list()

        self.layout.addWidget(self.listWidget)

        self.setLayout(self.layout)

    def init_list(self) -> None:

        self.layout = QHBoxLayout()		

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemDoubleClicked.connect(self.open_chat)

        for i in range(10):
            self.listWidget.addItem("Teste{}".format(i))

    @pyqtSlot(QListWidgetItem) 
    def open_chat(self,user) -> None:
        setattr(self,user.text()+'_chat',chat_window(username=user.text()))
        getattr(self,user.text()+'_chat').show()


def start():#TEMP
    app = QApplication(sys.argv)
    login = friends_list()
    login.show()
    sys.exit(app.exec_())
