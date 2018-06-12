from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import sys

import socket, pickle


class chat_window(QWidget):

    closed = pyqtSignal()
    signal_start_background_job = pyqtSignal(str)

    def __init__(self, parent=None,receiver="Friend",username="User"):
        super(chat_window, self).__init__()
        self.setWindowTitle(receiver)
	
        self.setFixedSize(640,480)
        self.init_components()
        self.init_thread()
        self.username = username

    def init_components(self) -> None:
	
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

    def init_thread(self) -> None:

        self.socket = sender_thread()
        self.socket.result.connect(self.msg_sended)
        self.thread = QThread(self)

        self.socket.moveToThread(self.thread)
        
        self.signal_start_background_job.connect(self.socket.connect)

    def closeEvent(self,event) -> None:
        self.thread.start()
        self.signal_start_background_job.emit("--ENDOFDATA--")
        self.closed.emit()
        
    def invalid_input(self) -> bool:
        return not self.input_text.toPlainText()


    @pyqtSlot()
    def msg_sended(self):
       self.chat_text.append(self.username+ ": " + self.input_text.toPlainText())
       self.input_text.clear()

    @pyqtSlot()
    def send_msg(self) -> None:
        
        if not self.invalid_input(): 
            self.thread.start()
            self.signal_start_background_job.emit(self.input_text.toPlainText())

    @pyqtSlot()
    def clear_msg(self) -> None:
       self.input_text.clear()


class sender_thread(QObject):

    result = pyqtSignal()

    @pyqtSlot(str)
    def connect(self,msg) -> None:

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(("127.0.0.1",12345))

        print(msg)

        soc.send(msg.encode("utf8"))

        while "--OKTOSEND--" not in soc.recv(4096).decode("utf8"):
            pass

        self.result.emit()





