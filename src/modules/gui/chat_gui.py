from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QTimer
import sys

from Crypto.Random import get_random_bytes

from .. import crypto
from .. import message

import time
import socket, pickle


class chat_window(QWidget):

    closed = pyqtSignal()
    signal_start_sender_job = pyqtSignal(object,str,str,bytes,bytes,bytes)
    signal_start_receiver_job = pyqtSignal(int,int)
    signal_stop_receiver_job = pyqtSignal()

    def __init__(self, parent=None,receiver=[],user=None,pb_key="None"):
        super(chat_window, self).__init__()
        self.setWindowTitle(receiver[1])
	
        self.setFixedSize(640,480)
        self.init_components()
        self.init_sender_thread()

        self.user_ = user
        self.username = user.get_username() 
        self.pb_key = pb_key

        self.friend_id = receiver[0]
        self.friend_name = receiver[1]
        print(self.friend_name)
        self.friend_pb = receiver[2]

        #self.init_receiver_thread()
    
        self.generate_AES_keyset()

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.start()

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

    def generate_AES_keyset(self) -> None:

        self.AES_KEY = get_random_bytes(16)

        key_user = crypto.CryptoEngine() 
        key_user.init_RSA_mode(self.pb_key)

        self.AES_KEY_USER = key_user.encrypt_RSA_string(raw_str=self.AES_KEY)

        key_friend = crypto.CryptoEngine() 
        key_friend.init_RSA_mode(self.friend_pb)
        
        self.AES_KEY_FRIEND = key_friend.encrypt_RSA_string(raw_str=self.AES_KEY)



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
        self.signal_start_receiver_job.emit(self.username,self.friend_id)

    def closeEvent(self,event) -> None: 
        print("QUITING")
        #self.signal_stop_receiver_job.emit()
        self.receiver_t.quit()
        self.receiver_t.wait()
        
    def invalid_input(self) -> bool:
        return not self.input_text.toPlainText()

    @pyqtSlot(str)
    def update_chat(self,msg) -> None:
        self.chat_text.append(self.friend_name+ ": " + msg)



    
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
            self.signal_start_sender_job.emit(self.user_,self.friend_name,self.input_text.toPlainText(),self.AES_KEY,self.AES_KEY_USER,self.AES_KEY_FRIEND)

    @pyqtSlot()
    def clear_msg(self) -> None:
       self.input_text.clear()


class sender_thread(QObject):

    result = pyqtSignal()

    @pyqtSlot(object,str,str,bytes,bytes,bytes)
    def connect(self,user,receiver_name,msg,AES_KEY,AES_KEY_pb1,AES_KEY_pb2) -> None:

        print(user.get_password())
        import datetime
        message_ = message.Message(sender=user,receiver=receiver_name,date=datetime.date.today(),text=msg)



        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect(("192.168.100.48",12345))

        soc.send("--SMSGREQ--".encode("utf8"))
        soc.send(pickle.dumps({"sender" : user.get_username() , "receiver" : receiver_name}))

        result = soc.recv(4096).decode("utf8")

        if "--OKTOSEND--" in result: 
            AES_KEY_encrypt = soc.recv(4096)
            
            engine = crypto.CryptoEngine()
            engine.init_RSA_mode(key=user.get_user_privateKey(),_passphrase=user.get_password())
            AES_KEY_ = engine.decrypt_RSA_string(AES_KEY_encrypt)


            soc.send(message_.get_string(AES_KEY_))
            
            if "--OK--" in soc.recv(4096).decode("utf8"):
                self.result.emit()
             
        elif "--NOCONV--" in result:  
            print(user.get_user_privateKey())

            soc.send(pickle.dumps({ "AES_USER" : AES_KEY_pb1 , "AES_FRIEND" : AES_KEY_pb2}))

            if "--OKTOSEND--" in soc.recv(4096).decode("utf8"): 
                soc.send(message_.get_string(AES_KEY))

            if "--OK--" in soc.recv(4096).decode("utf8"):
                self.result.emit()
            

        



class receiver_thread(QObject):

    has_msg = pyqtSignal(str)

    def __init__(self,parent=None):
        super(receiver_thread,self).__init__()
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.still_listen = True

    @pyqtSlot(int,int)
    def connect(self,user_id,sender_id) -> None:
        self.soc.connect(("192.168.100.48",12345))

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
                 
    


