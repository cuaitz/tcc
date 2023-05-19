import json

import pygame
import keyboard

from .. import const
from .. import core
from . import state
from . import playing


class GameOverState(state.GameState):
    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                with open("data.json", "r") as file:
                    data = json.load(file)
                
                with open("data.json", "w") as file:
                    data.append(playing.get_score())
                    json.dump(data, file, indent=4)
                    
                core.pop_state()
                playing.restart_game()

    def update(self, delta_time_seconds: float):
        update_gui()
        #keyboard.press_and_release('r')
    
    def render(self, surface: pygame.Surface):
        surface.fill("#181818")
        surface.fill("#232323", const.GAME_AREA_RECT)
        
        texts = [_gameover_text, _level_text, _score_text, _continue_text]
        height = 50
        for text in texts:
            surface.blit(text, (const.GAME_AREA_RECT.centerx - text.get_width() / 2, height))
            height += 5 + text.get_height()

def update_gui():
    global _level_text
    global _score_text
    
    _level_text = font_normal.render(f"Nível: {playing._level}", True, "#eeeeee")
    _score_text = font_normal.render(f"Pontuação: {playing._score}", True, "#eeeeee")


font_big = pygame.font.Font(None, 50)
font_normal = pygame.font.Font(None, 25)

_gameover_text = font_big.render("Fim de Jogo!", True, "#eeeeee")
_level_text = font_normal.render(f"Nível: x", True, "#eeeeee")
_score_text = font_normal.render(f"Pontuação: x", True, "#eeeeee")
_continue_text = font_normal.render("Pressione \"R\" para jogar novamente", True, "#eeeeee")
