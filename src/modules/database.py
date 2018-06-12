import psycopg2 as pg

class CryptoDatabase:
	
	def __init__(self):
		try:
			self.conn = pg.connect(dbname="cryptochat",user="postgres",password="1234")	
			self.cur = self.conn.cursor()
		except pg.Error as e:
			print(e)
	
	def close_conn(self):
		self.cur.close()
		self.conn.close()
		
	def insert_user(self,user_data : tuple):
		#tupla tem que ter nickname,pass_hash,salt,public_key
		query = "INSERT INTO chat_user (nickname,pass_hash,salt,public_key,is_active) VALUES (%s,%s,%s,%s,%s)"
		try:
			self.cur.execute(query,user_data)
		except pg.Error as e:
			print(e)

	def commit(self):
		self.conn.commit()

	def execute(self,query,query_data):
		try:
			self.cur.execute(query,query_data)
		except pg.Error as e:
			print(e)

	def query(self,query,query_data=None):
		try:
			self.cur.execute(query,query_data)
			return self.cur.fetchall()
		except pg.Error as e:
			print(e)
