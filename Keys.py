"""
This is a class that stores the coordinates of the keys on osk.png.
Author: Alvin Lin (alvin.lin.dev@gmail.com)
"""
from __future__ import print_function
import pyautogui
import os

KEY_LIST = list()
for filename in os.listdir('./pics/win10_keys/'):
    if filename.endswith('.png'):
        KEY_LIST.append( filename[:-4] )
print(KEY_LIST)

class Keys():
    def __init__(self, address_keys='./pics/'):
        self.address_keys = address_keys
        for k in KEY_LIST: setattr(self, k, pyautogui.locateOnScreen(os.path.join(self.address_keys, 'win10_keys', k+'.png'), grayscale=True, confidence=0.8 ))
        self.maplestory = pyautogui.locateOnScreen(os.path.join(self.address_keys, 'maplestory.png'))

if __name__ == '__main__':
    keys = Keys()
    print(keys.a, keys.s, keys.maplestory)
