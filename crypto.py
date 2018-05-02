from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class CryptoEngine(object):
	

	def __init__(self):
		self.__RSA_ready = False
		self.__AES_ready = False

	def is_RSA_ready(self):
		return self.__RSA_ready

	def is_AES_ready(self):
		return self.__AES_ready

	def __set_RSA_ready(self,state):
		if(self.__AES_ready):
			raise Exception('Error setting RSA state')
		else:	
			self.__RSA_ready = state

	def __set_AES_ready(self,state):
		if(self.__RSA_ready):
			raise Exception('Error setting AES state')
		else:
			self.__AES_ready = state


	def init_RSA(self,key=None,key_size=2048):
		if (key != None):
			self.RSA_key_obj = RSA.import_key(key)
		else:
			self.RSA_key_obj = RSA.generate(key_size)

		self.__set_RSA_ready(True) 

	def generate_RSA_keypair(self):
		if (not self.__RSA_ready):
			raise Exception('RSA state not set')
			
		private_key_obj = self.RSA_key_obj
		public_key_obj = private_key_obj.publickey()

		private_key = private_key_obj.export_key()
		public_key = public_key_obj.export_key()

		return (private_key,public_key)
	
	def encrypt_RSA_string(self,raw_str,key=None):
		if (not self.__RSA_ready):
			raise Exception('RSA state not set')

		if key == None:
			key_obj = self.RSA_key_obj
		else:
			key_obj = RSA.import_key(key)

		if not key_obj.has_private():
			cipher = PKCS1_OAEP.new(key_obj)
			cipher_str = cipher.encrypt(raw_str)
			return cipher_str
		else:
			raise Exception('Trying to encrypt with a private key')
	
	def decrypt_RSA_string(self,cipher_str,key=None):
		if (not self.__RSA_ready):
			raise Exception('RSA state not set')

		if key == None:
			key_obj = self.RSA_key_obj
		else:
			key_obj = RSA.import_key(key)

		if key_obj.has_private():
			cipher = PKCS1_OAEP.new(key_obj)
			raw_str = cipher.decrypt(cipher_str)
			return raw_str
		else:
			raise Exception('Trying to decrypt with a public key')

	def init_AES(self):
		self.__set_AES_ready(True)

	def encrypt_AES_string(self,raw_str,key):
		if(not self.__AES_ready):
			raise Exception('AES state not set')
			
		nonce = get_random_bytes(16)
		cipher = AES.new(key,AES.MODE_EAX,nonce=nonce)
		ciphertext, tag = cipher.encrypt_and_digest(bytearray(raw_str,'utf-8'))
		
		return (ciphertext,tag,nonce)
	
	def decrypt_AES_string(self,AES_info,key):
		if (not self.__AES_ready):
			raise Exception('AES state not set')

		ciphertext,tag,nonce = AES_info
		cipher = AES.new(key,AES.MODE_EAX,nonce=nonce)
		
		try:
			plaintext = cipher.decrypt_and_verify(ciphertext,tag)
		except ValueError:
			raise Exception('Corrupted message')
		
		return plaintext.decode()
	
