import random
import sys
import pygame
pygame.init()
WIDTH, HEIGHT = 980, 360
GROUND_Y = 290
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner - Polished Edition")
clock = pygame.time.Clock()
title_font = pygame.font.SysFont("arial", 60, bold=True)
font = pygame.font.SysFont("arial", 30, bold=True)
small_font = pygame.font.SysFont("arial", 22)

SKY_TOP = (160, 215, 255)
SKY_BOTTOM = (236, 247, 255)
SUN = (255, 214, 112)
MOUNTAIN_DARK = (130, 150, 165)
MOUNTAIN_LIGHT = (170, 188, 200)
GROUND_COLOR = (75, 75, 75)
TRACK_COLOR = (95, 95, 95)
WHITE = (255, 255, 255)
BLACK = (12, 12, 12)
GREEN = (44, 149, 72)
RED = (198, 69, 69)
HUD_BG = (255, 255, 255, 170)

def vertical_gradient(surface, top_color, bottom_color):
    """Draw a soft sky gradient."""
    for y in range(HEIGHT):
        blend = y / HEIGHT
        color = (
            int(top_color[0] + (bottom_color[0] - top_color[0]) * blend),
            int(top_color[1] + (bottom_color[1] - top_color[1]) * blend),
            int(top_color[2] + (bottom_color[2] - top_color[2]) * blend),
        )
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))

class Dino:
    def __init__(self):
        self.x = 120
        self.base_y = GROUND_Y - 74
        self.y = self.base_y
        self.vy = 0.0
        self.gravity = 0.82
        self.jump_strength = -16.3
        self.jumping = False
        self.ducking = False
        self.run_frame = 0

    def update(self, keys):
        if not self.jumping and keys[pygame.K_SPACE]:
            self.vy = self.jump_strength
            self.jumping = True

        self.ducking = keys[pygame.K_DOWN] and not self.jumping

        if self.jumping:
            self.y += self.vy
            self.vy += self.gravity
            if self.y >= self.base_y:
                self.y = self.base_y
                self.vy = 0
                self.jumping = False
        else:
            self.run_frame = (self.run_frame + 1) % 24

    def hitbox(self):
        if self.ducking:
            return pygame.Rect(self.x + 8, self.y + 34, 75, 33)
        return pygame.Rect(self.x + 10, self.y + 8, 62, 64)

    def draw(self, surf):
        # Shadow
        shadow_w = 56 if not self.ducking else 66
        pygame.draw.ellipse(surf, (40, 40, 40), (self.x + 8, GROUND_Y - 7, shadow_w, 8))

        if self.ducking:
            body = pygame.Rect(self.x + 14, self.y + 40, 48, 20)
            neck = pygame.Rect(self.x + 58, self.y + 34, 11, 14)
            head = pygame.Rect(self.x + 65, self.y + 30, 18, 15)
            tail = [(self.x + 10, self.y + 45), (self.x + 0, self.y + 51), (self.x + 10, self.y + 54)]
            pygame.draw.rect(surf, BLACK, body, border_radius=6)
            pygame.draw.rect(surf, BLACK, neck, border_radius=3)
            pygame.draw.rect(surf, BLACK, head, border_radius=4)
            pygame.draw.polygon(surf, BLACK, tail)
            pygame.draw.circle(surf, WHITE, (self.x + 76, self.y + 36), 2)
        else:
            body = pygame.Rect(self.x + 18, self.y + 23, 36, 35)
            neck = pygame.Rect(self.x + 46, self.y + 10, 11, 20)
            head = pygame.Rect(self.x + 52, self.y + 3, 20, 16)
            arm = pygame.Rect(self.x + 34, self.y + 33, 9, 14)
            tail = [(self.x + 18, self.y + 32), (self.x + 4, self.y + 39), (self.x + 18, self.y + 44)]
            leg_y = self.y + 58

            leg_a_low = self.run_frame < 12
            leg1 = pygame.Rect(self.x + 24, leg_y + (0 if leg_a_low else 3), 9, 13 if leg_a_low else 10)
            leg2 = pygame.Rect(self.x + 40, leg_y + (3 if leg_a_low else 0), 9, 10 if leg_a_low else 13)

            pygame.draw.rect(surf, BLACK, body, border_radius=7)
            pygame.draw.rect(surf, BLACK, neck, border_radius=4)
            pygame.draw.rect(surf, BLACK, head, border_radius=4)
            pygame.draw.rect(surf, BLACK, arm, border_radius=4)
            pygame.draw.polygon(surf, BLACK, tail)
            pygame.draw.rect(surf, BLACK, leg1, border_radius=3)
            pygame.draw.rect(surf, BLACK, leg2, border_radius=3)
            pygame.draw.circle(surf, WHITE, (self.x + 66, self.y + 10), 2)

class Obstacle:
    def __init__(self, speed):
        self.x = WIDTH + random.randint(30, 120)
        self.speed = speed
        self.kind = random.choice(["cactus", "bird"])
        if self.kind == "cactus":
            self.w = random.choice([24, 30, 36])
            self.h = random.choice([48, 58, 68])
            self.y = GROUND_Y - self.h
        else:
            self.w = 46
            self.h = 27
            self.y = random.choice([205, 220])

    def update(self, speed):
        self.speed = speed
        self.x -= self.speed

    def rect(self):
        return pygame.Rect(int(self.x), self.y, self.w, self.h)

    def draw(self, surf, tick):
        rect = self.rect()
        if self.kind == "cactus":
            pygame.draw.rect(surf, GREEN, rect, border_radius=4)
            arm1 = pygame.Rect(rect.x + rect.w // 2, rect.y + 8, 8, 18)
            arm2 = pygame.Rect(rect.x + 3, rect.y + 19, 7, 16)
            pygame.draw.rect(surf, GREEN, arm1, border_radius=3)
            pygame.draw.rect(surf, GREEN, arm2, border_radius=3)
        else:
            wing_up = ((tick // 7) % 2) == 0
            body = pygame.Rect(rect.x + 10, rect.y + 8, 23, 12)
            wing_peak = rect.y + (2 if wing_up else 10)
            wing = [(rect.x + 14, rect.y + 13), (rect.x + 24, wing_peak), (rect.x + 31, rect.y + 13)]
            beak = [(rect.x + 33, rect.y + 11), (rect.x + 43, rect.y + 14), (rect.x + 33, rect.y + 17)]
            pygame.draw.rect(surf, RED, body, border_radius=6)
            pygame.draw.polygon(surf, RED, wing)
            pygame.draw.polygon(surf, RED, beak)


class Background:
    def __init__(self):
        self.clouds = []
        for _ in range(7):
            self.clouds.append(
                [random.randint(0, WIDTH), random.randint(35, 145), random.randint(55, 95), random.uniform(0.25, 0.8)]
            )
        self.track_offset = 0.0
        # Static mountains (generated once) to avoid any visual vibration.
        self.far_mountains = [(-40, 235), (80, 170), (190, 235), (320, 160), (470, 235), (620, 175), (780, 235), (940, 165), (1060, 235)]
        self.near_mountains = [(-30, 255), (90, 195), (220, 255), (350, 185), (520, 255), (670, 200), (830, 255), (980, 190), (1110, 255)]

    def update(self, speed):
        self.track_offset = (self.track_offset + speed) % 44

        for cloud in self.clouds:
            cloud[0] -= cloud[3]
            if cloud[0] < -120:
                cloud[0] = WIDTH + random.randint(20, 140)
                cloud[1] = random.randint(35, 145)
                cloud[2] = random.randint(55, 95)

    def draw(self, surf):
        vertical_gradient(surf, SKY_TOP, SKY_BOTTOM)
        pygame.draw.circle(surf, SUN, (WIDTH - 130, 74), 33)

        #mountains 
        pygame.draw.polygon(surf, MOUNTAIN_LIGHT, self.far_mountains)
        pygame.draw.polygon(surf, MOUNTAIN_DARK, self.near_mountains)

        # Clouds
        for x, y, w, _speed in self.clouds:
            pygame.draw.ellipse(surf, WHITE, (x, y, w, 30))
            pygame.draw.ellipse(surf, WHITE, (x + 14, y - 10, w // 2, 28))
            pygame.draw.ellipse(surf, WHITE, (x + w // 2, y - 6, w // 2, 24))

        # Ground
        pygame.draw.rect(surf, GROUND_COLOR, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        pygame.draw.rect(surf, TRACK_COLOR, (0, GROUND_Y - 4, WIDTH, 4))
        for i in range(0, WIDTH + 50, 44):
            start_x = i - self.track_offset
            pygame.draw.line(surf, (165, 165, 165), (start_x, GROUND_Y + 16), (start_x + 20, GROUND_Y + 16), 3)


def draw_hud(surf, score, speed, dino):
    panel = pygame.Surface((250, 94), pygame.SRCALPHA)
    panel.fill(HUD_BG)
    surf.blit(panel, (14, 12))
    pygame.draw.rect(surf, (220, 220, 220), (14, 12, 250, 94), 2, border_radius=8)

    action = "RUN"
    if dino.jumping:
        action = "JUMP"
    elif dino.ducking:
        action = "DUCK"

    surf.blit(small_font.render(f"Score: {score}", True, BLACK), (28, 24))
    surf.blit(small_font.render(f"Speed: {speed:.1f}", True, BLACK), (28, 50))
    surf.blit(small_font.render(f"Action: {action}", True, BLACK), (28, 74))


def draw_center_text(lines):
    y = 78
    for text, use_big, color in lines:
        current_font = title_font if use_big else font
        text_surface = current_font.render(text, True, color)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y))
        y += 58 if use_big else 42


def start_screen(background):
    blink_timer = 0
    demo_dino = Dino()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        blink_timer = (blink_timer + 1) % 60
        background.update(4.8)
        background.draw(screen)
        demo_dino.update(pygame.key.get_pressed())
        demo_dino.draw(screen)

        draw_center_text(
            [
                ("DINO RUNNER", True, BLACK),
                ("SPACE to jump, DOWN to duck", False, BLACK),
                ("Jump cactus, duck birds", False, BLACK),
            ]
        )

        if blink_timer < 34:
            prompt = font.render("Press SPACE to Start", True, (35, 35, 35))
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 260))

        pygame.display.flip()
        clock.tick(FPS)


def game():
    dino = Dino()
    background = Background()
    obstacles = []
    spawn_timer = 0
    spawn_gap = random.randint(70, 112)
    score = 0
    speed = 7.2
    tick = 0

    while True:
        tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dino.update(keys)
        background.update(speed)
        background.draw(screen)
        dino.draw(screen)

        spawn_timer += 1
        if spawn_timer >= spawn_gap:
            obstacles.append(Obstacle(speed))
            spawn_timer = 0
            spawn_gap = random.randint(max(48, int(88 - speed * 2)), max(76, int(126 - speed)))

        dino_box = dino.hitbox()
        for obs in obstacles:
            obs.update(speed)
            obs.draw(screen, tick)
            if dino_box.colliderect(obs.rect()):
                return score

        obstacles = [o for o in obstacles if o.x > -80]
        score += 1
        speed += 0.0022

        draw_hud(screen, score, speed, dino)
        pygame.display.flip()
        clock.tick(FPS)


def game_over(score):
    background = Background()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        background.update(3.8)
        background.draw(screen)
        draw_center_text(
            [
                ("GAME OVER", True, RED),
                (f"Final Score: {score}", False, BLACK),
                ("Press SPACE to Restart", False, BLACK),
            ]
        )
        pygame.display.flip()
        clock.tick(FPS)


def main():
    menu_background = Background()
    while True:
        start_screen(menu_background)
        final_score = game()
        game_over(final_score)


if __name__ == "__main__":
    main()