"""
a=input()
v={'a','e','i','o','u'}
r = {}
for i in a:
  if i in v:
    r[i] = r.get(i,0)+1
for k,va in sorted(r.items()):
  print(k,"repeated",va,"number of times")
#SUPER COOL PYTHON

string = input()
a = string.split()
result = []
i=0
while i<len(a):
  result.append(a[i][::-1])
  i = i+1
print(" ".join(result))
  

string = input()
string1 = []
for x in string:
  if x not in string1:
    string1.append(x)

print(''.join(string1))
string = input()
d = {}
for x in string:
  if x in d.keys():
    d[x] = d[x]+1
  else:
    d[x] = 1
for a,b in d.items():
  print(f"{a} is repeated {b} number of times")

n = int(input())
for i in range(n):
  for j in range(i+1):
    print("*",end='')
  print()
  

n = int(input())
for i in range(n+1):
  print(" "*(n-i),end="")
  print("* "*i)

s = "i gave an idea which is very good idea."
sub = "idea"
f = False
l  = len(s)
pos = -1
while True:
  pos = s.find(sub,pos+1,l)
  if pos == -1:
    break
  print("sub stringing found at ",pos)
  
  f = True
if f == False:
  print("sub stringing not found")
  
  
import sys
lis = sys.argv
for i in lis:
  print(i)
print(lis[0])
  
x = "madhu"
def play():
  x = "babu"
  print(globals()['x'])
  print(x)
print(x)
play()

def first(name):
  def second():
    return "Hello"
   result = second()+name
  print(result) 
first(" Madhu")
def first(a):
  return "Hello "+a
def second():
  return "Madhu"
print(first(second()))
def factorial(n):
  if n==0:
    return 1
  else:
    return n*factorial(n-1)
print(factorial(6))
list = [21,7,1999,21,5,1997]
result = list(filter(lambda x:'Yes' if x%2==0 else 'No',list))
print(result)

result = lambda x:'Yes' if x%2==0 else 'No'
print(result(10))
print(dir())  #prints avalible buildin functions of a module

# help function get the documentation of a module and its builtin functions
import sys
help(sys)
a = [2,3,4,5,6]
b = [2,5,7,8,9]
result = [i for i in a if i in b]
print(result)
#Parameterized Constringuctor in a Class
class Cse:
  def __init__(self):
    self.students = "Madhu"
    self.faculty = "Mukesh sir"
    self.instringuctor = "IDCard sir"
m1 = cse()
print(m1.students)
print(m1.faculty)
print(m1.instringuctor)

#NonParameterized Constringuctor in a Class

class Marks:
  def __init__(self,noOfSubjects,maths,physics,chemistringy):
    self.noOfSubjects = noOfSubjects
    self.maths = maths
    self.physics = physics
    self.chemistringy = chemistringy
  def average(self):
    avg = (self.maths+self.physics+self.chemistringy)/self.noOfSubjects
    return avg
o = Marks(3,92,89,75)
print(o.average())

#Class inside a class
class Car:
  def __init__(self,brand,mfd):
    self.Brand=brand
    self.manufacturingDate=mfd
  class Engine:
    def __init__(self,ENo):
      self.engineNo=ENo
    def start(self):
      print("Engine has been started")
o = Car("Buggati",2022)
o1 = o.Engine("s123jnw218")
o1.start()

class Benz:
  def __init__(self,name,mfd,eNo):
    self.name = name
    self.mfd = mfd
    self.eNo = eNo
    
  def breaks(self):
    print("Breaks are working Fine.")
    
class Features(Benz):
  def __init__(self,glassCleaner,backCamera,name,mfd,eNo):
    Benz.__init__(self,name,mfd,eNo)
    self.glassCleaner = glassCleaner
    self.backCamera = backCamera
    
    
o1 = Features(True,True,"Benz",2019,"snjnj823i")
print(o1.name)
print(o1.glassCleaner)
o1.breaks()
#Duck TAlk class
class Duck():
  def talk(self):
    print("Quack Quack")
class Human():
  def talk(self):
    print("Hey, How are you?")
def lk(obj):
  obj.talk()
d = Duck()
lk(d)
h = Human()
lk(h)
import sys,os
if os.path.isfile("main.py"):
  f = open("main.py","r")
  s = f.read()
  print(s)
  f.close()
else:
  print("file does not exist")
  sys.exit()
  
#Student Class
class Student:
  def __init__(self,name,score,subject="mathematics"):
    self.name = name
    self.score = score
    self.subject = subject
  def display(self):
    print(self.name,self.price,self.subject)

#Pickle Class
import pickle,student
f = open("madhu.txt","w")
s = student.Student("madhu",89)
pickle.dump(f)
f.close()

#Unpickle the dumped class
import pickle
f = open("madhu.txt","r")
obj = pickle.load(f)
print(obj.display())
f.close()  

# Regular Expressions
import re  #regular Expression module
string = "madhu is a very good Boy and he is good at studies too."
result = re.search(r'B\w\w',string)
print(result.group()) # we use group method for search inorder to display the contents

result = re.findall(r'g\w',string)
for i in result:
  print(i) #It will return all the matched stringings into a list.

result = re.match(r'm\w\w\w\w',string)
print(result.group())  # we use group method for match inorder to display the contents

import time
t= time.time()
ct = time.ctime(t)
print(t,ct)

from datetime import datetime,date
d = datetime.now()
print(d)
def ValidateCrediCard(expDate):
  if expDate>datetime.now().date():
    print("Card valid")
  else:
    print("Card Invalid")
ValidateCrediCard(date(2022,7,19))

# reading url content
import urllib.request
try:
  url = urllib.request.urlopen("https://www.geeksforgeeks.org/python-programming-language/?ref=shm")
  content = url.read()
  url.close()
except urllib.error.HTTPError:
  print("Invalid Url")
  exit()
f = open("gfg.html","wb")
f.write(content)
f.close()

# Download Image
import urllib.request
url = "https://instagram.fvtz3-2.fna.fbcdn.net/v/t51.2885-19/273746003_495998082154976_7239134497816860392_n.jpg?stp=dst-jpg_s320x320&_nc_ht=instagram.fvtz3-2.fna.fbcdn.net&_nc_cat=108&_nc_ohc=tGTotc6lBy8AX9g5BSH&tn=DtOeE-hKEyNVZyMn&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_AT-Wf4USA50_G5k1RoS1-SRnbjhE1opJyq0hC3gcS4OcGw&oe=62D75AC1&_nc_sid=8fd12b"
urllib.request.urlretrieve(url,"madhu.png")

#sending mail using Python script
import smtplib
from email.mime.text import MIMEText

body = "Hey this was a sent by using python script"
msg = MIMEText(body)
msg['From'] = "madhu54991@gmail.com"
msg['To'] = "madhu54991@gmail.com"
msg['Subject'] = "Python scripted mail"

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

server.login("madhu54991@gmail.com","M@dhu123")
server.send_message(msg)

print("unable to login")

print("mail has been sent")
server.quit()

n = int(input())
s = set(map(int,input().split()))
num = int(input())
for i in range(num):
    ip = input().split()
    if ip[0]=="remove":
        s.remove(int(ip[1]))
    elif ip[0]=="discard":
        s.discard(int(ip[1]))
    else :
        s.pop()
print(sum(list(s)))

def minion_game(string):
    if string.isupper() and string.isalpha():
        res =[string[i:j] for i in range(len(string)) for j in range(i+1,len(string)+1)]
        
    vow = "AEIOU"
    Kevin = []

    for ele in res:
        a = any(ele.startswith(ove) for ove in vow)
        if a:
            Kevin.append(ele)
            
    Stuart =[i for i in res if i not in Kevin ]
    if len(Stuart)>len(Kevin):
        print("Stuart",len(Stuart))
    elif len(Kevin)>len(Stuart) :
        print("Kevin",len(Kevin))
    else:
        print("Draw")

s = input()
if ==True:
    print(s.isalnum())
else:
    print("False")
if s.isalpha()==True:
    print(s.isalpha())
else:
    print("False")
if ==True:
    print(s.isdigit())
else:
    print("False")
if ==True:
    print(s.islower())
else:
    print("False")
if ==True:
    print(s.isupper())
else:
    print("False")
    

class MyClass:
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def addition(self):
    print(self.x+self.y)
class Add(MyClass):
  def __init__(self,x,y):
    super().__init__(x,y)

c = Add(1,2)
c.addition()

mytuple = "masdhu"
myit = iter(mytuple)
i = 0
while i < len(mytuple):
  print(next(myit))
  i += 1
from practice import *
print(addition(1,32))
import practice
x = dir(practice)
print(x)

import datetime
x = datetime.datetime(1999, 7, 21)
print(x.strftime("%A"),x.strftime("%B"),x.strftime("%Y"),sep ='-')

from json import *
# some JSON:
x = '{ "name":"John", "age":30, "city":"New York"}'
print(type(x))
# parse x:
y = loads(x)
print(type(y))
# the result is a Python dictionary:
print(y["age"])
print(y.items())
print("")
for k, v in y.items():
	print(k, v, sep = ':')

from json import *
x = { "name":"John", "age":30, "city":"New York"}
print(type(x))
print(type(dumps(x)))

import re
import inspect
src = inspect.getsource(re)
print(src)
b = [23,343,424,544,5,57,876,686]
#a = b.sort()  #return None
print(b.sort())
import re
#a = re.search(r'^b...',"foodmadhuhas")
#print(a.group())
#b = re.search(r'b\w+',"fooobbauydfgufbr")
#print(b.group())
b = re.search(r'b\w+',"fooobbauydfgufbr")
print(b.group())
import re
f = open('madhu.txt', 'r')
match = re.findall(r'\w+',f.read())
print("Executed")
for each in match:
print(each)
import re
def convert_into_uppercase(a):
  print(a.group(1))
  return a.group(1) + a.group(2).upper()

s = "python is best programming 2language"
result = re.sub(r"(^|\s)(\S)", convert_into_uppercase, s)

print(result)
N,S = input().split()
l = []
for _ in range(int(S)):
  l1 = map(float,input().split())
  l.append(l1)
  
for i in zip(*l):
  print(i)
  print(sum(i)/len(i))
l = []
l = [l.append(int(input(i))) for i in range(int(input()))]
for i in l:
    print(i)
list(range(10,1,-1))
N = float(input('How many hours did you work last month? '))
N1 = float(input('What is your hourly rate? '))
print(f'Last month, you earned {N*N1} dollars')
n = 0
while True:
    n = int(input('When was Python 1.0 released? '))
    if n==1994:
        print('Correct!')
        break
    elif n>1994:
        print('It was earlier than that!')       
    else :
        print('It was later than that!')

spendings = [1346.0, 987.50, 1734.40, 2567.0, 3271.45, 2500.0, 2130.0, 2510.30, 2987.34, 3120.50, 4069.78, 1000.0]
 
low = 0
normal = 0
high = 0
 
for month in spendings:
    if month < 1000.0:
        low += 1
    elif month <= 2500.0:
        normal += 1
    else:
        high += 1
 
print('Numbers of months with low spendings: ' + str(low) + ', normal spendings: ' + str(normal) + ', high spendings: ' + str(high) + '.')
print([float(i) for i in range(1,101)])

connections = [
    ('Amsterdam', 'Dublin', 100),
    ('Amsterdam', 'Rome', 140),
    ('Rome', 'Warsaw', 130),
    ('Minsk', 'Prague', 95),
    ('Stockholm', 'Rome', 190),
    ('Copenhagen', 'Paris', 120),
    ('Madrid', 'Rome', 135),
    ('Lisbon', 'Rome', 170),
    ('Dublin', 'Rome', 170),
    ]
count = 0
sum = 0
for i in connections:
    if i[1]=='Rome':
        count += 1
        sum += i[2]
avg = sum/count
print(f'{count} connections lead to Rome with an average flight time of {avg} minutes')

sample_dict = {
    "mouth": "Mund",
    "finger": "Finger",
    "leg": "Bein",
    "hand": "Hand",
    "face": "Gesicht",
    "nose": "Nase"
}
flag = True
while flag:
  prompt = input('Enter a word in English or EXIT: ')  
  if prompt == 'EXIT':
    print('Bye!')
    flag = False
  else :
    if prompt in sample_dict.keys():
      print(f'Translation: {prompt} << replace {sample_dict[prompt]} with the word from the dictionary')
    else:
      print('No match!')
print(69/92)

list_a = [1, 2, 3]
list_b = list_a[-2:-1]
list_c = list_a[-1:-3]
print(list_b, list_c)
temp_list = [1, 2, 3]
for i in range(len(temp_list)):
    temp_list.insert(i, 0)
print(temp_list)
values = [[3 - x for x in range(2)] for y in range(5)]
print(values)
 
sum = 0.0
for row in values:
  for cell in row:
    sum += cell
 
print(sum)
l = [1,2,3,4,5,6]
print(l[-2:-4])
my_list = [0, 1, 2] * 3 
print(my_list+ [0])
print(len(my_list)) 
for i in range(1,501):
  print(i)
def unique(a=[]):
    l = []
    l = [l.append(ele) for ele in a if ele not in l]
    print(l)
    

unique()
def unique(a=[]):
  l = []
  l = [l.append(ele) for ele in a if ele not in l]
  return l
print(unique([1,1,1,2,3]))
my_list = ['aaa', 'bbb', 'ccc']
 
def do(my_list):
   del my_list[1]
   my_list[1] = 'aaa'
 
do(my_list)
print(my_list)
def do_magic(a = 0):
    print(a)
print(None+2)
    
def numerical():
  for i in range(10):
    yield i%2
 
for x in numerical():
  print(x, end='-')

tuple_first = (1, 2, 3)
tuple_second = ('a', 'b')
tuple_combined = tuple_first + tuple_second * 2
print(tuple_combined)
lst = [1, 2] * 3
print(len(lst))
a='madhu'
a[6] = 'a'
print(a)
def func(num):
    if num %2 == 0:
        return True
    else:
        return False
 
print(not func(2))
def swap(x, y):
    x, y = y, x

 
x = 5
y = 10
swap(x, y)
print(x, y)
dict1 = {'one': 1, 'two': 2, 'three': 3}
dict2 = {'one': 1, 'two': 5, 'four': 8}
dict3 = dict(dict1)
dict4 = dict(dict2)
dict3.update(dict2)
dict4.update(dict1)
print(dict3.items())
print(dict4.items())
print(dict3 == dict4)


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        for i in range(len(self.nums)):
            for j in range(1,len(self.nums)):
                if nums[i]+nums[j]==target:
                    return i,j


nums = list(map(int ,input().split()))
target = int(input())
for i in range(len(nums)):
            for j in range(1,len(nums)):
                if nums[i]+nums[j]==target:
                    print(i,j,sep = ',')

        
def madhu(l=[]):
        l1 = []
        for i in l:
                if i not in l1:
                        l1.append(i)
        return l1
        
print(madhu([1,1,2,1,34,5,68,9]))
a = 'Hello World'
print(a[-3])


#enumerate
a = ['a','b','c','d','e','f','h','g']
for i,j in enumerate(a):
  print(i,j,sep = '-')


#Zip function
l1 = [0,1,2]
l2 = ['m','a','d']
print([i for i in zip(l1,l2)])


for i in range(1,101):
  if i%3 == 0 and i%5 == 0:
    print("FizzBuzz")
  elif i%3 == 0:
    print("Fizz")
  elif i%5 == 0:
    print("Buzz")
  else:
    print(i)



def unique(a=[1,1,1,2,3]):
  l = []  
  return [l.append(ele) for ele in a if ele not in l]
  
result = unique()
print(result)




#Ball position Guessing Game
from random import shuffle

def shuffle_list(my_list):
  shuffle(my_list)
  return my_list
  
def user_guess():
  guess = ''
  while guess not in ['0','1','2']:
    guess = input('Please enter a number 0,1 or 2: ')
  return int(guess) 

def check_guess(my_list,guess):
  if my_list[guess] =='O':
    print("Correct")
  else:
    print('Wrong guess')
    print(my_list)

my_list = [' ',' ','O']
shuffled_list = shuffle_list(my_list)
guess = user_guess()
check_guess(shuffled_list,guess)



#*args arguments
#*args return tuple containing of arguments
def myfunc(*args):  
    return sum(args)
def myfunc(*args):
  l=[]
  for i in args:
    if i%2==0:
      l.append(i)
  return l
  
print(myfunc(1,2,3,4,5,6,7,8,9))



#**kwargs Keyward arguments
#**kwargs return dictonary containing of arguments
def my_func(**kwargs):
  print(kwargs)
  for i in kwargs:
    print(i)
    
my_func(one='madhu',two='babu',three='tammu')


#aNtHrOpOmOrPhIsM
def myfunc(a):
  even = a[0:len(a):2].lower()
  odd = a[1:len(a):2].upper()
  for i,j in zip(even,odd):
    print(i,j,sep="",end='')
       
myfunc('Anthropomorphism')


#Animal Cracker
def animal_cracker(a):
  words = a.split()
  first_word = words[0]
  second_word = words[1]
  return first_word[0] == second_word[0]

print(animal_cracker("madhu babu"))

#makes_twenty
def makes_twenty(a,b):
  return (a+b)==20 or a==20 or b==20

print(makes_twenty(12,8))


#MacDonals
def m_d(a):
  return a[:3].capitalize() + a[3:].capitalize()

print(m_d('madhu'))


#reverse the wod in a sentence 
def reverse_words(a):
  return ' '.join(a.split()[::-1])
  
print(reverse_words("madhu is a very good boy"))


#paper doll
def paper_doll(a):
  b = ''
  for i in a:
    b += (i*3)
  return b

print(paper_doll(input("enter a word: ")))


#blackjack 
def black_jack(x,y,z):
  a = x+y+z
  if  a<= 21:
    return a
  elif a>21 and x==11 or y==11 or z==11:
    return a-10
  else:
    return 'BUST'

print(black_jack(11,0,9))


#spy_game
def spy_game(l):
  l1 = [0,0,7,'5']
  for i in l:
    if i==l1[0]:
      l1.pop(0)
  return len(l1)==1

print(spy_game([1,0,0,3,0,8,9]))


#prime numbers in a range
def no_of_primes(a):
  prime_count = 0
  l = []
  for num in range(1,a+1):
    if num>1:
      for i in range(2,num):
        if num%i==0:
          break
      else:
        l.append(num)
        prime_count += 1
  print(l)
  return prime_count

print(no_of_primes(1000))       



r1 = ['','','']
r2 = ['','','']
r3 = ['','','']
#display matrix
def display(row1,row2,row3):
  print(row1)
  print(row2)
  print(row3)

#user input
def user_input(x,o):



#Tic Tac Toe project
#Board printing
#from IPython.display import clear_output
def board_printing(board_list):
  #clear_output()
  print(board_list[0],'|',board_list[1],'|',board_list[2])
  print('---------')
  print(board_list[3],'|',board_list[4],'|',board_list[5])
  print('---------')
  print(board_list[6],'|',board_list[7],'|',board_list[8])

#print(board_printing(board_list))


#Taking players input
def player_input():
    player = ''
    while player!='X' and player!='O':
        player = input('Player1 enter X or O: ').upper()
    if player == 'X':
        return ('X','O')
    else:
        return ('O','X')

#print(player_input())

#place marker at a index
def place_marker(board_list,player,index):
  board_list[index] = player

#print(place_marker(board_list,'x',3))

#Check the winner
def win_check(board_list,player):
  return (board_list[0] == board_list[1] == board_list[2] == player) or (board_list[3] == board_list[4] == board_list[5] == player) or (board_list[6] == board_list[7] == board_list[8] == player) or (board_list[0] == board_list[3] == board_list[6] == player) or (board_list[1] == board_list[4] == board_list[7] == player) or (board_list[2] == board_list[5] == board_list[9] == player) or (board_list[0] == board_list[4] == board_list[8] == player) or (board_list[2] == board_list[4] == board_list[6] == player)


#print(win_check(board_list,'X'))

#who is first
import random
def choose_first():
  flip = random.randint(0,1)
  if flip == 0:
    return 'Player 1'
  else:
    return 'Player 2'
#print(choose_first())

#space available or not in the board
def space_check(board_list,position):
  return board_list[position] == ' '
  
#print(space_check(board_list,3))

#check for board is full condition
def check_board_full(board_list):
  for i in [0,1,2,3,4,5,6,7,8]:
    if space_check(board_list,i):
      return False
  return True
  
#print(check_board_full(board_list))
# check for players choice of index
def player_choice(board_list):
  position = -1
  while position not in range(0,9) or not space_check(board_list, position):
    position = int(input('enter a position in between(0-8): '))
  return position
  
#print(player_choice(board_list))

#replay the game?
def replay():
  choice = input("Do you want to play the game again ? (Y|N): ").upper()
  return choice == 'Y'
#replay()

#main logic Of Tic Tac Toe Game
print("====Welcome to Tic Tac Toe====")
while True:
  
  #setting things ready
  board = [' ']*10
  player1_marker,player2_marker = player_input()
  player_turn = choose_first()
  print(player_turn+" Will go First!!!!!.")
  play_game = input("Ready to play the Game? (Y|N): ").upper()
  if play_game=='Y':
    game_on = True
  else:
    game_on = False
  while game_on:
#player 1 Turn
    if player_turn == 'Player 1':
      board_printing(board)
      position = player_choice(board)
      place_marker(board,player1_marker,position)

      if win_check(board,player1_marker):
        board_printing(board)
        print('Player 1 has won the match !!!:).')
        game_on = False
      else:
        if check_board_full(board):
          board_printing(board)
          print("It's a Tie!!!!")
          game_on = False
        else:
          player_turn = 'Player 2'
#player 2 Turn
    else:
      board_printing(board)
      position = player_choice(board)
      place_marker(board,player2_marker,position)

      if win_check(board,player2_marker):
        board_printing(board)
        print('Player 2 has won the match !!!:).')
        game_on = False
      else:
        if check_board_full(board):
          board_printing(board)
          print("It's a Tie!!!!")
          game_on = False
        else:
          player_turn = 'Player 1'


  if not replay():
    break
  




#==================================================
#object oriented programming
class Sample():
  species = 'mammals'
  def __init__(self,breed='lab',name='Jimmy'):
    self.breed  = breed
    self.name = name
  def hi(self):
    print('hey there ! Hi...')
#instan  = Sample("Lab") 
#print(instan.breed)
#print(instan.name)
#print(instan.species)  #species is a class object attribute will be declared befor __init__() method.

class Circle(Sample):
  pi=3.414
  def __init__(self,radius,breed):
    Sample.__init__(self) 
    self.breed = breed
    self.radius  = radius
    self.area = radius*2*Circle.pi #self.pi also you can use becuase it is a class object attribute.

c = Circle(2,'retriever')
print(c.name)
print(c.breed)
c.hi()
#obj = Circle(2)
#print(obj.area)


#practice problem
class Line:
  def __init__(self,cor1,cor2):
    self.cor1 = cor1
    self.cor2 = cor2
  def distance(self):
    x1,y1 = self.cor1
    x2,y2 = self.cor2
    return ((x2-x1)**2+(y2-y1)**2)**0.5

  def slope(self):
    x1,y1 = self.cor1
    x2,y2 = self.cor2 
    return (y2-y1)/(x2-x1)
obj = Line((3,2),(8,10))
print(obj.distance())
print(obj.slope())




#practice problem of Account Transactions
class Account:
  def __init__(self,acc_holder_name, acc_balance):
    self.acc_holder_name = acc_holder_name
    self.acc_balance = acc_balance

  def deposit(self,ammount):
    print(f'Current ammount is {self.acc_balance+ammount} rupees.')
    self.acc_balance += ammount
  def withdrawal(self,withdrawal_ammount):

    if withdrawal_ammount<=self.acc_balance:
      self.acc_balance -= withdrawal_ammount
      print(f'{withdrawal_ammount} rupees has been debited from your account and the remaining ammount is {self.acc_balance} rupees.')
    else:
      print('No sufficient balance in your account, Please enter another ammount')

  def __str__(self):
    return (f'{self.acc_holder_name} has {self.acc_balance} rupees in his Account.')
 

obj = Account(input('Enter Account holder name:'),int(input("Enter account balance: ")))
print(obj)
obj.deposit(int(input('Enter ammount to be credited: ')))
obj.withdrawal(int(input('Enter ammount to be debited: ')))


from colorama import init,Fore
init()
print(Fore.MAGENTA+"Hey Madhu ,Hi.....")




#Errors and Exception handling using try, except and finally blocks
def fun():
  while True:
    try:
      number = int(input("please provide an integer: "))
    except:
      print("it's not an integer\nplease try again to enter a number!!")
      continue
    return f'Square of {number} is {number**2}'
    break

print(fun())
  





#project cards
#global Variables declaration 
import random
suits=('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':11,'Queen':12,'King':13,'Ace':14}



#Desing the card class
class Card():
  def __init__(self,suit,rank):
    self.suit = suit
    self.rank = rank
    self.value = values[rank]

#for printing the card rank and suit of the card   
  def __str__(self):
    return self.rank+" of "+self.suit

#Deck Class
class Deck():
  def __init__(self):
    self.all_cards = []
    for suit in suits:
      for rank in ranks:
        created_card = Card(suit,rank)
    
        self.all_cards.append(created_card)
# For shuffling of cards in a deck 
  def shuffle(self):
    random.shuffle(self.all_cards)

#For drawing out a single card from the deck of cards
  def draw_one_card(self):
    return self.all_cards.pop()


#for inserting a single or a list of cards and removing of card from top of the deck 
#player class
class Player:
  def __init__(self,name):
    self.name = name
    self.all_cards = []

#For removing a card from the top of the deck
  def remove_card(self):
    return self.all_cards.pop(0)

#for adding a single card or a list of cards
  def add_cards(self,new_card):
    #checking whether new cards is a list or single card
    if type(new_card) == type([]):
      return self.all_cards.extend(new_card)
    else:
      return self.all_cards.append(new_card)

#for printing no of cards does the player have.
  def __str__(self):
    return f'{self.name} has {len(self.all_cards)} cards'



    
#main LOgic of the the Cards Game
#creating 2 objects for two players
player_1 = Player("player 1")
player_2 = Player("player 2")

#creating object for deck class
new_deck = Deck()
new_deck.shuffle()
new_deck.shuffle()

#Distribution of cards to the players equally
for i in range(26):
  player_1.add_cards(new_deck.draw_one_card())
  player_2.add_cards(new_deck.draw_one_card())

rounds = 0
game_on = True

while game_on:
  rounds += 1
  print(f'Round {rounds}')
  #player 1 has no cards
  if len(player_1.all_cards) == 0:
    print(f"player 1 has no cards left!\n{player_2.name} won the game.")
    game_on = False
    break
  #player 2 has no cards
  if len(player_2.all_cards) == 0:
    print(f"player 2 has no cards left!\n{player_1.name} won the game.")
    game_on = False
    break


  player_one_new_cards = []
  player_one_new_cards.append(player_1.remove_card())
  
  player_two_new_cards = []        
  player_two_new_cards.append(player_2.remove_card())   

  #war
  at_war = True
  while at_war:
    if player_one_new_cards[-1].value > player_two_new_cards[-1].value:
      player_1.add_cards(player_one_new_cards)
      player_1.add_cards(player_two_new_cards)
      at_war = False
    
    elif player_one_new_cards[-1].value < player_two_new_cards[-1].value:
      player_2.add_cards(player_one_new_cards)
      player_2.add_cards(player_two_new_cards)
      at_war = False
      
      
    else:
      print('At War!')
      if len(player_1.all_cards)<5:
        print(f"{player_1.name} unable to declare War\n{player_2.name} WINS!!!")
        game_on = False
        break
      elif len(player_2.all_cards)<5:
        print(f"{player_2.name} unable to declare War\n{player_1.name} WINS!!!")
        game_on = False
        break
      else:
        for i in range(5):
          player_one_new_cards.append(player_1.remove_card())
          player_two_new_cards.append(player_2.remove_card())
    






#returning function from another function.
def func(name='Madhu '):
  def in_func():
    print('Inside Function of func')  
  return in_func

f = func("madhubabu")
print(f())

#Passing function as parameter
def func_1(fun_as_input):
  print(fun_as_input())



#Decorater function
def decorator(some_function):
  def func_inside_decorater():
    print("welcome to the user before decoration.")
    some_function()
    print("welcome to the user after decoration.")
  return func_inside_decorater
  
@decorator
def test_decorator():
   print('This is a testing for function decoration.')

test_decorator()



#Generator and iterators 
#printing numbers from 1 t0 10
'''we use yield keyword to yield some value based on some certan condition and we user iter() function to iterate through the yielded value and we use next() to get a value which we have been iterated using iter function'''
def test_generator(n):
  for i in range(n):
    yield i

print(list(test_generator(10)))

str = 'this is a string'
iterate = iter(str)
for i in range(len(str)):
  print(next(iterate))


#some useful modules in python
from collections import Counter
l  = [1,1,1,1,1,2,2,2,23,3,3,3,34,4,4,]
Counter(l)
import os
os.cwd()

import os
import shutil
cwd = 'C:\\Users\MADHU\Desktop\python Code'
os.chdir(cwd)
"""
"""templateName=$1
propertyFileName=$2 
envtype=$3

./sagcc exec   templates composite apply $templateName -i $propertyFileName environment.type=$envtype

import subprocess
import os
templateName=input("please enter templateName: ")
propertyFileName=input('please enter propertyFileName: ')
envtype=input('please enter envtype: ')


cmd = f"'./sagcc exec   templates composite apply {templateName} -i {propertyFileName} environment.type={envtype}'"
directory = 'C:\\Users\MADHU\Desktop\python Code\Python_Coding'
os.chdir(directory)

subprocess.run('TicTacToeGame.py')

import os
 
# Path
path = 'C:\\Users\MADHU'
 
# Join various path components
print(os.path.join(path, "Desktop\python Code\Python_Coding", "file.txt"))
with open('file.txt') as f:
  f.read()
 
"""
#regular expressions
'''
\d -->digit
\D -->Non digit
\w -->alpha numeric
\W -->Non alha numeric
\s -->white space
\S -->Non white space
+ -->one or more times
* -->zero or more
^ -->Starts with
$ -->Ends with
{} -->range
| --> or
. -->Attachment 'madhu'  r'....u'  o/p:'hu'
[] -->Exclude condition that matches in square brace



import re 

def search(file,pattern = r'[^\d]+'):
  with open(file) as f:
    file_content = f.read()
    print(file_content)
    result = re.findall(pattern,file_content)
  return result
  
  
print(search('madhu.txt'))  
    
'''
