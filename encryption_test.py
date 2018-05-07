from crypto import CryptoEngine
#Cria um objeto CryptoEngine e inicia em modo RSA
RSA_section = CryptoEngine()
RSA_section.init_RSA_mode()
#É possivel passar uma chave tanto publica quanto privada para inicializar o objeto RSA, se não for passado nada é gerado keys novas

#Retorna a keypair do objeto gerado, caso o objeto seja iniciado com uma chave publica as duas chaves retornadas serão iguais
RSA_private,RSA_public = RSA_section.generate_RSA_keypair()

print(RSA_private)
print(RSA_public)

#Cria um objeto CryptoEngine e inicia em modo AES
encryptor = CryptoEngine()
encryptor.init_AES_mode()

message_sent = 'Essa mensagem eh segredo'
AES_key = b'Sixteen byte key'#Chave AES tem que ter 16 bytes

print(message_sent)
print(AES_key)

#Encripta a msg, AES_info é uma tupla com a msg cifrada, uma tag(acho que é um hash da msg, um nonce e a assinatura da msg com a chave RSA
AES_info = encryptor.encrypt_AES_string(message_sent,AES_key,RSA_private)

cipher_message = AES_info[0]

print(cipher_message)

#Cria um objeto CryptoEngine e inicia em modo AES
decryptor = CryptoEngine()
decryptor.init_AES_mode()

#Descriptografa a msg
message_received = decryptor.decrypt_AES_string(AES_info,AES_key,RSA_public)

if(message_sent == message_received):
	print('Tudo ok')
	print(message_received)
else:
	print('Ops')
