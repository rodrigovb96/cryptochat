from modules.crypto import CryptoEngine
from modules.user import ChatUser
import pickle

class Message(object):
	
	def __init__(self,sender,receiver,date,text=None,AES_info = None):
		
		if(text == None and AES_info != None):
			self._text = None
			self._AES_info = AES_info
		elif(AES_info == None and text != None):
			self._AES_info = None
			self._text = text
		else:
			raise Exception("Error to construct message")

		self._sender = sender
		self._receiver = receiver
		self._date = date	


	def set_text(self,text):
		self._text = text
	
	def get_text(self):
		return self._text
	
	def set_sender(self,sender):
		self._sender = sender
	
	def get_sender(self):
		return self._sender
	
	def set_receiver(self,receiver):
		self._receiver = receiver
	
	def get_receiver(self):
		return self._receiver
	
	def set_date(self,date):
		self._date = date
	
	def get_date(self):
		return self._date

	def get_string(self,AES_key):
		self.encrypt(AES_key)
		data = [self._AES_info,self._sender.get_username(),self._receiver,self._date]
#		string = r'{{"cipher":{AES_info[0]},"AEStag":{AES_info[1]},"msgNonce":{AES_info[2]},"signature":{AES_info[3]},"sender":{sender_},"receiver":{receiver_},"date":{date_}}}'.format(AES_info=self._AES_info,sender_=self._sender.get_username(),receiver_=self._receiver,date_=self._date)	
		string = pickle.dumps(data)
		return string
	
	def encrypt(self,AES_key):
		if (len(AES_key) not in [16,24,32]):
			raise Exception('Key must be 16, 24 or 32 bytes long')

		encryptor = CryptoEngine()
		encryptor.init_AES_mode()
		
		rsa_privateKey = self._sender.get_user_privateKey()

		_AES_info = encryptor.encrypt_AES_string(self._text,AES_key,rsa_privateKey)
		
		self._AES_info = _AES_info

	def decrypt(self,AES_key,RSA_public_key):
		if (len(AES_key) not in [16,24,32]):
			raise Exception('Key must be 16, 24 or 32 bytes long')
		
		decryptor = CryptoEngine()
		decryptor.init_AES_mode()

		self._text = decryptor.decrypt_AES_string(self._AES_info,AES_key,RSA_public_key)

		

