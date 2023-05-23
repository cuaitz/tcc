import json
import os

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
                core.pop_state()
                #collect_data()
                playing.restart_game()

    def update(self, delta_time_seconds: float):
        update_gui()
        #keyboard.press_and_release('r')
    
    def render(self, surface: pygame.Surface):
        surface.fill("#181818")
        surface.fill("#232323", const.GAME_AREA_RECT)
        
        texts = [
            _gameover_text,
            _level_text,
            _score_text,
            _clicks_text,
            _hits_text,
            _precision_text,
            _accuracy_text,
            _playtime_text
        ]
        
        height = 50
        for text in texts:
            surface.blit(text, (const.GAME_AREA_RECT.centerx - text.get_width() / 2, height))
            height += 5 + text.get_height()
        
        surface.blit(_continue_text, (const.GAME_AREA_RECT.centerx - _continue_text.get_width() / 2, height + 10))

def update_gui():
    global _level_text
    global _score_text
    global _clicks_text
    global _hits_text
    global _precision_text
    global _accuracy_text
    global _playtime_text
    
    _level_text = font_normal.render(f"Nível: {playing._level}", True, "#eeeeee")
    _score_text = font_normal.render(f"Pontos: {playing._score}", True, "#eeeeee")
    _clicks_text = font_normal.render(f"Cliques: {playing._clicks}", True, "#eeeeee")
    _hits_text = font_normal.render(f"Acertos: {playing._hits}", True, "#eeeeee")
    _precision_text = font_normal.render(f"Precisão: {round(playing._precision * 100, 2)}%", True, "#eeeeee")
    _accuracy_text = font_normal.render(f"Exatidão: {round(playing._accuracy * 100, 2)}%", True, "#eeeeee")
    _playtime_text = font_normal.render(f"Tempo de jogo: {round(playing._end_time - playing._start_time, 2)}s", True, "#eeeeee")

def collect_data():
    uid = 0
    
    filename = f"data\\base\\data{uid}.json"
    
    while os.path.exists(filename):
        uid += 1
        filename = f"data\\base\\data{uid}.json"
        
        assert uid < 10  # Crasha dps da 10th partida
    
    with open(filename, 'w+') as file:
        json.dump(playing._run_data, file, indent=4)

font_big = pygame.font.Font(None, 50)
font_normal = pygame.font.Font(None, 25)

_gameover_text = font_big.render("Fim de Jogo!", True, "#eeeeee")
_level_text = font_normal.render(f"Nível: x", True, "#eeeeee")
_score_text = font_normal.render(f"Pontuação: x", True, "#eeeeee")
_clicks_text: pygame.Surface = font_normal.render("Cliques: x", True, "#eeeeee")
_hits_text: pygame.Surface = font_normal.render("Acertos: x", True, "#eeeeee")
_precision_text: pygame.Surface = font_normal.render("Precisão: x", True, "#eeeeee")
_accuracy_text: pygame.Surface = font_normal.render("Exatidão: x", True, "#eeeeee")
_playtime_text: pygame.Surface = font_normal.render("Tempo de jogo: xs", True, "#eeeeee")
_continue_text = font_normal.render("Pressione \"R\" para jogar novamente", True, "#eeeeee")
