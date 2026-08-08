import pygame
import random
import math
import sys

# --- Initialization ---
pygame.init()
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Santa Claus: Gift Hunt")

# --- Colors ---
RED = (210, 30, 30)
DARK_RED = (150, 20, 20)
WHITE = (255, 255, 255)
SKIN = (255, 224, 189)
GOLD = (255, 215, 0)
DARK_GOLD = (218, 165, 32)
BLACK = (20, 20, 20)

font_main = pygame.font.SysFont("Verdana", 28, bold=True)

# Effects
shake_timer = 0
particles = []

def create_particles(x, y, color):
    for _ in range(15):
        particles.append([x, y, random.uniform(-4, 4), random.uniform(-4, 4), 25, color])

def draw_santa(blink):
    global shake_timer
    off_x = random.randint(-3, 3) if shake_timer > 0 else 0
    off_y = random.randint(-3, 3) if shake_timer > 0 else 0

    # Beard
    pygame.draw.ellipse(screen, WHITE, (-50 + off_x, 220 + off_y, 600, 600))
    # Face
    pygame.draw.circle(screen, SKIN, (250 + off_x, 250 + off_y), 180)
    # Hat
    pygame.draw.polygon(screen, RED, [(50+off_x, 150+off_y), (450+off_x, 150+off_y), (250+off_x, -50+off_y)])
    pygame.draw.rect(screen, WHITE, (50+off_x, 140+off_y, 400, 40), border_radius=15)
    
    # Eyes
    if not blink:
        pygame.draw.circle(screen, BLACK, (180 + off_x, 250 + off_y), 12)
        pygame.draw.circle(screen, BLACK, (320 + off_x, 250 + off_y), 12)
    else:
        pygame.draw.line(screen, BLACK, (160+off_x, 250+off_y), (200+off_x, 250+off_y), 5)
        pygame.draw.line(screen, BLACK, (300+off_x, 250+off_y), (340+off_x, 250+off_y), 5)

    # Nose
    nose_pulse = math.sin(pygame.time.get_ticks() * 0.005) * 3
    pygame.draw.circle(screen, (255, 120, 120), (250 + off_x, 300 + off_y), int(25 + nose_pulse))

    # Mustache
    pygame.draw.ellipse(screen, (240, 240, 240), (120 + off_x, 310 + off_y, 140, 50))
    pygame.draw.ellipse(screen, (240, 240, 240), (240 + off_x, 310 + off_y, 140, 50))

def draw_gift(x, y):
    pygame.draw.rect(screen, DARK_RED, (x-22, y-18, 44, 40), border_radius=5)
    pygame.draw.rect(screen, RED, (x-22, y-22, 44, 40), border_radius=5)
    pygame.draw.rect(screen, GOLD, (x-22, y-6, 44, 8))
    pygame.draw.rect(screen, GOLD, (x-4, y-22, 8, 40))
    pygame.draw.circle(screen, DARK_GOLD, (x-8, y-25), 8, 2)
    pygame.draw.circle(screen, DARK_GOLD, (x+8, y-25), 8, 2)
    pygame.draw.circle(screen, GOLD, (x, y-22), 5)

# --- Game Settings ---
score = 0
lives = 3
game_over = False
targets = []
clock = pygame.time.Clock()

while True:
    screen.fill((20, 20, 45))
    blink = random.random() < 0.015
    if shake_timer > 0: shake_timer -= 1

    draw_santa(blink)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()
            for t in targets[:]:
                if math.hypot(mx - t[0], my - t[1]) < 45:
                    create_particles(t[0], t[1], GOLD)
                    targets.remove(t)
                    score += 1
                    shake_timer = 7

        if event.type == pygame.KEYDOWN and game_over:
            score, lives, game_over, targets = 0, 3, False, []

    if not game_over:
        if random.random() < 0.04:
            targets.append([random.randint(60, WIDTH-60), -60, random.uniform(4, 7)])
        
        for t in targets[:]:
            t[1] += t[2]
            draw_gift(t[0], t[1])
            
            if t[1] > HEIGHT:
                targets.remove(t)
                lives -= 1
                if lives <= 0: game_over = True

    # Particles
    for p in particles[:]:
        p[0] += p[2]; p[1] += p[3]; p[4] -= 1
        if p[4] > 0:
            pygame.draw.rect(screen, p[5], (int(p[0]), int(p[1]), p[4]//3, p[4]//3))
        else:
            particles.remove(p)

    # Interface
    score_t = font_main.render(f"SCORE: {score}", True, BLACK)
    lives_t = font_main.render(f"LIVES: {lives}", True, RED)
    screen.blit(score_t, (25, 25))
    screen.blit(lives_t, (WIDTH - 180, 25))

    # Crosshair
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(screen, RED, (mx, my), 25, 2)
    pygame.draw.circle(screen, RED, (mx, my), 2)

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        final_t = font_main.render(f"FINAL SCORE: {score}", True, GOLD)
        restart_t = font_main.render("PRESS ANY KEY", True, WHITE)
        screen.blit(final_t, (WIDTH//2 - 110, HEIGHT//2 - 20))
        screen.blit(restart_t, (WIDTH//2 - 150, HEIGHT//2 + 40))

    pygame.display.flip()
    clock.tick(60)
