import string
import random
characters = string.ascii_letters + string.punctuation + string.digits

password = ""
password_length = random.randint(8, 10)

for x in range(password_length):
    char = random.choice(characters)
    #print(char)
    password = password + char

print(password)