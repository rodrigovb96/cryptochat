from message import Message
from user import ChatUser

u = ChatUser('eduardo','123')


m = Message(u,'voce','10/10/2010',_text = 'mensagem massa')

senha = b'Sixteen byte key'

json = m.get_string(senha)

print(json)
