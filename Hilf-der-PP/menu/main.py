# menu\main.py

import pygame
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import additional

def menu(state):
    def draw_text_with_outline(surface, text, text_font, center_pos, color, outline_color=(0, 0, 0)):
        main = text_font.render(text, True, color)
        rect = main.get_rect(center=center_pos)

        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)]

        for ox, oy in offsets:
            outline = text_font.render(text, True, outline_color)
            surface.blit(outline, (rect.x + ox, rect.y + oy))

        surface.blit(main, rect)

    pygame.init()

    # get screen width & height
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h

    # loading images
    icon = pygame.image.load(additional.resource_path("resources/images/pp-icon.png"))
    bg_p = pygame.image.load(additional.resource_path("resources/images/pp-bg-title.png"))
    chase_img = pygame.image.load(additional.resource_path("resources/images/pp-chase.png"))
    skye_img = pygame.image.load(additional.resource_path("resources/images/pp-skye.png"))

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
    button_rect.center = (width//2, int(height * 3//7))
    play_rect = play_text.get_rect(center=button_rect.center)
    play_rect.y += 15

    dog_size = (400, 400)

    # Chase
    chase_scaled = pygame.transform.scale(chase_img, dog_size)
    chase_rect = chase_scaled.get_rect()
    chase_rect.center = (width * 2//3, height // 2)
    overlay_chase = pygame.Surface((chase_rect.width, chase_rect.height), pygame.SRCALPHA)
    overlay_chase.fill((0, 0, 0, 0))
    pygame.draw.rect(overlay_chase, (128, 128, 128, 150), overlay_chase.get_rect(), border_radius=20)

    skye_scaled = pygame.transform.scale(skye_img, dog_size)
    skye_rect = skye_scaled.get_rect()
    skye_rect.center = (width * 1//3, height // 2)
    overlay_skye = pygame.Surface((skye_rect.width, skye_rect.height), pygame.SRCALPHA)
    overlay_skye.fill((0, 0, 0, 0))
    pygame.draw.rect(overlay_skye, (128, 128, 128, 150), overlay_skye.get_rect(), border_radius=20)
    pygame.draw.rect(overlay_skye, (128, 128, 128, 150), overlay_skye.get_rect(), border_radius=20)

    def menu_start():
        bg_2 = pygame.image.load(additional.resource_path("resources/images/pp-bg-tower.png"))
        n_bg = scale(bg_2)
        n_state = "menu"
        n_show_dogs = True
        return n_bg, n_state, n_show_dogs

    # main loop
    show_dogs = False
    running = True

    if state == "menu":
        bg, state, show_dogs = menu_start()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_ALT and not state == "chase":
                    running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if button_rect.collidepoint(event.pos):
                    bg, state, show_dogs = menu_start()
                elif show_dogs:
                    if chase_rect.collidepoint(event.pos):
                        pygame.quit()
                        return "chase"
                    if skye_rect.collidepoint(event.pos):
                        pygame.quit()
                        return "skye"

        # DRAWING
        screen.blit(bg, (0, 0))
        if state == "title":
            pygame.draw.rect(screen, (0,0,0), button_rect, border_radius=20)
            screen.blit(play_text, play_rect)
            draw_text_with_outline(
                screen,
                "HILF DER PAW PATROL!",
                font,
                (width // 2, int(height * 1//5)),
                (0, 100, 200),
                (0, 0, 0)
            )
        if show_dogs:
            screen.blit(overlay_chase, chase_rect)
            screen.blit(chase_scaled, chase_rect)

            screen.blit(overlay_skye, skye_rect)
            screen.blit(skye_scaled, skye_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    menu(state="title")