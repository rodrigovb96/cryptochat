from modules.message import Message
from modules.user import ChatUser
import pickle
u = ChatUser('eduardo','123')


m = Message(sender = u,receiver = 'voce',date = '10/10/2010',text='mensagem massa')

senha = b'Sixteen byte key'

data_sent = m.get_string(senha)
#transferencia
data_received = pickle.loads(data_sent)

_AES_info,_sender,_receiver,_date = data_received

n = Message(_sender,_receiver,_date,AES_info = _AES_info)

n.decrypt(senha,u.get_user_publicKey())

print(n.get_text())
