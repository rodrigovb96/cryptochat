from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from chat_gui import chat_window
import os,sys


sys.path.insert(0,'..')

import user

class login_window(QWidget):

    
    def __init__(self, parent=None):
        super(login_window,self).__init__()
        self.setWindowTitle("Login")

        self.setFixedSize(200,200)
        self.init_components()

    
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
                self.close()
                self.second = chat_window(username=self.name_text.text())
                self.second.show()


        else:
            QMessageBox.warning(self,"Erro!","Valores Informados Inválidos", QMessageBox.Ok)
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = login_window()
    login.show()
    sys.exit(app.exec_())
