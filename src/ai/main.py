import time

import cv2
import numpy as np
from PIL import ImageGrab
import win32api
import win32con

def click(position: tuple[int, int]) -> None:
    win32api.SetCursorPos(position)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.005)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def find_window():
    while True:
        target = cv2.imread("img/sample.png")
        screenshot = np.array(ImageGrab.grab())

        result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)
        threshold = .999

        match = np.where(result >= threshold)[::-1]
        
        
        try:
            position = tuple([i[0] for i in match])  #TODO Encontrar uma forma melhor de fazer isso...

        except IndexError:
            print("Janela não encontrada. Tentando novamente...")
            time.sleep(1)
            continue
        
        win32api.SetCursorPos(position)
        print(f"Janela encontrada! (X: {position[0]} | Y: {position[1]})")
        print(f"Posições totais encontradas: {len(match[0])}")
        len(match[0]) > 1 and print(match)
        #return


find_window()
