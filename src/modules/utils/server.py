import socket,sys,pickle
from threading import Thread

def process_input(input_string):  
	processed_data = pickle.loads(input_string)
    return processed_data

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):

    # the input is in bytes, so decode it
    input_from_client = conn.recv(MAX_BUFFER_SIZE)

    # MAX_BUFFER_SIZE is how big the message can be
    # this is test if it's sufficiently big
    siz = sys.getsizeof(input_from_client_bytes)
    if  siz >= MAX_BUFFER_SIZE:g
        print('The length of input is probably too long: {}'.format(siz))

    # decode input and strip the end of line
    #input_from_client = input_from_client_bytes.decode('utf8').rstrip()

    res = process_data(input_from_client)
    print(res)

    #vysl = res.encode('utf8')  # encode the result string
    conn.sendall('True')  # send it to client
    conn.close()  # close connection
    print('Connection ' + ip + ':' + port + ' ended')

def start_server():
    conn.sendall("pika".encode("utf8"))
    ack = None
    
    while(ack != "ack"):
    	data = conn.recv(MAX_BUFFER_SIZE)
    	ack = data.decode('utf8').rstrip()
    	print('Esperando ACK')
    
    print('publickey enviada com sucesso!')

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind(('192.168.100.55', 12345))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    # for handling task in separate jobs we need threading

    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print('Terible error!')
            import traceback
            traceback.print_exc()
    soc.close()

start_server()  
