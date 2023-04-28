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

def find_in_image(needle: np.array, haystack: np.array, threshold: float = .999):
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    
    #  Filtra os resultados menores que o mínimo e inverte a coord X e Y
    matches = np.array(np.where(result >= threshold)[::-1])
    
    #  Retorna nada caso nenhum resultado tenha sido encontrado
    if matches.size == 0:
        return
    
    #? Encontrar uma forma de sempre utilizar o MELHOR match ao invés do primeiro
    chosen_match = [i[0] for i in matches]
    
    position_x, position_y = chosen_match
    height, width, _ = needle.shape  # needle.shape = (rows, columns, channels)
    return pygame.Rect(
        position_x,
        position_y,
        width,
        height
    )
    
    
    
def find_window():
    global _window_rect
    
    screenshot = np.array(ImageGrab.grab())
    top_left = find_in_image(_top_left_corner, screenshot)
    bottom_right = find_in_image(_bottom_right_corner, screenshot)
    
    if top_left and bottom_right:
        _window_rect = pygame.Rect(
            top_left.left,
            top_left.top,
            bottom_right.right - top_left.left,
            bottom_right.bottom - top_left.top
        )
        pop_state()


def loop():
    while True:
        delta_time_seconds: float = 0
        
        function = get_current_state()
        if function is None:
            return
    
        function()

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


_top_left_corner: np.array = cv2.imread("img/top_left.png")
_bottom_right_corner: np.array = cv2.imread("img/bottom_right.png")

_window_rect: pygame.Rect = None


register_state('find_window', find_window)
push_state('find_window')

loop()

