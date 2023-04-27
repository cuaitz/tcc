import time
import typing

import cv2
import numpy as np
from PIL import ImageGrab
import pygame
import win32api
import win32con

def click(position: tuple[int, int]) -> None:
    win32api.SetCursorPos(position)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.005)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def find_window():
    while True:
        target = cv2.imread("img/top_left.png")
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


def loop():
    while True:
        delta_time_seconds: float = 0
        get_current_state().update(delta_time_seconds)

def register_state(name: str, function: typing.Callable[[float], None]):
    global __states
    
    if name in __states:
        raise KeyError(f"Um state já foi registrado com o nome \"{name}\".")
    
    __states[name] = function
    
def push_state(name: str):
    global __state_stack
    
    if not name in __states:
        raise KeyError(f"Nenhum state foi registrado com o nome \"{name}\".")
    
    __state_stack.append(__states[name])

def pop_state():
    global __state_stack
    
    if __state_stack:
        __state_stack.pop()

def get_current_state():
    try:
        return __state_stack[-1]
    except IndexError:
        return None


__states = {}
__state_stack = []
