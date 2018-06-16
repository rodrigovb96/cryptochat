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
		
	def commit(self):
		try:
			self.conn.commit()
		except pg.Error as e:
			print(e)

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
