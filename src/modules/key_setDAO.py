from modules.database import CryptoDatabase

class KeySetDAO:
	
	def __init__(self):
		self.conn = CryptoDatabase()
	
	def insert(self,key_set_data:tuple):
		#tupla tem que ser (usuario1,key_user1,usuario2,key_user2,conversation_id)
		query = "INSERT INTO key_set (private_owner,key,conversation_id) VALUES (%s,%s,%s)"
		rows = 0
		for i in range(0,3,2):
			data = tuple([key_set_data[0+i],key_set_data[1+i]]+[key_set_data[-1]])
			self.conn.execute(query,query_data=data)
			result = self.conn.query("SELECT * FROM key_set WHERE private_owner = %s and conversation_id = %s",(data[0],data[2]))
			rows += len(result)
		self.conn.commit()
		return rows
	
	def update(self,new_data:tuple):
		#tupla tem que ser (usuario1,key_user1,usuario2,key_user2,conversation_id)
		rows = 0
		for i in range(2):
			query = "UPDATE key_set SET key = %s WHERE private_owner = %s AND conversation_id = %s"
			data = tuple([new_data[1+i],new_data[0+i],new_data[-1]])
			self.conn.execute(query,query_data=data)
			result = self.conn.query("SELECT * FROM key_set WHERE private_owner = %s AND conversation_id = %s",(data[1],data[2]))
			rows += len(result)
		self.conn.commit()
		return rows

	def delete(self,conversation_id):
		query = "DELETE FROM key_set WHERE conversation_id = %s"
		self.conn.execute(query,(conversation_id,))
		self.conn.commit()

	def select_by_owner_conversation(self,data):
		query = "SELECT * FROM key_set WHERE private_owner = %s AND conversation_id = %s"
		res = self.conn.query(query,query_data=data)
		if(len(res) > 0):
			return res[0]
		else:
			return None

