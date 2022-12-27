str = input('Enter some text as you like: ')
from cryptography.fernet import Fernet
import rsa
key = Fernet.generate_key()
print(key)
fernet = Fernet(key)
encrypted = fernet.encrypt(str.encode())
decrypted = fernet.decrypt(encrypted).decode()
print('original msg:\n',str,'\n\nEncrypted msg:\n',encrypted,'\n\ndecrypted msg:\n',decrypted)