import math
import random

import pygame

from .. import const

from . import state


class PlayingState(state.GameState):
    def process_event(self, event: pygame.event.Event):
        global _score
        global _targets
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for target in _targets:
                    click_position = event.pos
                    target_center = target.position
                    target_radius = target.radius
                    
                    distance = math.dist(click_position, target_center)
                    
                    if distance <= target_radius:
                        _targets.remove(target)
                        _score += 1 * _level
                        update_gui()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                spawn_target()
            elif event.key == pygame.K_a:
                decrease_level()
            elif event.key == pygame.K_d:
                increase_level()
        
    def update(self, delta_time_seconds: float):
        global _targets
        global _current_cooldown
        global _lives
        
        _current_cooldown -= delta_time_seconds / const.TARGET_FPS
        
        if _current_cooldown <= 0:
            spawn_target()
            _current_cooldown = _spawn_cooldown * get_cooldown_multiplier()
        
        for target in _targets:
            if target.position.y - target.radius > const.WINDOW_SIZE[1]:
                _targets.remove(target)
                _lives -= 1
                if _lives <= 0:
                    restart_game()
                update_gui()
            
            target.position += target.speed * delta_time_seconds * get_speed_multiplier()

    def render(self, surface: pygame.Surface):
        surface.fill("#232323")
        for target in _targets:
            pygame.draw.circle(surface, target.color, target.position, target.radius)
        
        texts = [_level_text, _lives_text, _score_text]
        height = 5
        for text in texts:
            surface.blit(text, (5, height))
            height += 5 + text.get_height()


class Target:
    def __init__(self, radius: int, position: pygame.Vector2):
        self.radius: int = radius
        self.position: pygame.Vector2 = position
        
        self.color: str = "#c42323"
        self.speed: pygame.Vector2 = pygame.Vector2(0, 1)


def get_speed_multiplier() -> float:
    return 1 + 1.07 ** _level - 1.035 ** _level + 1

def get_amount_multiplier() -> int:
    return int(20 + 5 * _level)

def get_cooldown_multiplier() -> int:
    return max(.05, 1 / 1.07 ** _level)

def increase_level(amount: int = 1):
    global _level
    _level += amount
    update_gui()

def decrease_level(amount: int = 1):
    global _level
    _level = max(1, _level - amount)
    update_gui()

def restart_game():
    global _targets
    global _level
    global _lives
    global _total_targets_spawned
    global _current_cooldown
    global _score
    
    _targets = []
    _level = 1
    _lives = 3
    _total_targets_spawned= 0
    _current_cooldown = 0
    _score = 0
    update_gui()

def spawn_target():
    global _targets
    global _total_targets_spawned
    
    position = (random.randint(_radius, const.WINDOW_SIZE[0] - _radius), _radius)
    _targets.append(Target(_radius, pygame.Vector2(position)))
    _total_targets_spawned += 1
    
    if _total_targets_spawned % _targets_per_level == 0:
        increase_level()

def update_gui():
    global _level_text
    global _lives_text
    global _score_text
    
    _level_text = font.render(f"Nível: {_level}", True, "#eeeeee")
    _lives_text = font.render(f"Vidas: {_lives}", True, "#eeeeee")
    _score_text = font.render(f"Pontos: {_score}", True, "#eeeeee")

_targets: list[Target] = []

_level: int = 1
_lives: int = 3
_radius: int = 15
_total_targets_spawned: int = 0
_targets_per_level: int = 10
_score: int = 0

_spawn_cooldown: float = 1
_current_cooldown: float = 0


font = pygame.font.Font(None, 25)

_level_text: pygame.Surface = font.render("Nível: x", True, "#eeeeee")
_lives_text: pygame.Surface = font.render("Vidas: x", True, "#eeeeee")
_score_text: pygame.Surface = font.render("Pontos: x", True, "#eeeeee")
update_gui()
