import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Flappy Bird")
FONT = pygame.font.SysFont("Arial", 24)

GRAVITY = 0.4
JUMP = -7
PIPE_WIDTH = 60
PIPE_GAP = 150
SPEED = 3
RADIUS = 18

CLOUD_COLORS = [(255, 255, 255), (240, 245, 250), (230, 240, 255)]
NUM_CLOUDS = 7

def spawn_clouds():
    clouds = []
    for _ in range(NUM_CLOUDS):
        x = random.randint(0, WIDTH)
        y = random.randint(20, 230)
        r = random.randint(34, 62)
        speed = random.uniform(0.4, 1.2)
        color = random.choice(CLOUD_COLORS)
        alpha = random.randint(110, 200)
        layer = random.randint(1, 3)
        clouds.append({"x": x, "y": y, "r": r, "speed": speed, "color": color, "alpha": alpha, "layer": layer})
    return clouds

def move_and_draw_clouds(clouds, win_surface):
    for cloud in clouds:
        cloud["x"] -= cloud["speed"] * (0.8 + 0.3 * cloud["layer"])
        if cloud["x"] < -cloud["r"]*2:
            cloud["x"] = WIDTH + random.randint(20, 120)
            cloud["y"] = random.randint(20, 230)
            cloud["r"] = random.randint(34, 62)
            cloud["speed"] = random.uniform(0.4, 1.2)
            cloud["color"] = random.choice(CLOUD_COLORS)
            cloud["alpha"] = random.randint(110, 200)
            cloud["layer"] = random.randint(1, 3)
        surf = pygame.Surface((cloud["r"]*2.8, cloud["r"]*1.6), pygame.SRCALPHA)
        main_color = (*cloud["color"], cloud["alpha"])
        pygame.draw.ellipse(surf, main_color, (cloud["r"]*0.4, cloud["r"]*0.55, cloud["r"]*1.3, cloud["r"]*0.8))
        pygame.draw.ellipse(surf, main_color, (cloud["r"]*1.0, cloud["r"]*0.2, cloud["r"]*0.95, cloud["r"]*0.70))
        pygame.draw.ellipse(surf, main_color, (cloud["r"]*0.0, cloud["r"]*0.1, cloud["r"]*1.1, cloud["r"]*0.7))
        pygame.draw.ellipse(surf, (*cloud["color"], min(255, cloud["alpha"]+30)), (cloud["r"]*0.68, cloud["r"]*0.94, cloud["r"]*0.8, cloud["r"]*0.4))
        win_surface.blit(surf, (cloud["x"], cloud["y"]))

def draw_pipe_column(surface, x, top_h, pipe_color, base_color, width, gap, total_height, gloss=True, shadow=True):
    border_radius = 15
    pipe_rect_top = pygame.Rect(x, 0, width, top_h)
    pipe_rect_bot = pygame.Rect(x, top_h + gap, width, total_height - top_h - gap)
    pygame.draw.rect(surface, base_color, pipe_rect_top, border_radius=border_radius)
    pygame.draw.rect(surface, base_color, pipe_rect_bot, border_radius=border_radius)
    pipe_cap_height = 16
    cap_rect_top = pygame.Rect(x-4, top_h-pipe_cap_height, width+8, pipe_cap_height)
    cap_rect_bot = pygame.Rect(x-4, top_h+gap, width+8, pipe_cap_height)
    pygame.draw.rect(surface, pipe_color, cap_rect_top, border_radius=border_radius)
    pygame.draw.rect(surface, pipe_color, cap_rect_bot, border_radius=border_radius)
    if gloss:
        gloss_w = width // 4
        gloss_h = int(top_h * 0.6)
        pygame.draw.ellipse(surface, (240,255,240), (x+6, int(top_h*0.3), gloss_w, gloss_h))
        gloss_hb = int((total_height - top_h - gap) * 0.6)
        pygame.draw.ellipse(surface, (240,255,240), (x+6, top_h+gap+int((total_height-top_h-gap)*0.3), gloss_w, gloss_hb))
    if shadow:
        pygame.draw.rect(surface, (60,100,60), (x+width-7, 3, 7, top_h-6), border_radius=11)
        pygame.draw.rect(surface, (60,100,60), (x+width-7, top_h+gap+3, 7, total_height-top_h-gap-6), border_radius=11)

def draw_bird(surface, center_x, center_y, radius):
    pygame.draw.circle(surface, (255, 220, 30), (center_x, center_y), radius)
    
    smile_radius = int(radius * 0.6)
    smile_rect = pygame.Rect(center_x - smile_radius, center_y + int(radius*0.18), 
                            smile_radius*2, int(radius*0.7))
    start_angle = 3.3  
    end_angle = 6.0    
    pygame.draw.arc(surface, (200, 90, 40), smile_rect, start_angle, end_angle, 3)
    
    eye_radius = max(2, radius // 7)
    eye_y = center_y - radius // 3
    eye_x_off = radius // 3
    pygame.draw.circle(surface, (0,0,0), (center_x - eye_x_off, eye_y), eye_radius)
    pygame.draw.circle(surface, (0,0,0), (center_x + eye_x_off, eye_y), eye_radius)
    
    beak_len = radius // 2
    beak_pts = [
        (center_x, center_y),
        (center_x + beak_len, center_y + radius // 5),
        (center_x, center_y + radius // 2)
    ]
    pygame.draw.polygon(surface, (240, 170, 0), beak_pts)

def main():
    bird_y = HEIGHT // 2
    bird_v = 0
    pipes = []
    score = 0
    alive = True
    clouds = spawn_clouds()
    clock = pygame.time.Clock()
    frame = 0
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if alive and e.key == pygame.K_SPACE:
                    bird_v = JUMP
                if not alive and e.key == pygame.K_r:
                    main()
                    return
        if alive:
            bird_v += GRAVITY
            bird_y += bird_v
            if bird_y > HEIGHT - RADIUS or bird_y < RADIUS:
                alive = False
            if frame % 80 == 0:
                h = random.randint(50, HEIGHT - PIPE_GAP - 50)
                pipes.append([WIDTH, h, False])
            for pipe in pipes:
                pipe[0] -= SPEED
            pipes = [p for p in pipes if p[0] > -PIPE_WIDTH]
            for pipe in pipes:
                bx, by = 80, int(bird_y)
                px, ph = pipe[0], pipe[1]
                if (px < bx + RADIUS < px + PIPE_WIDTH) or (px < bx - RADIUS < px + PIPE_WIDTH):
                    if by - RADIUS < ph or by + RADIUS > ph + PIPE_GAP:
                        alive = False
                if not pipe[2] and pipe[0] + PIPE_WIDTH < 80:
                    score += 1
                    pipe[2] = True
            frame += 1
        WIN.fill((133, 200, 255))
        move_and_draw_clouds(clouds, WIN)
        for pipe in pipes:
            draw_pipe_column(
                WIN,
                pipe[0],
                pipe[1],
                (0, 135, 35),
                (0, 190, 60),
                PIPE_WIDTH,
                PIPE_GAP,
                HEIGHT,
                gloss=True,
                shadow=True
            )
        draw_bird(WIN, 80, int(bird_y), RADIUS)
        srf = FONT.render("Score: " + str(score), True, (0,0,0))
        WIN.blit(srf, (10, 10))
        if not alive:
            over = FONT.render("Game Over! R to restart", True, (200, 30, 30))
            WIN.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 35))
        pygame.display.update()

main()

#Code was made by Albert Fisher.
#Don't take this seriously, I'm a begginer prorrammer :).
