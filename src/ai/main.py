import time
import typing

import cv2
import numpy as np
from PIL import ImageGrab
import pygame
import win32api
import win32con


class Rectangle(pygame.Rect):
    def __init__(self, left: int, top: int, width: int, height: int):
        super().__init__(left, top, width, height)
    
    def absolute_rect(self) -> tuple[int, int, int, int]:
        return (self.left, self.top, self.right, self.bottom)


def click(position: tuple[int, int]) -> None:
    win32api.SetCursorPos(position)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(.01)

def find_in_image(needle: np.array, haystack: np.array, threshold: float = .999, best_only=False):
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    
    #  Filtra os resultados menores que o mínimo e inverte a coord X e Y
    matches = np.array(np.where(result >= threshold)[::-1])
    
    height, width, _ = needle.shape  # needle.shape = (rows, columns, channels)
    
    output = []
    for x, y in zip(*matches):
        output.append(
            (
                result[y][x],
                Rectangle(
                    x,
                    y,
                    width,
                    height
                )
            )
        )
    
    output.sort(key=lambda x: x[0])
    
    if best_only:
        return output[0][1]
    else:
        return [i[1] for i in output]

def find_window():
    global _window_rect
    
    screenshot = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
    top_left = find_in_image(_top_left_corner_image, screenshot, best_only=True)
    bottom_right = find_in_image(_bottom_right_corner_image, screenshot, best_only=True)
    
    if top_left and bottom_right:
        _window_rect = Rectangle(
            top_left.left,
            top_left.top,
            bottom_right.right - top_left.left,
            bottom_right.bottom - top_left.top
        )
        
        #  Coloca o mouse em cada ponta para confirmar que a janela foi encontrada corretamente
        win32api.SetCursorPos(_window_rect.topleft)
        time.sleep(.25)
        win32api.SetCursorPos(_window_rect.topright)
        time.sleep(.25)
        win32api.SetCursorPos(_window_rect.bottomright)
        time.sleep(.25)
        win32api.SetCursorPos(_window_rect.bottomleft)
        time.sleep(.25)
        win32api.SetCursorPos(_window_rect.center)
        time.sleep(.25)

        push_state('play_game')

def play_game():
    screenshot = cv2.cvtColor(
        np.array(
            ImageGrab.grab(
                bbox=(
                    _window_rect.left,
                    _window_rect.top,
                    _window_rect.right,
                    _window_rect.bottom
                )
            )
        ), 
        cv2.COLOR_RGB2BGR
    )
    #  Encontra os alvos na tela
    targets = find_in_image(_target_image, screenshot, .99)
    
    for target in targets:
        click(
            (
                _window_rect.left + target.centerx,
                _window_rect.top + target.bottom
            )
        )

def loop():
    while True:
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


_top_left_corner_image: np.array = cv2.imread("img/top_left.png")
_bottom_right_corner_image: np.array = cv2.imread("img/bottom_right.png")
_target_image: np.array = cv2.imread("img/target.png")

_window_rect: Rectangle = None

register_state('find_window', find_window)
register_state('play_game', play_game)
push_state('find_window')

loop()

