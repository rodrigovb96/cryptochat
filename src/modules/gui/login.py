from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject


from modules.gui.chat_gui import chat_window
import os,sys

from .. import user

import time

''' 
    @DEBUG 
''' 
def log(**kwargs):
    print('*'*30)
    print("DEBUG:")
    for key in kwargs:
        print("{} : {}".format(key,kwargs[key]))
    print('*'*30)


class login_window(QWidget):

    signal_start_background_job = pyqtSignal()    

    def __init__(self, parent=None):
        super(login_window,self).__init__()
        self.setWindowTitle("Login")

        self.setFixedSize(200,200)

        self.init_components()

        self.init_thread()


    
    def init_components(self) -> None:
        self.layout = QVBoxLayout()		

        self.label_name = QLabel()
        self.label_pass = QLabel()
        
        self.label_name.setText("Nome:")
        self.label_pass.setText("Senha:")

        self.login_btn = QPushButton("Logar",self)
        self.login_btn.clicked.connect(self.connect)
        
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

        self.signal_start_background_job.connect(self.socket.test)

    def valid_input(self) -> bool:
        if not self.name_text.text() and not self.password_text.text():
            return False 
        else:
            return True 
                
    def clear_components(self) -> None:
        self.name_text.setText("")
        self.password_text.setText("")
    
    @pyqtSlot()	
    def connect(self) -> None:
        if self.valid_input() == True:
            try:
                user_= user.ChatUser(username=self.name_text.text(),password=self.password_text.text())
                user_.set_rsaKey()
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
        self.signal_start_background_job.emit()

    @pyqtSlot(bool)
    def auth_result(self,auth_flag):
        self.thread.quit()
        self.thread.wait()
        
        if auth_flag == True:
            self.close()
            self.chat_win = chat_window(self,username=self.name_text.text())
            self.chat_win.show()
        else:
            QMessageBox.warning(self,"Erro!","Problemas na conexão com o banco", QMessageBox.Ok) # Warning de exemplo
            self.clear_components()
            # Lidar com erros de conexão ou autenticação do banco
            pass




''' 
    Thread para fazer conexão com banco
    e realizar a autenticação do usuário
'''
class login_thread(QObject):
    result = pyqtSignal(bool)

    '''
        O código abaixo é temporário 
        será subistituido pelo socket para conexão com o banco
    '''
    @pyqtSlot()
    def test(self) -> None:
        for i in range(100):
            print("Thread rodando")
        time.sleep(3)
        self.result.emit(True) 






def start():
    app = QApplication(sys.argv)
    login = login_window()
    login.show()
    sys.exit(app.exec_())
    


