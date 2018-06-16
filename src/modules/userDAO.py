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
		return self.conn.query(query,query_data=(user_id,))[0]

	def select_by_nickname(self,nickname):
		query = "SELECT * FROM chat_user WHERE nickname = %s"
		return self.conn.query(query,query_data=(nickname,))[0]

