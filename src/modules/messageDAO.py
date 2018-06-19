from modules.database import CryptoDatabase
from modules.userDAO import UserDAO

class MessageDAO:
	
	def __init__(self):
		self.conn = CryptoDatabase()
	
	def insert(self,message_data:tuple):
		query = "INSERT INTO message (message_data,date_sent,exp_date,receiving_user,was_received,conversation_id) VALUES (%s,%s,%s,%s,%s,%s)"
		self.conn.execute(query,query_data=message_data)
		result = self.conn.query("SELECT * FROM message WHERE message_data = %s AND date_sent = %s AND exp_date = %s AND receiving_user = %s AND was_received = %s AND conversation_id = %s",message_data)
		self.conn.commit()
		return len(result)

	def update(self,message_id):
		query = "UPDATE message SET was_received = %s WHERE message_id = %s"
		self.conn.execute(query,query_data=('1',message_id))
		result = self.conn.query("SELECT * FROM message WHERE was_received = %s AND message_id = %s",('1',message_id))
		self.conn.commit()
		return len(result)

	def delete(self,message_id):
		query = "DELETE FROM message WHERE message_id = %s"
		self.conn.execute(query,(message_id,))
		self.conn.commit()

	def select_by_id(self,message_id):
		query = "SELECT * FROM message WHERE message_id = %s"
		res = self.conn.query(query,query_data=(message_id,))
		if(len(res) > 0):
			return res[0]
		else:
			return None

	def check_unread_messages_by_user(self,user_id):
		query = "SELECT user_one FROM conversation WHERE user_two = %s AND conversation_id IN (SELECT conversation_id FROM message WHERE receiving_user = %s AND was_received = '0') UNION SELECT user_two FROM conversation WHERE user_one = %s AND conversation_id IN (SELECT conversation_id FROM message WHERE receiving_user = %s AND was_received = '0')"
		data = tuple([user_id]*4)
		return self.conn.query(query,query_data=data)

	def fetch_unread_messages_by_users(self,receiving_user,other_user):
		uDAO = UserDAO()
		users_ids = []
		
		res = uDAO.select_by_nickname(other_user)
		if(res != None):
			users_ids.append(res[0])
		else:
			return False

		res = uDAO.select_by_nickname(receiving_user)
		if(res != None):
			users_ids.append(res[0])
		else:
			return False

		query = "SELECT * FROM message WHERE conversation_id IN (SELECT conversation_id FROM conversation WHERE user_one = %s AND user_two = %s) AND was_received = '0' AND receiving_user = %s"
		data = tuple(sorted([users_ids[0],users_ids[1]])+[users_ids[1]])
		return self.conn.query(query,query_data=data)

	

