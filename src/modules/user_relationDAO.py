from modules.database import CryptoDatabase
from modules.userDAO import UserDAO

class UserRelationDAO:
	
	def __init__(self):
		self.conn = CryptoDatabase()
	
	def insert(self,userR_data:tuple):
		query = "INSERT INTO user_relation (first_user,second_user,relation_type) VALUES (%s,%s,%s)"
		data = tuple(sorted([userR_data[0],userR_data[1]])+[userR_data[2]])
		self.conn.execute(query,query_data=data)
		result = self.conn.query("SELECT * FROM user_relation WHERE first_user = %s AND second_user = %s",(data[0],data[1]))
		self.conn.commit()
		return len(result)
	
	def update(self,new_data:tuple):
		query = "UPDATE chat_user SET relation_type = %s WHERE first_user = %s AND second_user = %s"
		data = tuple([userR_data[2]]+sorted([new_data[0],new_data[1]]))
		self.conn.execute(query,query_data=data)
		result = self.conn.query("SELECT * FROM user_relation WHERE first_user = %s AND second_user = %s AND relation_type = %s",tuple([data[1],data[2],data[0]]))
		self.conn.commit()
		return len(result)

	def delete(self,users:tuple):
		query = "DELETE FROM user_relation WHERE first_user = %s AND second_user = %s"
		data = tuple(sorted(users[0],users[1]))
		self.conn.execute(query,data)
		self.conn.commit()

	def select_by_users(self,users):
		query = "SELECT * FROM user_relation WHERE first_user = %s AND second_user = %s"
		data = tuple(sorted([users[0],users[1]]))
		res = self.conn.query(query,query_data=data)
		if(len(res) > 0):
			return res[0]
		else:
			return None

	def select_by_single_user(self,user_id):
		query = "SELECT * FROM user_relation WHERE first_user = %s OR second_user = %s"
		return self.conn.query(query,query_data=tuple([user_id]*2))

	def select_relation_of_users(self,users):
		query = "SELECT relation_type FROM user_relation WHERE first_user = %s AND second_user = %s"
		data = tuple(sorted([users[0],users[1]]))
		return self.conn.query(query,query_data=data)

	def select_friends_of_user(self,nickname):
		uDAO = UserDAO()

		current_user = uDAO.select_by_nickname(nickname)

		if(len(current_user) < 1):
			return False

		query = "SELECT user_id, nickname, public_key FROM chat_user WHERE user_id IN (SELECT first_user FROM user_relation WHERE second_user = %s AND relation_type = 'friends' UNION SELECT second_user FROM user_relation WHERE first_user = %s AND relation_type = 'friends')"
		return self.conn.query(query,query_data=tuple([current_user[0]]*2))

	def invite_friend(self,nickname,friend_nickname):
		uDAO = UserDAO()

		friend_found = uDAO.select_by_nickname(friend_nickname)
		current_user = uDAO.select_by_nickname(nickname)
		
		relation_exists = self.select_relation_of_users((friend_found[0],current_user[0]))
		
		if(len(relation_exists) > 0):
			return False

		if(friend_found != None and current_user != None):
			res = self.insert((friend_found[0],current_user[0],'friends'))
			if(res == 1):
				return (friend_found[0],friend_found[1],friend_found[4])
			else:
				return False
		else:
			return False






