from crypto import CryptoEngine
from user import ChatUser

class Message(object):
	
	def __init__(self,_sender : ChatUser,_receiver : str,_date : str,_text = None : str):
		self.text = _text
		self.sender = _sender
		self.receiver = _receiver
		self.date = _date
		self.AES_info = None

	def set_text(self,_text):
		self.text = _text
	
	def get_text(self):
		return self.text
	
	def set_sender(self,_sender):
		self.sender = _sender
	
	def get_sender(self):
		return self.sender
	
	def set_receiver(self,_receiver):
		self.receiver = _receiver
	
	def get_receiver(self):
		return self.receiver
	
	def set_date(self,_date):
		self.date = _date
	
	def get_date(self):
		return self.date

	def get_string(self):
		self.encrypt()
		string = '{"cipher":{AES_info[0]},"AEStag":{AES_info[1]},"msgNonce":{AES_info[2]},"signature":{AES_info[3]},"sender":{sender_},"receiver":{receiver_},"date":{date_}}'.format(AES_info=self.AES_info,sender_=self.sender.get_username(),receiver_=self.receiver,date_=self.date)	
	
	def encrypt(self,AES_key):
		if (len(AES_key) not in [16,24,32]):
			raise Exception('Key must be 16, 24 or 32 bytes long')

		encryptor = ne()
		encryptor.init_AES_mode()
		
		rsa_privateKey = self.sender.get_user_privateKey()

		_AES_info = encryptor.encrypt_AES_string(self.text,AES_key,rsa_privateKey)
		
		self.AES_info = _AES_info


