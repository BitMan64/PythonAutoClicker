#!/usr/bin/env python3
# Threaded auto clicker
# -*- coding: utf-8 -*-

# Programmed by BitMan64 with minor changes by CoolCat467

import os, time
from threading import Thread

# To change back to original mode without clicks per seccond
# regulation, change REGULATE to False.
REGULATE = True

try:
    from pynput.mouse import Button, Controller
    from pynput.keyboard import Listener, KeyCode
except ImportError:
    print('Error: pynput not found!')
    print('Please install pynput for this program to function!')
    print('Would you like to attempt to automatically install pynput?')
    autoinstall = input('(y/n) : ').lower() in ('y', 'yes')
    if autoinstall:
        print('\nAttempting automatic install...')
        cmdout = os.system('pip3 install pynput --user')
        if cmdout == 0:
            print('pynput installed successfully! Please restart the program.')
        else:
            print('Attempted install returned with code %i.' % cmdout, file=os.sys.stderr)
            autoinstall = False
    if not autoinstall:
        print('Please install pynput manually with "pip3 install pynput --user".')
    sand = input('Press Press Return to Continue. ')
    os.abort()

__title__ = 'Threaded Auto Clicker'
__author__ = 'BitMan64 & CoolCat467'
__version__ = '1.1.0'
__ver_major__ = 1
__ver_minor__ = 1
__ver_patch__ = 0

TOGGLEDELAY = 1

def delaySet():
    while True:
        try:
            delay = 1 / int(input('Enter clicks per seccond: '))
        except ValueError:
            print('Please enter a valid number.\n')
        else:
            break
    return delay

class ClickMouse(Thread):
    """Thread that uses a mouse object to click a given button with a delay."""
    def __init__(self, mouse, button, delay=0):
        Thread.__init__(self)
        self.mouse = mouse
        self.button = button
        self.delay = float(delay)
        self.lastToggle = 0
        self.click = False
        self.active = False
        self.start()
    
    def toggle(self):
        if time.time() + TOGGLEDELAY > self.lastToggle:
            self.lastToggle = int(time.time())
            self.click = not self.click
    
    def exit(self):
        self.click = False
        self.active = False
    
    def run(self):
        if not REGULATE:
            self.active = True
            while self.active:
                if self.click:
                    self.mouse.click(self.button)
                time.sleep(self.delay)
        else:
            self.active = True
            last = time.time()
            count = 0
            originalDelay = self.delay
            targetCps = 1 / originalDelay
            while self.active:
                if self.click:
                    self.mouse.click(self.button)
                    count += 1
                    change = time.time() - last
                    if change >= 1:
                        cps = count / change
                        last = time.time()
                        if cps != targetCps:
                            deltacps = targetCps - cps
                            self.delay += (1/deltacps)
                    time.sleep(self.delay)
                else:
                    time.sleep(0.001)
    pass

def run():
    mouse = Controller()
    leftclick = Button.left
    rightclick = Button.right
    
    delay = delaySet()
    
    leftclick_thread = ClickMouse(mouse, leftclick, delay)
    rightclick_thread = ClickMouse(mouse, rightclick, delay)
    
    print('To toggle left clicking, press the "1" key.\nTo toggle right clicking, press the "2" key.\nPress the "3" key to stop clicking.\nPress the "`" key (grave accent) to stop the program.')
    
    leftToggle = KeyCode(char='1')
    rightToggle = KeyCode(char='2')
    stopClicking = KeyCode(char='3')
    exit_key = KeyCode(char='`')
    
    def ToggleKeys():
        def on_press(key):
            if key == leftToggle:
                leftclick_thread.toggle()
            elif key == rightToggle:
                rightclick_thread.toggle()
            elif key == stopClicking:
                leftclick_thread.click = False
                rightclick_thread.click = False
            elif key == exit_key:
                listener.stop()
        with Listener(on_press=on_press) as listener:
            listener.join()
    try:
        ToggleKeys()
    finally:
        leftclick_thread.exit()
        rightclick_thread.exit()

if __name__ == '__main__':
    print('%s v%s Programmed by %s.\n' % (__title__, __version__, __author__))
    run()
