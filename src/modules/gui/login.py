from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject

from modules.crypto import CryptoEngine

from modules.gui.friends_gui import friends_list 
import os,sys

from .. import user
import socket,pickle




class login_window(QWidget):

    signal_start_background_job = pyqtSignal(user.ChatUser)    

    def __init__(self, parent=None):
        super(login_window,self).__init__()
        self.setWindowTitle("Login")

        self.setFixedSize(200,200)

        self.init_components()

        self.init_thread()


    
    def init_components(self) -> None:
        self.user_ = None 

        self.layout = QVBoxLayout()		

        self.label_name = QLabel()
        self.label_pass = QLabel()
        
        self.label_name.setText("Nome:")
        self.label_pass.setText("Senha:")

        self.login_btn = QPushButton("Logar",self)
        self.login_btn.clicked.connect(self.login)
        
        self.name_text = QLineEdit()
        self.password_text = QLineEdit()
        self.password_text.setEchoMode(QLineEdit.Password)
        
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.name_text)

        self.layout.addWidget(self.label_pass)
        self.layout.addWidget(self.password_text)

        self.layout.addWidget(self.login_btn)
        
        self.setLayout(self.layout)
    
    def init_thread(self) -> None:
        self.socket = login_thread()
        self.socket.result.connect(self.auth_result)
        self.thread = QThread(self)

        self.socket.moveToThread(self.thread)

        self.signal_start_background_job.connect(self.socket.connect)

    def valid_input(self) -> bool:
        if not self.name_text.text() and not self.password_text.text():
            return False 
        else:
            return True 
                
    def clear_components(self) -> None:
        self.name_text.setText("")
        self.password_text.setText("")
    
    @pyqtSlot()	
    def login(self) -> None:
        if self.valid_input() == True:
            try:
                self.user_= user.ChatUser(username=self.name_text.text(),password=self.password_text.text())
            except ValueError as error:
                QMessageBox.critical(self,"Erro!","Usuário ou Senha Inválidos!\nInsira os dados novamente.", QMessageBox.Ok)
                self.clear_components()
            else:
                # Se o input for válido tenta a conexão com o banco
                self.name_text.setEnabled(False)
                self.password_text.setEnabled(False)
                self.login_btn.setEnabled(False)
                self.call_auth_socket()
               
        else:
            QMessageBox.warning(self,"Erro!","Valores Informados Inválidos", QMessageBox.Ok)
    

    def call_auth_socket(self):
        self.thread.start()
        self.signal_start_background_job.emit(self.user_)

    @pyqtSlot(str)
    def auth_result(self,auth_flag):
        self.thread.quit()
        self.thread.wait()
        
        if auth_flag == 'True':
            self.close()
            self.friends_win = friends_list(username=self.user_.get_username());

            self.friends_win.show()
        else:
            QMessageBox.warning(self,"Erro!","Problemas na conexão com o banco", QMessageBox.Ok) # Warning de exemplo
            self.name_text.setEnabled(True)
            self.password_text.setEnabled(True)
            self.login_btn.setEnabled(True)
            self.clear_components()
            # Lidar com erros de conexão ou autenticação do banco




''' 
    Thread para fazer conexão com banco
    e realizar a autenticação do usuário
'''
class login_thread(QObject):
    result = pyqtSignal(str)

    @pyqtSlot(user.ChatUser)
    def connect(self,user) -> None:

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        soc.connect(("192.168.100.48", 12345))

        soc.send("--LOGINREQ--".encode("utf8")) # Login request

        public_key = soc.recv(4096)

        encrypt_obj = CryptoEngine()
        encrypt_obj.init_RSA_mode(key=public_key)

        username = encrypt_obj.encrypt_RSA_string(raw_str=user.get_username().encode("utf8")) 
        password = encrypt_obj.encrypt_RSA_string(raw_str=user.get_password().encode("utf8")) 
		
        pb_key = user.get_user_publicKey()
        
        soc.send(pickle.dumps({"user" : username,  "password" : password , "publickey" : pb_key}))

        result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
        result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
        self.result.emit(result_string)
        



        







def start():
    app = QApplication(sys.argv)
    login = login_window()
    login.show()
    sys.exit(app.exec_())
    


