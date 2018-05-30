import socket,sys,pickle
from threading import Thread
from modules.crypto import CryptoEngine

LOG = print

def process_input(input_string):  
    processed_data = pickle.loads(input_string)
    return processed_data

def chat_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):

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

def start_server():


    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    LOG('Socket created')

    try:
        soc.bind(('192.168.100.47', 12345))
        LOG('Socket bind complete')
    except socket.error as msg:
        LOG('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    LOG('Socket now listening')

    # for handling task in separate jobs we need threading

    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        LOG('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=chat_thread, args=(conn, ip, port)).start()
        except:
            print('Terible error!')
            import traceback
            traceback.print_exc()
    soc.close()

start_server()  
