from modules.userDAO import UserDAO
from modules.messageDAO import MessageDAO
from modules.user_relationDAO import UserRelationDAO
from modules.conversationDAO import ConversationDAO
from modules.key_setDAO import KeySetDAO
from Crypto.Random import *
from Crypto.Random import random
import datetime

def insert_user(data):
	userD = UserDAO()
	username = data[0]
	res = userD.select_by_nickname(username)
	
	if(len(res) > 0):
		print("já possui cadastro")
		return res
	
	res = userD.insert(data)

def create_relation(data):
	relD = user_relationDAO()
	
	userD = UserDAO()
	users = tuple([userD.select_by_nickname(user)[0] for user in data])
	
	res = relD.select_by_users(users)

	if(res != None):
		print("já possui relação")
		return -1

	return relD.insert(tuple([users[0],users[1],'friends']))
	
def create_conversation(data):
	convD = ConversationDAO()
	
	userD = UserDAO()
	users = tuple([userD.select_by_nickname(user)[0] for user in data])
	
	res = convD.select_by_users(users)

	if(res != None):
		print("já possui conversa")
		return -1

	return convD.insert(users)

def create_keyset(data):
	keyD = KeySetDAO()
	
	userD = UserDAO()
	users = tuple([userD.select_by_nickname(data[i])[0] for i in range(0,4,2)])
	
	convD = ConversationDAO()
	conv = convD.select_by_users(users)

	for i in range(2):
		res = keyD.select_by_owner_conversation((users,conv))
		if(res != None):
			print("Algo deu errado no keyset")
			return -1

	return keyD.insert(tuple([d for d in data]+[conv]))

def send_message(data):
	


data = ('nick1',get_random_bytes(30),get_random_bytes(15),get_random_bytes(20),'0')

if(insert_user(data)):
	print('insert 1 ok')

data = ('nick2',get_random_bytes(30),get_random_bytes(15),get_random_bytes(20),'0')


if(insert_user(data)):
	print('insert 2 ok')

if(create_relation(('nick1','nick2')) == 1):
	print('relation ok')

if(create_conversation(('nick1','nick2') == 1):
	print('convesation ok')

key1 = 'asdfsaadsfad'.encode('utf-8')
key2 = 'dsfsdfsdfsdf'.encode('utf-8')

if(create_keyset(('nick1',key1,'nick2',key2)) == 1):
	print('key set ok')

today = datetime.date.today()
message = ('asdfasda'.enconde('utf-8'),today,today+datetime.timedelta(days=2),2,'0',1)

if(send_message(message)):
	print('message sent ok')

