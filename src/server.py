import socket,sys,pickle
from threading import Thread
from modules.crypto import CryptoEngine

LOG = print

def rec_data(conn,MAX_BUFFER_SIZE):
    
    LOG("AGUARDANDO DADOS")

    try:
        input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)
    except:
        print("FUDEU")
        

    LOG("PASSOU DAQUI PQ? N SEI")


    siz = sys.getsizeof(input_from_client_bytes)

    if siz >= MAX_BUFFER_SIZE:
        print("Input Maior que o permitido")


    input_from_client = input_from_client_bytes.decode("utf8")


    return input_from_client

def process_input(input_string):  
    processed_data = pickle.loads(input_string)
    return processed_data

def login_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):

    key = CryptoEngine()
    key.init_RSA_mode()

    private_key,public_key = key.generate_RSA_keypair()

    conn.sendall(public_key) # public_key do servidor
    
    LOG('publickey enviada com sucesso!') 

    # the input is in bytes, so decode it
    input_from_client = conn.recv(MAX_BUFFER_SIZE)

    # MAX_BUFFER_SIZE is how big the message can be
    # this is test if it's sufficiently big
    siz = sys.getsizeof(input_from_client)
    if  siz >= MAX_BUFFER_SIZE:
        print('The length of input is probably too long: {}'.format(siz))

    res = process_input(input_from_client)
    LOG(res)

    user = key.decrypt_RSA_string(cipher_str=res["user"])
    password = key.decrypt_RSA_string(cipher_str=res["password"])

    LOG(user)
    LOG(password)

    '''
        Verificar o usuário e a senha no banco
    '''
    conn.sendall('True'.encode("utf8"))  # send it to client

    conn.close()  # close connection
    LOG('Connection ' + ip + ':' + port + ' ended')

    LOG("ENTRANDO NA THREAD DE CHAT")
    chat_thread(conn,ip,port)



def friends_thread():
    '''
        Verifica lista de amigos no banco
            - Manda os amigos do banco para o servidor
    '''
    pass
    

def chat_thread(conn,ip,port,MAX_BUFFER_SIZE = 4096):

    while True:
        conn_check, addr = soc.acept()
    still_listen = True

    while still_listen:
        LOG("NA THREAD CHAT")

        
        input_from_client = rec_data(conn,MAX_BUFFER_SIZE)


        
        LOG("PASSOU PQ?")

        if "--ENDOFDATA--" in input_from_client:

            print("--ENDOFDATA--")

            conn.close()
            print("Connection " + ip + ":" + port + "ended")

            still_listen = False

        else:

            print(input_from_client)

            conn.sendall("--OKTOSEND--".encode("utf8"))
            






def start_server():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    LOG('Socket created')

    try:
        soc.bind(('127.0.0.1', 12345))
        LOG('Socket bind complete')
    except socket.error as msg:
        LOG('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    LOG('Socket now listening')

    ips = []

    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        if ip not in ips:
            LOG('Accepting connection from ' + ip + ':' + port)
            ips.append(ip)
            try:
                Thread(target=login_thread, args=(conn, ip, port)).start()
            except:
                print('Terible error!')
                import traceback
                traceback.print_exc()
        else:
            pass
    soc.close()


start_server()  
