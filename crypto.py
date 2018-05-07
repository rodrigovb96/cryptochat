from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP,AES
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

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


	def init_RSA_mode(self,key=None,key_size=2048):
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

	def init_AES_mode(self):
		self.__set_AES_ready(True)

	def encrypt_AES_string(self,raw_str,AES_key,RSA_private_key):
		if(not self.__AES_ready):
			raise Exception('AES state not set')
			
		nonce = get_random_bytes(16)
		cipher = AES.new(AES_key,AES.MODE_EAX,nonce=nonce)
		ciphertext, tag = cipher.encrypt_and_digest(bytearray(raw_str,'utf-8'))
		
		signer = CryptoEngine()
		signer.init_SIG_mode(RSA_private_key)
		signature = signer.sign_string(tag)

		return (ciphertext,tag,nonce,signature)
	
	def decrypt_AES_string(self,AES_info,AES_key,RSA_public_key):
		if (not self.__AES_ready):
			raise Exception('AES state not set')

		ciphertext,tag,nonce,signature = AES_info
		cipher = AES.new(AES_key,AES.MODE_EAX,nonce=nonce)
		
		signer = CryptoEngine()
		signer.init_SIG_mode(RSA_public_key)
		
		if(signer.verify_sign(tag,signature)):
			try:
				plaintext = cipher.decrypt_and_verify(ciphertext,tag)
			except ValueError:
				raise Exception('Corrupted message')
			
			return plaintext.decode()
		else:
			raise Exception('Message not authentic')
	
	def init_SIG_mode(self,RSA_key=None):
		self.init_RSA_mode(key=RSA_key)
	
	def sign_string(self,unsigned_str):
		
		private_key = self.generate_RSA_keypair()[0]
		str_hash = SHA256.new(unsigned_str)
		signature = pkcs1_15.new(self.RSA_key_obj).sign(str_hash)

		return signature

	def verify_sign(self,unsigned_str,signature):
		public_key = self.generate_RSA_keypair()[1]
		str_hash = SHA256.new(unsigned_str)
		try:
			pkcs1_15.new(self.RSA_key_obj).verify(str_hash,signature)
			return True
		except (ValueError):
			return False




