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
    return 1 + 1.07 ** __level - 1.035 ** __level + 1

def get_amount_multiplier() -> int:
    return int(20 + 5 * __level)

def get_cooldown_multiplier() -> int:
    return max(.05, 1 / 1.07 ** __level)

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
    global __current_cooldown
    global __lives
    
    __current_cooldown -= delta_time_seconds / const.__TARGET_FPS
    
    if __current_cooldown <= 0:
        spawn_target()
        __current_cooldown = __spawn_cooldown * get_cooldown_multiplier()
    
    for target in __targets:
        if target.position.y - target.radius > const.__WINDOW_SIZE[1]:
            __targets.remove(target)
            __lives -= 1
            update_gui()
        
        target.position += target.speed * delta_time_seconds * get_speed_multiplier()

def render(surface: pygame.Surface):
    for target in __targets:
        pygame.draw.circle(surface, target.color, target.position, target.radius)
    
    texts = [__level_text, __lives_text, __score_text]
    height = 5
    for text in texts:
        surface.blit(text, (5, height))
        height += 5 + text.get_height()

def spawn_target():
    global __targets
    global __total_targets_spawned
    
    position = (random.randint(__radius, const.__WINDOW_SIZE[0] - __radius), __radius)
    __targets.append(Target(__radius, pygame.Vector2(position)))
    __total_targets_spawned += 1
    
    if __total_targets_spawned % __targets_per_level == 0:
        increase_level()

def update_gui():
    global __level_text
    global __lives_text
    global __score_text
    
    __level_text = font.render(f"Nível: {__level}", True, "#eeeeee")
    __lives_text = font.render(f"Vidas: {__lives}", True, "#eeeeee")
    __score_text = font.render(f"Pontos: {__score}", True, "#eeeeee")

__targets: list[Target] = []

__level: int = 1
__lives: int = 3
__radius: int = 15
__total_targets_spawned: int = 0
__targets_per_level: int = 10
__score: int = 0

__spawn_cooldown: float = 1
__current_cooldown: float = __spawn_cooldown


font = pygame.font.Font(None, 25)

__level_text: pygame.Surface = font.render("Nível: x", True, "#eeeeee")
__lives_text: pygame.Surface = font.render("Vidas: x", True, "#eeeeee")
__score_text: pygame.Surface = font.render("Pontos: x", True, "#eeeeee")
update_gui()
