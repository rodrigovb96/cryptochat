from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

import os,sys

from modules.gui.chat_gui import chat_window 
import socket,pickle


class friends_list(QWidget):


    closed = pyqtSignal()

    def __init__(self, parent=None,username="user"):
        super(friends_list,self).__init__()
        self.setWindowTitle("Amigos")
        self.setFixedSize(200,600)

        self.username=username

        self.init_list()

        self.layout.addWidget(self.listWidget)

        self.setLayout(self.layout)

        self.thread_pool = [] 
        self.receiver_pool = []
        self.chat_pool = []


        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.start()
        

    def init_list(self) -> None:

        self.layout = QHBoxLayout()		

        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listFriends")
        self.listWidget.itemDoubleClicked.connect(self.open_chat)

        for i in range(10): #TEMP 
            self.listWidget.addItem("Teste{}".format(i))

    def closeEvent(self,event):
        for thread in self.thread_pool:
            thread.quit()
            thread.wait()
        self.closed.emit()

    @pyqtSlot(int)
    def end_thread(self,id_) -> None:
        print(id_)
        self.thread_pool[id_].quit()
        self.thread_pool[id_].wait()
        self.thread_pool.pop(id_)
        self.receiver_pool.pop(id_)


    @pyqtSlot(QListWidgetItem)
    def open_chat(self,receiver) -> None:

        if receiver.text() not in self.receiver_pool:
            self.chat_pool.append(chat_friend_thread(id_=len(self.thread_pool)-1,sender=self.username,receiver=receiver.text()))
            self.receiver_pool.append(receiver.text())
            self.thread_pool.append(QThread())
            self.chat_pool[-1].moveToThread(self.thread_pool[-1])
            self.chat_pool[-1].finished.connect(self.end_thread)
            self.thread_pool[-1].start()



class chat_friend_thread(QObject):

    finished = pyqtSignal(int)

    def __init__(self,id_,sender,receiver):
        super(chat_friend_thread, self).__init__()

        self.id = id_
        self.sender = sender
        self.receiver = receiver
        
        self.chat_win = chat_window(username=self.sender,receiver=self.receiver)
        self.chat_win.closed.connect(self.done)
        self.chat_win.show()

    @pyqtSlot()
    def done(self) -> None:
        self.finished.emit(self.id)

    def chat(self) -> None:
        if self.chat_win.isVisible() == False:
            self.finished.emit(self.id)



def start():#TEMP
    app = QApplication(sys.argv)
    login = friends_list(username="Rodrigo") # TEMP 
    login.show()
    sys.exit(app.exec_())
