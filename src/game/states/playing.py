import math
import random
import time

import pygame

from .. import const
from .. import core

from . import state


class PlayingState(state.GameState):
    def __init__(self):
        self.game_surface: pygame.Surface = pygame.Surface(const.GAME_AREA_RECT.size)
        self.game_surface_rect: pygame.Rect = self.game_surface.get_rect()
    
    def process_event(self, event: pygame.event.Event):
        global _score
        global _alive_targets
        global _dead_targets
        global _clicks
        global _hits
        global _hits_accuracy
        global _precision
        global _accuracy
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                _clicks += 1
                _precision = _hits / _clicks
                for target in _alive_targets:
                    click_position = (
                        event.pos[0] - const.GAME_AREA_RECT.left,
                        event.pos[1] - const.GAME_AREA_RECT.top
                    )
                    target_center = target.position
                    target_radius = target.radius
                    
                    distance = math.dist(click_position, target_center)
                    
                    if distance <= target_radius:
                        target.disable(True, click_position)
                        _alive_targets.remove(target)
                        _dead_targets.append(target)
                        _score += 1 * _level
                        _hits += 1
                        
                        normalized_distance = 1 - distance / _radius
                        _hits_accuracy.append(normalized_distance)
                        
                        _accuracy = sum(_hits_accuracy) / len(_hits_accuracy)
                        _precision = _hits / _clicks

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                spawn_target()
            elif event.key == pygame.K_a:
                decrease_level()
            elif event.key == pygame.K_d:
                increase_level()
        
    def update(self, delta_time_seconds: float):
        global _alive_targets
        global _dead_targets
        global _current_cooldown
        global _lives
        global _started_run
        global _start_time
        global _last_data_gather
        
        if not _started_run:
            _started_run = True
            _start_time = time.time()
        
        _current_cooldown -= delta_time_seconds / const.TARGET_FPS
        
        if time.time() - _last_data_gather >= 1:
            _run_data.append(get_game_data())
            _last_data_gather = time.time()
        
        if _current_cooldown <= 0:
            spawn_target()
            _current_cooldown = _spawn_cooldown * get_cooldown_multiplier()
        
        for target in _alive_targets:
            if not self.game_surface_rect.collidepoint(target.position.x, target.position.y - target.radius):
                target.disable(False)
                _alive_targets.remove(target)
                _dead_targets.append(target)
                _lives -= 1
                if _lives <= 0:
                    _run_data.insert(0, get_game_data(complete=True))
                    core.push_state('gameover')
            
            target.position += target.speed * delta_time_seconds * get_speed_multiplier()
        
        update_gui()

    def render(self, surface: pygame.Surface):
        surface.fill("#181818")
        self.game_surface.fill("#232323")
        
        for target in _alive_targets:
            pygame.draw.circle(self.game_surface, target.color, target.position, target.radius)
        
        surface.blit(self.game_surface, const.GAME_AREA_RECT.topleft)
        
        texts = [_level_text, _lives_text, _score_text, _clicks_text, _hits_text, _precision_text, _accuracy_text]
        height = 5
        for text in texts:
            surface.blit(text, (5, height))
            height += 5 + text.get_height()
            
            if text in [_score_text, _hits_text]:
                height += 10


class Target:
    def __init__(self, radius: int, position: pygame.Vector2):
        self.radius: int = radius
        self.position: pygame.Vector2 = position
        self.kill_hit_position: tuple[int, int] = (0, 0)
        self.killed: bool = False
        
        self.color: str = "#c42323"
        self.speed: pygame.Vector2 = pygame.Vector2(0, 1)
        self.time_born = time.time()
        self.time_alive = 0
    
    def disable(self, killed: bool, click: tuple[int, int]=(0, 0)):
        if killed:
            assert math.dist(click, self.position) <= self.radius
        
            self.killed = True
            self.kill_hit_position = click
        self.time_alive = time.time() - self.time_born
    
    def to_dict(self) -> dict:
        return {
            'final_position': (int(self.position.x), int(self.position.y)),
            'time_alive': self.time_alive,
            'killed': self.killed,
            'kill_hit_position': self.kill_hit_position,
            'hit_accuracy': 0 if not self.killed else 1 - math.dist(self.position, self.kill_hit_position) / self.radius
        }


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
    global _alive_targets
    global _dead_targets
    global _level
    global _lives
    global _total_targets_spawned
    global _current_cooldown
    global _score
    global _clicks
    global _hits
    global _hits_accuracy
    global _precision
    global _accuracy
    global _started_run
    global _run_data
    
    _alive_targets = []
    _dead_targets = []
    _level = 1
    _lives = 3
    _total_targets_spawned= 0
    _current_cooldown = 0
    _score = 0
    _clicks = 0
    _hits = 0
    _hits_accuracy = []
    _precision = 0
    _accuracy = 0
    _started_run = False
    _run_data = []
    
    update_gui()

def spawn_target():
    global _alive_targets
    global _total_targets_spawned
    
    position = (
        random.randint(
            _radius,
            const.GAME_AREA_RECT.width - _radius
        ), 
        _radius
    )
    
    _alive_targets.append(Target(_radius, pygame.Vector2(position)))
    _total_targets_spawned += 1
    
    if _total_targets_spawned % _targets_per_level == 0:
        increase_level()

def update_gui():
    global _level_text
    global _lives_text
    global _score_text
    global _precision_text
    global _clicks_text
    global _hits_text
    global _accuracy_text
    
    _level_text = font.render(f"Nível: {_level}", True, "#eeeeee")
    _lives_text = font.render(f"Vidas: {_lives}", True, "#eeeeee")
    _score_text = font.render(f"Pontos: {_score}", True, "#eeeeee")
    _clicks_text = font.render(f"Cliques: {_clicks}", True, "#eeeeee")
    _hits_text = font.render(f"Acertos: {_hits}", True, "#eeeeee")
    _precision_text = font.render(f"Precisão: {round(_precision * 100, 2)}%", True, "#eeeeee")
    _accuracy_text = font.render(f"Exatidão: {round(_accuracy * 100, 2)}%", True, "#eeeeee")

def get_game_data(complete=False):
    if complete:
        return {
            'dead_targets': [target.to_dict() for target in _dead_targets],

            'level': _level,
            'lives': _lives,
            'radius': _radius,
            'total_targets_spawned': _total_targets_spawned,
            'targets_per_level': _targets_per_level,
            'score': _score,
            'clicks': _clicks,
            'hits': _hits,
            'precision': _precision,
            'accuracy': _accuracy,
            'spawn_cooldown': _spawn_cooldown,
            'current_cooldown': _current_cooldown,
            'game_time': time.time() - _start_time,
        }
    else:
        return {
            'level': _level,
            'lives': _lives,
            'total_targets_spawned': _total_targets_spawned,
            'score': _score,
            'clicks': _clicks,
            'hits': _hits,
            'precision': _precision,
            'accuracy': _accuracy,
            'current_cooldown': _current_cooldown,
            'game_time': time.time() - _start_time,
        }

_dead_targets: list[Target] = []
_alive_targets: list[Target] = []

_level: int = 1
_lives: int = 3
_radius: int = 15
_total_targets_spawned: int = 0
_targets_per_level: int = 10
_score: int = 0

_clicks: int = 0
_hits: int = 0
_hits_accuracy: list[float] = []
_precision: int = 0
_accuracy: int = 0

_spawn_cooldown: float = 1
_current_cooldown: float = 0

_started_run: bool = False
_start_time: float = 0
_last_data_gather: float = 0
_run_data: list[dict] = []


font = pygame.font.Font(None, 25)

_level_text: pygame.Surface = font.render("Nível: x", True, "#eeeeee")
_lives_text: pygame.Surface = font.render("Vidas: x", True, "#eeeeee")
_score_text: pygame.Surface = font.render("Pontos: x", True, "#eeeeee")
_clicks_text: pygame.Surface = font.render("Cliques: x", True, "#eeeeee")
_hits_text: pygame.Surface = font.render("Acertos: x", True, "#eeeeee")
_precision_text: pygame.Surface = font.render("Precisão: x", True, "#eeeeee")
_accuracy_text: pygame.Surface = font.render("Exatidão: x", True, "#eeeeee")
update_gui()
