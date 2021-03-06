#!/usr/bin/python
"""
Basic botting program for Zero. Works with my keybindings only.

Premise:
A - Giga Crash
S - Flash Cut
D - Rising Slash
Del - Shadow Rain
End - Rhinne's Protection

Ctrl - Health pots

Run while in Beta form standing on a platform with a wall to your right.
This will bump the character against the wall and spam abilties in all
directions. This bot is not smart responsive except for potting when your
HP is low, so make sure you have thousands of health potions. If you get
moved out of position, the bot will continue doing the same thing, so you
need to find a place to stand where mobs do not or can not attack you.

Author: Alvin Lin (alvin.lin.dev@gmail)
"""

from Bot import Bot
from Keys import Keys

import time

def main():
    bot = Bot()
    time.sleep(1)
    iterations_run = 0

    while True:
        print bot.getDebugText()
        bot.checkHealth(Keys.CTRL)
        bot.click(Keys.LEFT, 0.1)
        bot.click(Keys.D, 0.25)
        bot.click(Keys.D, 0.25)
        bot.checkHealth(Keys.CTRL)
        bot.click(Keys.S, 0.25)
        bot.click(Keys.S, 0.25)
        bot.checkHealth(Keys.CTRL)
        if iterations_run % 2 == 1:
            bot.click(Keys.A, 0.25)
            bot.click(Keys.A, 0.25)
            bot.click(Keys.A, 0.25)

        print bot.getDebugText()
        bot.checkHealth(Keys.CTRL)
        bot.click(Keys.RIGHT, 0.5)
        bot.click(Keys.D, 0.25)
        bot.click(Keys.D, 0.25)
        bot.checkHealth(Keys.CTRL)
        bot.click(Keys.S, 0.25)
        bot.click(Keys.S, 0.25)
        bot.checkHealth(Keys.CTRL)
        if iterations_run % 2 == 0:
            bot.click(Keys.A, 0.25)
            bot.click(Keys.A, 0.25)
            bot.click(Keys.A, 0.25)

        bot.checkHealth(Keys.CTRL)

        # Try to clear mobs every 2 iterations with ultimate ability
        if iterations_run % 2 == 0:
            bot.click(Keys.DEL, 0.25)

        # Buff self every 5 iterations
        if iterations_run % 5 == 0:
            bot.click(Keys.END, 0.25)
        print bot.getDebugText()

    iterations_run += 1

if __name__ == "__main__":
    main()
