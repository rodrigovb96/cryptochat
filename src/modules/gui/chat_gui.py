from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QTimer
import sys

import time
import socket, pickle


class chat_window(QWidget):

    closed = pyqtSignal()
    signal_start_sender_job = pyqtSignal(int,int,str)
    signal_start_receiver_job = pyqtSignal(int,int)
    signal_stop_receiver_job = pyqtSignal()

    def __init__(self, parent=None,receiver="Friend",username="User"):
        super(chat_window, self).__init__()
        self.setWindowTitle(receiver)
	
        self.setFixedSize(640,480)
        self.init_components()
        self.init_sender_thread()

        self.username = username
        self.receiver = receiver

        self.init_receiver_thread()

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.start()

    def init_components(self) -> None:

        self.user_id = 0 #TODO
        self.friend_id = 1#TODO
	 
        self.chat_text = QTextEdit()
        self.input_text = QTextEdit()

        self.send_btn = QPushButton("Enviar",self)
        self.send_btn.setStyleSheet("background-color: #F7CE16") # botão enviar fica amarelo
        self.send_btn.clicked.connect(self.send_msg)

        self.clear_btn = QPushButton("Limpar",self)
        self.clear_btn.clicked.connect(self.clear_msg)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.chat_text,5)
        self.layout.addWidget(self.input_text,1)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.send_btn)
        self.btn_layout.addWidget(self.clear_btn)
     
        self.layout.addLayout(self.btn_layout)
        
        self.chat_text.setReadOnly(True)
        self.setLayout(self.layout)

    def init_sender_thread(self) -> None:

        self.sender_socket = sender_thread()
        self.sender_socket.result.connect(self.msg_sended)
        self.sender_t = QThread(self)

        self.sender_socket.moveToThread(self.sender_t)
        
        self.signal_start_sender_job.connect(self.sender_socket.connect)

    def init_receiver_thread(self) -> None:
        self.receiver_socket = receiver_thread()
        self.receiver_socket.has_msg.connect(self.update_chat)

        self.receiver_t = QThread(self)
        
        self.receiver_t.finished.connect(self.receiver_socket.stop) 

        self.receiver_socket.moveToThread(self.receiver_t)
        self.signal_start_receiver_job.connect(self.receiver_socket.connect)
        self.signal_stop_receiver_job.connect(self.receiver_socket.stop)

        self.receiver_t.start()
        self.signal_start_receiver_job.emit(self.user_id,self.friend_id)

    def closeEvent(self,event) -> None: 
        print("QUITING")
        #self.signal_stop_receiver_job.emit()
        self.receiver_t.quit()
        self.receiver_t.wait()
        
    def invalid_input(self) -> bool:
        return not self.input_text.toPlainText()

    @pyqtSlot(str)
    def update_chat(self,msg) -> None:
        self.chat_text.append(self.receiver+ ": " + msg)



    
    @pyqtSlot()
    def msg_sended(self) -> None:
       self.sender_t.quit()
       self.sender_t.wait()
       self.chat_text.append(self.username+ ": " + self.input_text.toPlainText())
       self.input_text.clear()

    @pyqtSlot()
    def send_msg(self) -> None:
        
        if not self.invalid_input(): 
            self.sender_t.start()
            self.signal_start_sender_job.emit(self.user_id,self.friend_id,self.input_text.toPlainText())

    @pyqtSlot()
    def clear_msg(self) -> None:
       self.input_text.clear()


class sender_thread(QObject):

    result = pyqtSignal()

    @pyqtSlot(int,int,str)
    def connect(self,user_id,receiver_id,msg) -> None:

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(("127.0.0.1",12345))

        soc.send("--SMSGREQ--".encode("utf8"))

        if "--OKTOSEND--" in soc.recv(4096).decode("utf8"):
            soc.send(pickle.dumps({"sender":user_id, "receiver":receiver_id,"msg":msg}))


        while "--OKTOSEND--" not in soc.recv(4096).decode("utf8"):
            pass
        
        self.result.emit()

class receiver_thread(QObject):

    has_msg = pyqtSignal(str)

    def __init__(self,parent=None):
        super(receiver_thread,self).__init__()
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.soc.setblocking(False)
        self.still_listen = True

    @pyqtSlot(int,int)
    def connect(self,user_id,sender_id) -> None:
        self.soc.connect(("127.0.0.1",12345))

        self.soc.send("--RMSGREQ--".encode("utf8"))

        if "--OKTOSEND--" in self.soc.recv(4096).decode("utf8"):
            self.soc.send(pickle.dumps( {"receiver" : user_id, "sender" : sender_id} ))

            while self.still_listen:
                    self.has_msg.emit(self.soc.recv(4096).decode("utf8"))
                    self.soc.send("--OKTOSEND--".encode("utf8"))
        
        self.soc.send("--ENDOFCHAT--".encode("utf8"))




    @pyqtSlot()
    def stop(self) -> None:
        self.still_listen = False
                 
    


