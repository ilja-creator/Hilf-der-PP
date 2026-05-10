# menu\main.py

import pygame
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import additional

def menu(state):
    pygame.init()

    # get screen width & height
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h

    # loading images
    icon = pygame.image.load(additional.resource_path("resources/images/pp-icon.png"))
    bg_p = pygame.image.load(additional.resource_path("resources/images/pp-bg-title.png"))
    chase_img = pygame.image.load(additional.resource_path("resources/images/pp-chase.png"))

    # Scale bg
    def scale(picture):
        img_w, img_h = picture.get_width(), picture.get_height()
        screen_ratio = width / height
        img_ratio = img_w / img_h
        if img_ratio > screen_ratio:
            new_h = height
            new_w = int(height * img_ratio)
        else:
            new_w = width
            new_h = int(width / img_ratio)
        n_bg = pygame.transform.scale(picture, (new_w, new_h))
        return n_bg
    bg = scale(bg_p)

    # create screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Hilf der Paw Patrol!')
    pygame.display.set_icon(icon)

    # PLAY
    font_path = additional.resource_path("resources/fonts/LuckiestGuy/LuckiestGuy-Regular.ttf")
    font = pygame.font.Font(font_path, 150)
    play_text = font.render("PLAY", True, (255, 255, 255))
    button_rect = pygame.Rect(0, 0, 400, 150)
    button_rect.center = (width//2, height//3)
    play_rect = play_text.get_rect(center=button_rect.center)
    play_rect.y += 15

    # Chase
    chase_scaled = pygame.transform.scale(chase_img, (chase_img.get_width()//2, chase_img.get_height()//2))
    chase_rect = chase_scaled.get_rect()
    chase_rect.center = (width // 2, height // 2)

    overlay = pygame.Surface((chase_rect.width, chase_rect.height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 0))
    pygame.draw.rect(overlay, (128, 128, 128, 150), overlay.get_rect(), border_radius=20)

    def menu_start():
        bg_2 = pygame.image.load(additional.resource_path("resources/images/pp-bg-tower.png"))
        n_bg = scale(bg_2)
        n_state = "menu"
        n_chase = True
        return n_bg, n_state, n_chase

    # main loop
    chase = False
    running = True

    if state == "menu":
        bg, state, chase = menu_start()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_ALT and not state == "chase":
                    running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos):
                    bg, state, chase = menu_start()
                elif chase_rect.collidepoint(event.pos) and chase:
                    pygame.quit()
                    return "chase"

        # DRAWING
        screen.blit(bg, (0, 0))
        if state == "title":
            pygame.draw.rect(screen, (0,0,0), button_rect, border_radius=20)
            screen.blit(play_text, play_rect)
        if chase:
            screen.blit(overlay, chase_rect)
            screen.blit(chase_scaled, chase_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu(state="title")