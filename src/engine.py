import pygame

__WINDOW_SIZE: tuple[int, int] = (800, 600)
__TARGET_FPS: int = 60
__OVER: bool = False

__display = pygame.display.set_mode(__WINDOW_SIZE)
__clock = pygame.time.Clock()

pygame.display.set_icon(pygame.Surface((0, 0)))
pygame.display.set_caption(f"FPS: {round(__clock.get_fps(), 2)}")

def update(delta_time_seconds: float):
    pygame.display.set_caption(f"FPS: {round(__clock.get_fps(), 2)}")

def render(surface: pygame.Surface):
    surface.fill("#232323")

def loop():
    while not __OVER:
        delta_time_seconds: int = __clock.tick(__TARGET_FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


        update(delta_time_seconds)
        render(__display)
        pygame.display.update()
        