from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 

import os,sys

from modules.gui.chat_gui import chat_window 
import socket,pickle


class friends_list(QWidget):


    closed = pyqtSignal()
    search_friend_signal = pyqtSignal()
    friends = []

    def __init__(self, parent=None,username="user"):
        super(friends_list,self).__init__()
        self.setWindowTitle("Amigos")
        self.setFixedSize(200,600)

        self.username=username

        self.search_layout = QHBoxLayout()		

        self.search_field = QLineEdit()
        self.search_btn = QPushButton("Buscar",self)
        self.search_btn.clicked.connect(self.search_friend)

        self.search_layout.addWidget(self.search_field)
        self.search_layout.addWidget(self.search_btn)
        
        self.layout = QVBoxLayout()
        
        self.init_list()

        self.layout.addLayout(self.search_layout)
        self.layout.addWidget(self.listWidget)

        self.setLayout(self.layout)

        self.thread_pool = [] 
        self.receiver_pool = []
        self.chat_pool = []



    def init_list(self) -> None:
        self.listWidget = QListWidget()
        self.listWidget.setObjectName("listFriends")
        self.listWidget.itemDoubleClicked.connect(self.open_chat)
        
        self.get_friends()

        for friend in self.friends:
            self.listWidget.addItem(friend[1])
        self.listWidget.repaint()
        
            
    def get_friend_info(self,friend_name):
        for friend in self.friends:
            if friend_name == friend[1]:
                return [friend[0],friend[1],friend[2]]
        

    def get_friends(self) -> None:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        soc.connect(("192.168.100.48", 12345))

        soc.send("--SEARCHALL--".encode("utf8"))

        soc.send(self.username.encode("utf8"))
        
        import struct
        buf = b''

        while len(buf) < 4:
            buf += soc.recv(4-len(buf))

        length = struct.unpack('!I',buf)[0]

        data = b''

        l = length

        while l > 0:
            d = soc.recv(l)
            l -= len(d)
            data += d

        self.friends = pickle.loads(data) 


    def update_list(self,friend) -> None:
        self.listWidget.addItem(friend[1])
        self.listWidget.repaint()




    @pyqtSlot(object)
    def add_friend(self,friend) -> None:
        print(self.friends)
        self.friends.append(friend)
        self.update_list(friend)
        self.thread.quit()
        self.thread.wait()

    @pyqtSlot()
    def search_friend(self) -> None: 
        self.friend_name = self.search_field.text()
        self.worker = search_friend_thread(self.username,self.friend_name)
        self.thread = QThread(self)
        self.worker.moveToThread(self.thread)
        self.search_friend_signal.connect(self.worker.run)
        self.worker.result.connect(self.add_friend)
        self.thread.start()
        self.search_friend_signal.emit()
        self.search_field.setText("")
    
        

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
            
            print("DEBUG")
            friend_info = self.get_friend_info(receiver.text())
            print(friend_info)

            self.chat_pool.append(chat_friend_thread(id_=len(self.thread_pool)-1,sender=self.username,receiver=friend_info))
            self.receiver_pool.append(receiver.text())
            self.thread_pool.append(QThread(self))
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


class search_friend_thread(QObject): 
    
    result = pyqtSignal(object)

    def __init__(self,username,friend):
        super(search_friend_thread, self).__init__()
        self.username  = username
        self.friend = friend 

    @pyqtSlot()
    def run(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        soc.connect(("192.168.100.48", 12345))

        soc.send("--SEARCHREQ--".encode("utf8"))
        soc.send(pickle.dumps({"username" : self.username.encode("utf8"), "friend" : self.friend.encode("utf8")}))
        result_bytes = soc.recv(4096)
        result = pickle.loads(result_bytes)
            
        
        self.result.emit(result)
        


        




