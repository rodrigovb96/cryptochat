from modules.message import Message
from modules.user import ChatUser
import pickle
u = ChatUser('eduardo','123')


m = Message(u,'voce','10/10/2010',_text='mensagem massa')

senha = b'Sixteen byte key'

sdata = m.get_string(senha)


print(len(sdata))

data = pickle.loads(sdata)

