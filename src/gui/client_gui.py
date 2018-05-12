from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import sys


class chat_window(QWidget):

    def __init__(self, parent=None):
        super(chat_window, self).__init__()
        self.setWindowTitle("Cliente")


        self.setFixedSize(640,480)
        self.init_components()

    def init_components(self):

        self.chat_text = QTextEdit()
        self.input_text = QTextEdit()

        self.send_btn = QPushButton("Enviar",self)
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


    @pyqtSlot()
    def send_msg(self):
       self.chat_text.append(self.input_text.toPlainText())
       self.input_text.clear()

    @pyqtSlot()
    def clear_msg(self):
       self.input_text.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = chat_window()
    client.show()
    sys.exit(app.exec_())
