from modules.database import CryptoDatabase

class ConversationDAO:
	
	def __init__(self):
		self.conn = CryptoDatabase()
	
	def insert(self,conversation_data:tuple):
		query = "INSERT INTO conversation (user_one,user_two) VALUES (%s,%s)"
		data = tuple(sorted([conversation_data[0],conversation_data[1]]))
		self.conn.execute(query,query_data=data)
		result = self.conn.query("SELECT * FROM conversation WHERE user_one = %s AND user_two = %s",(data[0],data[1]))
		self.conn.commit()
		return len(result)

	def delete(self,users:tuple):
		query = "DELETE FROM conversation WHERE user_one = %s AND user_two = %s"
		data = tuple(sorted(users[0],users[1]))
		self.conn.execute(query,data)
		self.conn.commit()

	def select_by_users(self,users):
		query = "SELECT * FROM conversation WHERE user_one = %s AND user_two = %s"
		data = tuple(sorted([users[0],users[1]]))
		res = self.conn.query(query,query_data=data)
		if(len(res) > 0):
			return res[0]
		else:
			return None

	def select_by_single_user(self,user_id):
		query = "SELECT * FROM conversation WHERE user_one = %s OR user_two = %s"
		return self.conn.query(query,query_data=(user_id,user_id))

