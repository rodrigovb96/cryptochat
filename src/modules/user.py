import os,sys

import modules.utils.files as utils
from modules.crypto import CryptoEngine


class ChatUser(object):
	
	def __init__(self,username,password):
		self.username = username
		self.__password = password
		self.rsaKey = None

		self.set_rsaKey()


	def get_username(self):
		return self.username
	def get_password(self):
		return self.__password

	def set_rsaKey(self):
		h = CryptoEngine()
		h.init_HASH_mode()
		user_hash = h.hash_string(self.username)
		
		filename = os.path.expanduser('~/cryptochat/user_data/') + user_hash + '/private_key'

		file_data = utils.read_file(filename)

		key = CryptoEngine()

		if(file_data == False):
			key.init_RSA_mode() 
			self.rsaKey = key
			privatekey,_ = self.rsaKey.generate_RSA_keypair(_passphrase=self.__password)
			
			utils.create_file(filename,privatekey.decode('utf-8'))
		else:
			try:
				key.init_RSA_mode(key=file_data,_passphrase=self.__password)
			except ValueError as e:
                                raise e 

			self.rsaKey = key

	def get_user_publicKey(self):
		if(self.rsaKey != None):
			publickey = self.rsaKey.generate_RSA_keypair(_passphrase = self.__password)[1]
			return publickey
		else:
			raise Exception('RSA key not set')

	def get_user_privateKey(self):
		if(self.rsaKey != None):
			privatekey = self.rsaKey.generate_RSA_keypair(_passphrase = self.__password)[0]
			return privatekey
		else:
			raise Exception('RSA key not set')

