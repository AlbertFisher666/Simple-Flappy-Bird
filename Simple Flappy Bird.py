import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Flappy Bird")
FONT = pygame.font.SysFont("Arial", 24)

GRAVITY = 0.5
JUMP = -7
PIPE_WIDTH = 60
PIPE_GAP = 150
SPEED = 3
RADIUS = 18

def main():
    bird_y = HEIGHT // 2
    bird_v = 0
    pipes = []
    score = 0
    alive = True

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
                if px < bx + RADIUS < px + PIPE_WIDTH or px < bx - RADIUS < px + PIPE_WIDTH:
                    if by - RADIUS < ph or by + RADIUS > ph + PIPE_GAP:
                        alive = False
                if not pipe[2] and pipe[0] + PIPE_WIDTH < 80:
                    score += 1
                    pipe[2] = True
            frame += 1

        WIN.fill((133, 200, 255))
        for pipe in pipes:
            pygame.draw.rect(WIN, (0, 180, 40), (pipe[0], 0, PIPE_WIDTH, pipe[1]))
            pygame.draw.rect(WIN, (0, 180, 40), (pipe[0], pipe[1] + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe[1] - PIPE_GAP))
        pygame.draw.circle(WIN, (255, 220, 30), (80, int(bird_y)), RADIUS)
        srf = FONT.render("Score: " + str(score), True, (0,0,0))
        WIN.blit(srf, (10, 10))

        if not alive:
            over = FONT.render("Game Over! R to restart", True, (200, 30, 30))
            WIN.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 35))
        pygame.display.update()

main()

#This code was written by Albert Fisher.
#Don't take this seriously, I'm a beginner programmer :).