import pygame, random
from pathlib import Path

def skye():
    def resource_path(relative_path):
        base_path = Path(__file__).parent.parent.parent
        return str(base_path / relative_path)
    def round_to_speed(y, speed):
        return round(y / speed) * speed

    pygame.init()

    pygame.display.set_caption("Hilf Skye!")
    pygame.display.set_icon(pygame.image.load(resource_path("resources/images/pp-skye-icon.png")))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()

    bg = pygame.image.load(resource_path("resources/images/pp-bg-skye.png"))
    bg = pygame.transform.scale(bg, (width, height))

    gull_img = pygame.image.load(resource_path("resources/images/pp-gull.png"))
    orig_w, orig_h = gull_img.get_size()
    gull_img = pygame.transform.scale(gull_img, (int(orig_w // 6), int(orig_h // 6)))

    skye_img = pygame.image.load(resource_path("resources/images/pp-skye-flying.png"))
    orig_w, orig_h = skye_img.get_size()
    skye_img = pygame.transform.scale(skye_img, (int(orig_w // 6), int(orig_h // 6)))

    font = pygame.font.SysFont("Arial", 40)
    big_font = pygame.font.SysFont("Arial", 80)

    number_gulls = 3

    gulls = [None] * number_gulls
    skye_pos = None
    skye_speed = 3
    target = None

    caught = False
    game_duration = 30 * 1000

    waiting = True
    while waiting:
        screen.blit(bg, (0, 0))
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        start_text = big_font.render("Hilf Skye! indem du sie sicher zur Zentrale bringst!", True, (255, 255, 255))
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

    running = True
    start_ticks = pygame.time.get_ticks()
    next_gull_times = [
        start_ticks + random.randint(300, 2500),
        start_ticks + random.randint(1800, 4200),
        start_ticks + random.randint(3500, 6500),
        start_ticks + random.randint(5500, 9000)
    ]

    gull_timers = [None] * number_gulls

    while running:
        try:
            now = pygame.time.get_ticks()
            remaining = max(0, game_duration - (now - start_ticks))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_ALT:
                        pygame.quit()
                        return False
                elif skye_pos is not None:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        target = round_to_speed(int(event.pos[1]), skye_speed)

                """if event.type == pygame.MOUSEBUTTONUP and remaining > 0:
                    if active_gull_1 is not None:
                        gx, gy = active_gull_1[0], active_gull_1[1]
                        dx = event.pos[0] - gx
                        dy = event.pos[1] - gy
                        if dx*dx + dy*dy <= gull_img ** 2:
                            caught = True
                            remaining = 0
                            """

            screen.blit(bg, (0, 0))

            if remaining > 0:
                if skye_pos is None:
                    skye_pos = [80, height // 2]
                    target = int(skye_pos[1])
                elif skye_pos is not None:
                    if skye_pos[1] < target:
                        skye_pos[1] += skye_speed
                    elif skye_pos[1] > target:
                        skye_pos[1] -= skye_speed

                for i in range(len(gulls)):
                    if gulls[i] is None and now >= next_gull_times[i]:
                        gulls[i] = [width * 9//10, random.randint(50, height - 50)]
                        gull_timers[i] = now
                    elif gulls[i] is not None:
                        if gulls[i][0] <= 10:
                            gulls[i] = None
                            gull_timers[i] = now
                            next_gull_times[i] += random.randint(int(0.5 * 1000), int(5 * 1000))
                        else:
                            gulls[i][0] -= 1
                    if skye_pos is not None and skye is not None and gulls[i] is not None:
                        if skye_img.get_rect(center=(skye_pos[0], skye_pos[1])).colliderect(
                                gull_img.get_rect(center=(gulls[i][0], gulls[i][1]))):
                            caught = True
                            remaining = 0

            for i in range(len(gulls)):
                if gulls[i] is not None:
                    gx, gy = gulls[i][0], gulls[i][1]
                    img = gull_img
                    screen.blit(img, img.get_rect(center=(gx, gy)))

            if skye_pos is not None:
                sx, sy = skye_pos
                img = skye_img
                screen.blit(img, img.get_rect(center=(sx, sy)))

            timer_text = font.render(f"Zeit: {remaining // 1000 + 1}s", True, (0, 0, 0))
            screen.blit(timer_text, (20, 20))

            if remaining == 0:
                overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))

                if caught:
                    end_text = big_font.render("Leider hat Skye es nicht bis zur Zentrale geschafft.", True, (255, 255, 255))
                    sub_text = font.render("Drücke ENTER um es erneut zu probieren! Oder ALT+ENTER um zurückzukehren!", True, (255, 255, 255))
                else:
                    end_text = big_font.render("Super! Skye hat es sicher bis zur Zentrale geschafft!", True, (200, 200, 200))
                    sub_text = font.render("Drücke ENTER um zurückzukehren!", True, (200, 200, 200))
                screen.blit(end_text, end_text.get_rect(center=(width // 2, height / 2 - 50)))
                screen.blit(sub_text, sub_text.get_rect(center=(width // 2, height / 2 + 50)))

                pygame.display.flip()

                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return False
                        if event.type == pygame.KEYDOWN:
                            if caught:
                                if event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                                    pygame.quit()
                                    return True
                                elif event.key == pygame.K_RETURN:
                                    skye()
                            else:
                                if event.key == pygame.K_RETURN:
                                    pygame.quit()
                                    return True
            pygame.display.flip()

        except Exception as e:
            print(f"Fehler: {e}")
            import traceback
            traceback.print_exc()
            running = False

if __name__ == '__main__':
    skye()