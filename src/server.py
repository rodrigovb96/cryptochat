import socket,sys,pickle
from threading import Thread
from modules.crypto import CryptoEngine
from modules.userDAO import UserDAO
from modules.user_relationDAO import UserRelationDAO
from modules.conversationDAO import ConversationDAO
from modules.key_setDAO import KeySetDAO
from modules.messageDAO import MessageDAO
	

import time
import datetime 

LOG = print

def rec_data(conn,MAX_BUFFER_SIZE):
    

    try:
        input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)
    except:
        print("nao deu")
        



    siz = sys.getsizeof(input_from_client_bytes)

    if siz >= MAX_BUFFER_SIZE:
        print("Input Maior que o permitido")


    input_from_client = input_from_client_bytes.decode("utf8")


    return input_from_client

def process_input(input_string):  
    processed_data = pickle.loads(input_string)
    return processed_data

def login_handler(conn, ip, port, MAX_BUFFER_SIZE = 4096):

    key = CryptoEngine()
    key.init_RSA_mode()

    private_key,public_key = key.generate_RSA_keypair()

    conn.sendall(public_key) # public_key do servidor

    LOG('Requisição de login!\n')
    
    LOG('publickey enviada com sucesso!') 

    input_from_client = conn.recv(MAX_BUFFER_SIZE)

    siz = sys.getsizeof(input_from_client)
    if  siz >= MAX_BUFFER_SIZE:
        print('The length of input is probably too long: {}'.format(siz))

    res = process_input(input_from_client)

    user = key.decrypt_RSA_string(cipher_str=res["user"])
    password = key.decrypt_RSA_string(cipher_str=res["password"])
    pb_key = res["publickey"] 


	
    user_db = UserDAO()
	
    if user_db.try_to_login(nickname=user,password=password,publickey=pb_key):
        conn.sendall('True'.encode("utf8"))  # send it to client
        conn.sendall(pb_key)
    else:
        conn.sendall('False'.encode("utf8"))  # send it to client
		


	




def receive_msg_handler(conn,MAX_BUFFER_SIZE = 4096):

	sender_receiver = process_input(conn.recv(MAX_BUFFER_SIZE))
		
	user_db = UserDAO()
	conv_db = ConversationDAO()
	key_set_db = KeySetDAO()
	message_db = MessageDAO()
	
	

	user_ids = []
	
	res = user_db.select_by_nickname(sender_receiver["sender"])
	
	if res is not None:
		user_ids.append(res[0])
		print(user_ids)
				
		res = user_db.select_by_nickname(sender_receiver["receiver"])

		if res is not None:
			user_ids.append(res[0])
		
			res = conv_db.select_by_users(user_ids)

			if res is not None:

				conv_id = res[0]
				AES = key_set_db.select_by_owner_conversation((user_ids[0],conv_id))[2]
				
				conn.sendall("--OKTOSEND--".encode("utf8"))	
				conn.sendall(bytes(AES))

				msg = process_input(conn.recv(MAX_BUFFER_SIZE))
				date = msg[3]
				exp_date = date + datetime.timedelta(days=2)
				msg_info = (msg[0],date,exp_date,user_ids[1],'0',conv_id)
				if message_db.insert(msg_info) is 1:
					conn.sendall("--OK--".encode("utf8"))

			else:
				conn.sendall("--NOCONV--".encode("utf8"))	
				AES_USER_FRIEND = process_input(conn.recv(MAX_BUFFER_SIZE))
				
				res = conv_db.insert(user_ids)

				if res is 1:
					conv_id = conv_db.select_by_users(user_ids)[0]
					res = key_set_db.insert((user_ids[0],AES_USER_FRIEND["AES_USER"],user_ids[1],AES_USER_FRIEND["AES_FRIEND"],conv_id))
					if res is 2:
						conn.sendall("--OKTOSEND--".encode("utf8"))

						msg = process_input(conn.recv(MAX_BUFFER_SIZE))
						date = msg[3]
						exp_date = date + datetime.timedelta(days=2)
						msg_info = (msg[0],date,exp_date,user_ids[1],'0',conv_id)
						if message_db.insert(msg_info) is 1:
							conn.sendall("--OK--".encode("utf8"))
						
					

					
				

    


def send_msg_handler(conn,MAX_BUFFER_SIZE = 4096):


    input_from_client = conn.recv(MAX_BUFFER_SIZE)

    sender_receiver = process_input(input_from_client)

    msg_db = MessageDAO()
    conv_db = ConversationDAO()
    key_set_db = KeySetDAO()
    user_db = UserDAO()

    user_ids = []
	
    res = user_db.select_by_nickname(sender_receiver["sender"])
	
    if res is not None:
        user_ids.append(res[0])
        print(user_ids)
				
        res = user_db.select_by_nickname(sender_receiver["receiver"])

        if res is not None:
            user_ids.append(res[0])
		
            res = conv_db.select_by_users(user_ids)

            if res is not None:

                conv_id = res[0]
                AES = key_set_db.select_by_owner_conversation((user_ids[1],conv_id))[2]
                conn.sendall(bytes(AES))

    temp_msg_list = msg_db.fetch_unread_messages_by_users(sender_receiver["receiver"],sender_receiver["sender"])
	
	
    messages_list = []
    for msg in temp_msg_list:
       messages_list.append( (msg[0],bytes(msg[1]),msg[2],msg[3],msg[4],msg[5],msg[6]) )
		
		

    conn.sendall(pickle.dumps(messages_list))
	
    if "--ALLREAD--" in conn.recv(MAX_BUFFER_SIZE).decode("utf8"):
        for msg in temp_msg_list:
           msg_db.update(msg[0])

	

def search_friend_handler(conn,MAX_BUFFER_SIZE = 4096):
	
	search = conn.recv(MAX_BUFFER_SIZE)
	user_friend = process_input(search)


	request = UserRelationDAO().invite_friend(user_friend["username"].decode("utf8"),user_friend["friend"].decode("utf8"))

	
	if request == False:
		pass
	else:
		result_request = (request[0],request[1],bytes(request[2]))	
		conn.send(pickle.dumps(result_request))
	
		

def search_all_friends(conn):
	
	
	LOG('REQ: Buscando todos os amigos!')

	user_nick_bytes = conn.recv(4096)
	user_nick = user_nick_bytes.decode("utf8")
	
	request = UserRelationDAO().select_friends_of_user(user_nick)


	if request == False:
		pass
	else:

		result = []
		for value in request:
			result.append( (value[0],value[1],bytes(value[2])))	

		import struct 

		packet = pickle.dumps(result)
		length = struct.pack('!I',len(packet))
		packet = length + packet
		
		conn.sendall(packet)

	


def client_handler(conn,ip,port,MAX_BUFFER_SIZE=4096):

    operation_request = conn.recv(MAX_BUFFER_SIZE).decode("utf8")

    if "--LOGINREQ--" in operation_request:
        login_handler(conn,ip,port)
    elif "--FRIENDSREQ--" in operation_request:
        friends_list_handler()
    elif "--SMSGREQ--" in operation_request:
        receive_msg_handler(conn) 
    elif "--RMSGREQ--" in operation_request:
        send_msg_handler(conn)
    elif "--SEARCHREQ--" in operation_request:
        search_friend_handler(conn)
    elif "--SEARCHALL--" in operation_request:
        search_all_friends(conn)


    conn.close() 
    LOG('Connection ' + ip + ':' + port + ' ended')






def start_server():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    LOG('Socket created')

    ip_serv = ''
    with open('ip.txt','r') as f:	
        ip_serv = f.read()
		
    try:
        soc.bind((ip_serv, 12345))
        LOG('Socket bind complete')
    except socket.error as msg:
        LOG('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    LOG('Socket now listening')


    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        LOG('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_handler, args=(conn, ip, port)).start()
        except:
            print('Terible error!')
            import traceback
            traceback.print_exc()

    soc.close()


start_server()  
