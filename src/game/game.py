import random

import pygame

from . import const

__level: int = 1
__radius: int = 10

def get_speed_multiplier() -> float:
    return 1.1 * 1.2 ** __level

def get_amount_multiplier() -> int:
    return int(20 + 5 * __level)

def increase_level(amount: int = 1):
    global __level
    __level += amount

def decrease_level(amount: int = 1):
    global __level
    __level = max(1, __level - amount)


class Target:
    def __init__(self, radius: int, position: pygame.Vector2):
        self.radius: int = radius
        self.position: pygame.Vector2 = position
        
        self.color: str = "#c42323"
        self.speed: pygame.Vector2 = pygame.Vector2(0, 1)


def update(delta_time_seconds: float):
    global __targets
    
    for target in __targets:
        if target.position.y > const.__WINDOW_SIZE[1]:
            __targets.remove(target)
        
        target.position += target.speed * delta_time_seconds * get_speed_multiplier()

def render(surface: pygame.Surface):
    for target in __targets:
        pygame.draw.circle(surface, target.color, target.position, target.radius)

def spawn_target():
    global __targets
    
    position = (random.randint(__radius, const.__WINDOW_SIZE[0] - __radius), __radius)
    __targets.append(Target(__radius, pygame.Vector2(position)))

__targets: list[Target] = []
