import time
import typing

import cv2
import mss
import numpy as np
import pygame
import win32api
import win32con


class Rectangle(pygame.Rect):
    def __init__(self, left: int, top: int, width: int, height: int) -> None:
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

def take_screenshot(area: tuple[int, int, int, int]) -> np.array:
    #  Captura a tela
    screenshot = np.array(_screenshoter.grab(area))
    
    #  Converte a cor para o formato utilizado pelo cv2, BGR
    return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

def find_in_image(
    template: np.array,
    area: np.array,
    threshold: float = .999) -> list[float, Rectangle]:
    
    #  Faz a busca do template na imagem
    result = cv2.matchTemplate(area, template, cv2.TM_CCOEFF_NORMED)
    
    #  Filtra os resultados menores que o mínimo
    matches = np.where(result >= threshold)
    
    ...
    
    #  Inverte a coordenada X e Y
    matches = matches[::-1]
    
    
    height, width, _ = template.shape  # needle.shape = (rows, columns, channels)
    
    output = []
    for x, y in zip(*matches):
        output.append(
            (result[y][x], Rectangle(x, y, width, height))
        )
    
    #  Organiza pela similaridade de maneira decrescente
    output.sort(key=lambda x: x[0], reverse=True)
    
    return output

def find_window() -> None:
    global _window_rect
    screenshot = take_screenshot(_screenshoter.monitors[1])
    
    
    top_left_corner = find_in_image(_top_left_corner_image, screenshot)
    bottom_right_corner = find_in_image(_bottom_right_corner_image, screenshot)
    
    if top_left_corner and bottom_right_corner:
        top_left_rect = top_left_corner[0][1]
        bottom_right_rect = bottom_right_corner[0][1]
        
        _window_rect = Rectangle(
            top_left_rect.left,
            top_left_rect.top,
            bottom_right_rect.right - top_left_rect.left,
            bottom_right_rect.bottom - top_left_rect.top
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

def play_game() -> None:
    screenshot = take_screenshot(_window_rect.absolute_rect())
    
    #  Encontra os alvos na tela
    targets = find_in_image(_target_image, screenshot, .99)
    
    for coef, target in targets:
        click(
            (
                _window_rect.left + target.centerx,
                _window_rect.top + target.bottom
            )
        )

def loop() -> None:
    while True:
        
        function = get_current_state()
        if function is None:
            return
    
        function()

def register_state(name: str, function: typing.Callable[[float], None]) -> None:
    global __states
    
    if name in __states:
        raise KeyError(f"Um state já foi registrado com o nome \"{name}\".")
    
    __states[name] = function
    
def push_state(name: str) -> None:
    global __state_stack
    
    if not name in __states:
        raise KeyError(f"Nenhum state foi registrado com o nome \"{name}\".")
    
    __state_stack.append(__states[name])

def pop_state() -> None:
    global __state_stack
    
    if __state_stack:
        __state_stack.pop()

def get_current_state() -> None | typing.Callable:
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
_screenshoter = mss.mss()
register_state('find_window', find_window)
register_state('play_game', play_game)
push_state('find_window')

loop()
