from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import sys


class login_window(QWidget):


	def __init__(self, parent=None):
		super(login_window,self).__init__()
		self.setWindowTitle("Login")

		self.setFixedSize(200,200)
		self.init_components()

	
	def init_components(self):
		
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
	
	@pyqtSlot()	
	def connect(self):
		"Verifica a Conexão com o banco"
		pass
	


if __name__ == '__main__':
	app = QApplication(sys.argv)
	login = login_window()
	login.show()
	sys.exit(app.exec_())
