import pyautogui as pg
from random import choice
from time import sleep
animal = ('dog', 'cat', 'pig')
sleep(8)

for i in range(10):
  msg = choice(animal)
  pg.write('you are a'+msg)
  pg.press('enter')
