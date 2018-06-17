import socket,sys,pickle
from threading import Thread
from modules.crypto import CryptoEngine
from modules.userDAO import UserDAO
from modules.user_relationDAO import UserRelationDAO
import time

LOG = print

def rec_data(conn,MAX_BUFFER_SIZE):
    

    try:
        input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)
    except:
        print("FUDEU")
        



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
        print("FOI")
    else:
        conn.sendall('False'.encode("utf8"))  # send it to client
        print("NAO FOI")
		






def friends_thread():
    '''
        Verifica lista de amigos no banco
            - Manda os amigos do banco para o servidor
    '''
    pass
    

def receive_msg_handler(conn,MAX_BUFFER_SIZE = 4096):

    '''
        Verifica LOGIN TODO
        Recebe remetente e destinatário
    ''' 
    
    conn.sendall("--OKTOSEND--".encode("utf8"))

    input_from_client = conn.recv(MAX_BUFFER_SIZE)

    sender_receiver_msg = process_input(input_from_client)

    print(sender_receiver_msg["sender"])
    print(sender_receiver_msg["receiver"])
    print(sender_receiver_msg["msg"])



    conn.sendall("--OKTOSEND--".encode("utf8"))

def send_msg_handler(conn,MAX_BUFFER_SIZE = 4096):

    
    '''
        VERIFICA LOGIN 
    '''

    conn.sendall("--OKTOSEND--".encode("utf8"))

    input_from_client = conn.recv(MAX_BUFFER_SIZE)

    receiver_sender = process_input(input_from_client)

    conn.send("MESAGEM".encode("utf8")) # TODO


    while True:
        client_msg = conn.recv(MAX_BUFFER_SIZE).decode("utf8")

        print(client_msg)
        if "--OKTOSEND--" in client_msg:
            time.sleep(5)
            conn.send("MESAGEM".encode("utf8")) # TODO
        if "--ENDOFCHAT--" in client_msg:
            print("ACABOU CHAT")
            return


def search_friend_handler(conn,MAX_BUFFER_SIZE = 4096):
	
	search = conn.recv(MAX_BUFFER_SIZE)
	friend = process_input(search)

	request = U
	
		
	
	
	


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


    conn.close() 
    LOG('Connection ' + ip + ':' + port + ' ended')






def start_server():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    LOG('Socket created')

    try:
        soc.bind(('192.168.100.48', 12345))
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
