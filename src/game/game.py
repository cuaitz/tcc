import random

import pygame

from . import const


class Target:
    def __init__(self, radius: int, position: pygame.Vector2):
        self.radius: int = radius
        self.position: pygame.Vector2 = position
        
        self.color: str = "#c42323"
        self.speed: pygame.Vector2 = pygame.Vector2(0, 1)


def get_speed_multiplier() -> float:
    return 1.1 * 1.2 ** __level

def get_amount_multiplier() -> int:
    return int(20 + 5 * __level)

def increase_level(amount: int = 1):
    global __level
    __level += amount
    update_gui()

def decrease_level(amount: int = 1):
    global __level
    __level = max(1, __level - amount)
    update_gui()

def update(delta_time_seconds: float):
    global __targets
    
    for target in __targets:
        if target.position.y > const.__WINDOW_SIZE[1]:
            __targets.remove(target)
            update_gui()
        
        target.position += target.speed * delta_time_seconds * get_speed_multiplier()

def render(surface: pygame.Surface):
    for target in __targets:
        pygame.draw.circle(surface, target.color, target.position, target.radius)
    
    surface.blit(__level_text, (5, 5))
    surface.blit(__lives_text, (5, 10 + __level_text.get_height()))

def spawn_target():
    global __targets
    
    position = (random.randint(__radius, const.__WINDOW_SIZE[0] - __radius), __radius)
    __targets.append(Target(__radius, pygame.Vector2(position)))
def update_gui():
    global __level_text
    global __lives_text
    
    __level_text = font.render(f"Nível: {__level}", True, "#eeeeee")
    __lives_text = font.render(f"Vidas: {__lives}", True, "#eeeeee")

__targets: list[Target] = []

__level: int = 1
__lives: int = 3
__radius: int = 15

font = pygame.font.Font(None, 25)

__level_text: pygame.Surface = font.render("Nível: x", True, "#eeeeee")
__lives_text: pygame.Surface = font.render("Vidas: x", True, "#eeeeee")
update_gui()
