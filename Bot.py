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
import keyboard

pyautogui.FAILSAFE = True

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

    def locate(self, key, relative_size=(None, None)):
        loc = getattr(self.keys, key)
        pos_x = loc[0]
        pos_y = loc[1]
        size_x = loc[2] if (relative_size[0] is None) else relative_size[0]
        size_y = loc[3] if (relative_size[1] is None) else relative_size[1]
        return (pos_x + size_x//2, pos_y + size_y//2)

    def _moveTo(self, key, relative_size=(None, None)):
        """
        Helper method that moves the mouse to a specified coordinate.
        """
        x, y = self.locate(key, relative_size)
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
        self._moveTo(key, relative_size)

        pyautogui.mouseDown()
        time.sleep(duration)
        pyautogui.mouseUp()
        time.sleep(0.25)

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

    bot = Bot()
    set_windows_front('maplestory')
    while(True):
        bot.click('left', 5)
