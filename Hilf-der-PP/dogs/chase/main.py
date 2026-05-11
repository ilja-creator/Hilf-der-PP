import pygame, random, os
from pathlib import Path

def chase():
    def resource_path(relative_path):
        base_path = Path(__file__).parent.parent.parent
        return str(base_path / relative_path)

    pygame.init()

    pygame.display.set_caption("Hilf Chase!")
    pygame.display.set_icon(pygame.image.load(resource_path("resources/images/pp-chase-icon.png")))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()

    bg = pygame.image.load(resource_path("resources/images/pp-bg-city.png"))
    bg = pygame.transform.scale(bg, (width, height))

    holes = [
        (int(width * 0.11), int(height * 0.7)),  # 2 links mitte
        (int(width * 0.19), int(height * 0.78)),  # 3 links unten
        (int(width * 0.36), int(height * 0.70)),  # 5 mitte links
        (int(width * 0.4), int(height * 0.17)),  # 6 oben mitte
        (int(width * 0.58), int(height * 0.71)),  # 7 mitte rechts
        (int(width * 0.62), int(height * 0.65)),  # 8 mitte rechts oben
        (int(width * 0.61), int(height * 0.42)),  # 9 mitte rechts hoch
        (int(width * 0.94), int(height * 0.72))  # 12 ganz rechts
    ]

    hole_r = 60
    cat_show_time = 1.2 * 1000
    game_duration = 30 * 1000

    cat_imgs = []
    cats_path = Path(__file__).parent.parent.parent / "resources/images/cats"
    cat_files = sorted([f for f in os.listdir(cats_path) if f.endswith(".png")])
    for f in cat_files:
        img = pygame.image.load(str(cats_path / f))
        img = pygame.transform.scale(img, (hole_r * 2, hole_r * 2))
        cat_imgs.append(img)

    font = pygame.font.SysFont("Arial", 40)
    big_font = pygame.font.SysFont("Arial", 80)

    score = 0
    active_hole = None
    active_cat = None
    cat_timer = 0

    waiting = True
    while waiting:
        screen.blit(bg, (0, 0))
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        start_text = big_font.render("Hilf Chase! indem du die Katzen fängst!", True, (255, 255, 255))
        sub_text = font.render("Drücke ENTER um zu starten!", True, (255, 255, 255))

        screen.blit(start_text, start_text.get_rect(center=(width//2, height//2 - 50)))
        screen.blit(sub_text, sub_text.get_rect(center=(width//2, height//2 + 50)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                        waiting = False
                if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_ALT:
                    pygame.quit()
                    return False

    start_ticks = pygame.time.get_ticks()
    next_cat_time = start_ticks + random.randint(500, 1500)

    running = True
    while running:
        try:
            now = pygame.time.get_ticks()
            remaining = max(0, game_duration - (now - start_ticks))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_ALT:
                        pygame.quit()
                        return False

                if event.type == pygame.MOUSEBUTTONUP and remaining > 0:

                    if active_hole is not None:
                        hx, hy = holes[active_hole]
                        dx = event.pos[0] - hx
                        dy = event.pos[1] - hy
                        if dx*dx + dy*dy <= hole_r ** 2:
                            score += 1
                            active_hole = None
                            active_cat = None
                            next_cat_time = now + random.randint(500, 1500)

            if active_hole is None and now >= next_cat_time and remaining > 0:
                active_hole = random.randint(0, len(holes) - 1)
                active_cat = random.randint(0, len(cat_imgs) - 1)
                cat_timer = now

            if active_hole is not None and now - cat_timer > cat_show_time:
                active_hole = None
                active_cat = None
                next_cat_time = now + random.randint(500, 1500)

            screen.blit(bg, (0, 0))

            #for hx, hy in holes:
               #pygame.draw.circle(screen, (60, 40, 20), (hx, hy), hole_r)

            if active_hole is not None:
                hx, hy = holes[active_hole]
                img = cat_imgs[active_cat]
                screen.blit(img, img.get_rect(center=(hx, hy)))

            score_text = font.render(f"Punkte: {score}", True, (0, 0, 0))
            timer_text = font.render(f"Zeit: {remaining // 1000 + 1}s", True, (0, 0, 0))
            screen.blit(score_text, (20, 20))
            screen.blit(timer_text, (width - 200, 20))

            if remaining == 0:
                overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                end_text = big_font.render(f"Punkte: {score}", True, (255, 255, 255))
                sub_text = font.render("Drücke ENTER um zurückzukehren", True, (200, 200, 200))
                screen.blit(end_text, end_text.get_rect(center=(width // 2, height // 2 - 50)))
                screen.blit(sub_text, sub_text.get_rect(center=(width // 2, height // 2 + 50)))

                pygame.display.flip()

                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return True
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            pygame.quit()
                            return True
                return True
            pygame.display.flip()

        except Exception as e:
            print(f"Fehler: {e}")
            import traceback
            traceback.print_exc()
            running = False

if __name__ == '__main__':
    chase()