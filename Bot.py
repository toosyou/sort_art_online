#!/usr/bin/python
# coding=utf-8
"""
This file contains the Bot class, which is initialize and used to complete
sets of actions.

NoKeyboardException is raised when we cannot find the On-Screen Keyboard.

Author: Alvin Lin (alvin.lin.dev@gmail.com)
"""
from __future__ import print_function
import math
import pyautogui
import sys
import time
import Keys
import win32gui
import numpy as np
from PIL import Image
import os
from threading import Thread

pyautogui.FAILSAFE = True

def flip_image(image_path, saved_location):
    """
    Flip or mirror the image

    @param image_path: The path to the image to edit
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
    rotated_image.save(saved_location)

def set_windows_front(program_name):
    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        # print(i[1])
        if program_name in i[1].lower():
            win32gui.ShowWindow(i[0],5)
            win32gui.SetForegroundWindow(i[0])
            # break

def flip_in_game_pics():
    prefix = './pics/in_game'
    filelist = ['char', 'char_on_portal']
    for filename in filelist:
        print(filename)
        flip_image(os.path.join(prefix, filename + '.png'), os.path.join(prefix, filename + '_flip.png'))

class NoKeyboardException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "No On-Screen Keyboard found. Try redo-ing your screenshot."

class Bot():
    def __init__(self):
        self.keys = Keys.Keys()
        if self.keys.up is None:
            raise NoKeyboardException()
        self.time_created = time.time()
        self.hp_pots_used = 0
        self.mana_pots_used = 0

    def getDebugText(self):
        """
        Returns debug text showing time running as well the amount of
        health/mana potions used and other statistical data.
        """
        timeDifference = time.time() - self.time_created
        hours = math.floor(timeDifference / 3600)
        minutes = math.floor((timeDifference % 3600) / 60)
        seconds = math.floor(timeDifference % 3600 % 60)

        output = "\n" * 50
        output += "Time started: %s\n" % time.ctime(self.time_created)
        output += "Time now: %s\n" % time.ctime()
        output += "Time elapsed: %02d:%02d:%02d\n" % (hours, minutes, seconds)
        output += ("=" * 80) + "\n"
        output += "Health potions used: %d\n" % self.hp_pots_used
        output += "Health potions per hour: %d\n" % (self.hp_pots_used / (
                timeDifference / 3600))
        output += "Mana potions used: %d\n" % self.mana_pots_used
        output += "Mana potions per hour: %d\n" % (self.mana_pots_used / (
                timeDifference / 3600))
        return output

    def locate_key(self, key, relative_size=(None, None)):
        loc = getattr(self.keys, key)
        pos_x = loc[0]
        pos_y = loc[1]
        size_x = loc[2] if (relative_size[0] is None) else relative_size[0]
        size_y = loc[3] if (relative_size[1] is None) else relative_size[1]
        return (pos_x + size_x//2, pos_y + size_y//2)

    def _mouse_moveTo(self, key, relative_size=(None, None)):
        """
        Helper method that moves the mouse to a specified coordinate.
        """
        x, y = self.locate_key(key, relative_size)
        pyautogui.moveTo(x, y)

    def click(self, key, duration=0.5, relative_size=(None, None)):
        """
        Given a key to click and a duration to click it for, this method will
        click the key for the given duration.
        """
        '''
        x, y = self.locate(key, relative_size)
        pyautogui.click(x, y, interval=duration)

        '''
        self._mouse_moveTo(key, relative_size)

        pyautogui.mouseDown()
        time.sleep(duration)
        pyautogui.mouseUp()
        time.sleep(0.25)

    def charactor_position(self):
        rtn = pyautogui.locateOnScreen('./pics/in_game/char.png', grayscale=True, confidence=0.7)
        if rtn is None:
            return pyautogui.locateOnScreen('./pics/in_game/char_flip.png', grayscale=True, confidence=0.7)
        return rtn

    def portal_position(self):
        return pyautogui.locateOnScreen('./pics/in_game/portal.png', grayscale=True, confidence=0.95)

    def char_on_portal(self):
        if pyautogui.locateOnScreen('./pics/in_game/char_on_portal.png', grayscale=True, confidence=0.95) is None:
            if pyautogui.locateOnScreen('./pics/in_game/char_on_portal_flip.png', grayscale=True, confidence=0.95) is None:
                return True
        return False

    def checkHealth(self, pot_key):
        """
        Given a key that is bound to a health potion, this method will check
        for a depleted health bar and use potions until it can no longer see a
        depleted health bar.
        """
        while not pyautogui.locateOnScreen('data/hp.png'):
            self.click(pot_key, 0.25)
            self.hp_pots_used += 1

    def checkMana(self, pot_key):
        """
        Given a key that is bound to a mana potion, this method will check for a
        depleted mana bar and use potions until it can no longer see a depleted
        mana bar.
        """
        while not pyautogui.locateOnScreen('data/mana.png'):
            self.click(pot_key, 0.25)
            self.mana_pots_used += 1

if __name__ == '__main__':
    flip_in_game_pics()

    bot = Bot()
    set_windows_front('maplestory')
    while(True):
        chr_pos = bot.charactor_position()
        por_pos = bot.portal_position()
        print(chr_pos, por_pos)
        if chr_pos is None or por_pos is None:
            print(bot.char_on_portal())
            if np.random.rand(1)[0] > 0.5:
                bot.click('right', 2)
            else:
                bot.click('left', 2)
        else:
            if chr_pos[0] - por_pos[0] > -1:
                Thread(target=bot.click, args=('left', 0.15)).start()
            elif por_pos[0] - chr_pos[0] > -1:
                Thread(target=bot.click, args=('right', 0.15)).start()
