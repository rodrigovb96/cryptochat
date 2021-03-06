from modules.database import CryptoDatabase

class UserDAO:
	
	def __init__(self):
		self.conn = CryptoDatabase()
	
	def insert(self,user_data:tuple):
		query = "INSERT INTO chat_user (nickname,pass_hash,salt,public_key,is_active) VALUES (%s,%s,%s,%s,%s)"
		self.conn.execute(query,query_data=user_data)
		result = self.conn.query("SELECT * FROM chat_user WHERE nickname = %s",(user_data[0],))
		self.conn.commit()
		return len(result)
	
	def update(self,new_data:tuple):
		#tupla tem que ser (nick,hash,salt,public,active,nick)
		query = "UPDATE chat_user SET nickname = %s, pass_hash = %s, salt = %s, public_key = %s, is_active = %s WHERE nickname = %s"
		self.conn.execute(query,query_data=new_data)
		result = self.conn.query("SELECT * FROM chat_user WHERE nickname = %s and pass_hash = %s and salt = %s and public_key = %s and is_active = %s",tuple([x for x in new_data][:-1]))
		self.conn.commit()
		return len(result)

	def delete(self,user_id):
		query = "DELETE FROM chat_user WHERE user_id = %s"
		self.conn.execute(query,(user_id,))
		self.conn.commit()

	def select_by_id(self,user_id):
		query = "SELECT * FROM chat_user WHERE user_id = %s"
		res = self.conn.query(query,query_data=(user_id,))
		if(len(res) > 0):
			return res[0]
		else:
			return None

	def try_to_login(self,nickname,password,publickey):
		from modules.crypto import CryptoEngine		
		salt_pos = 3
		hash_pos = 2

		nick = nickname.decode("utf8")

		select_result = self.select_by_nickname(nickname=nick)
		engine = CryptoEngine()
		engine.init_HASH_mode()	
		
		if select_result == None:

			from Crypto.Random import get_random_bytes	
			salt = get_random_bytes(16)
			password_salt = password + salt
			hash_pass = engine.hash_byte_string(password_salt)
			self.insert(user_data=(nick,hash_pass,salt,publickey,'0'))
			
			return True	
		else:

			password_salt = password + bytes(select_result[salt_pos])

			password_hash = engine.hash_byte_string(password_salt)

			if password_hash == select_result[hash_pos].tobytes(): 
				self.update((nick,password_hash,select_result[salt_pos].tobytes(),publickey,'1',nick))
				print("Usuario cadastrado: Login com sucesso!")
				return True
			else:
				print("Usuario cadastrado: Login sem sucesso!")
				return False
				

	
	def select_by_nickname(self,nickname:str):
		query = "SELECT * FROM chat_user WHERE nickname = %s"
		res = self.conn.query(query,query_data=(nickname,))
		if(len(res) > 0):
			return res[0]
		else:
			return None

