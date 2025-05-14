import pygame
import sys
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 120
COLORS = {
    'background': (10, 10, 30),
    'player': (100, 200, 255),
    'enemy': (200, 50, 80),
    'bullet': (255, 255, 200),
    'powerup': (150, 255, 150)
}

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Vortex 2025")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Load assets
try:
    player_img = pygame.image.load('assets/player_ship.png').convert_alpha()
    enemy_imgs = [
        pygame.image.load('assets/enemy1.png').convert_alpha(),
        pygame.image.load('assets/enemy2.png').convert_alpha(),
        pygame.image.load('assets/enemy3.png').convert_alpha()
    ]
    powerup_imgs = {
        'health': pygame.image.load('assets/health_powerup.png').convert_alpha(),
        'shield': pygame.image.load('assets/shield_powerup.png').convert_alpha(),
        'spread': pygame.image.load('assets/spread_powerup.png').convert_alpha()
    }
    bullet_img = pygame.image.load('assets/laser.png').convert_alpha()
    background = pygame.image.load('assets/nebula_bg.jpg').convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load sounds
    laser_sound = mixer.Sound('assets/laser.wav')
    explode_sound = mixer.Sound('assets/explode.wav')
    powerup_sound = mixer.Sound('assets/powerup.wav')
    mixer.music.load('assets/electronic_bg_music.mp3')
    mixer.music.set_volume(0.3)
    mixer.music.play(-1)
except Exception as e:
    print(f"Asset loading error: {e}")
    # Fallback to basic graphics
    player_img = pygame.Surface((50, 50))
    player_img.fill(COLORS['player'])
    # ... similar fallbacks for other images ...


# Particle system
class Particle(pygame.sprite.Sprite):
    def __init__(self, position, color, speed, lifespan):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.lifespan = lifespan
        self.age = 0

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.age += 1
        if self.age > self.lifespan:
            self.kill()


# Enhanced Player class with powerups
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = player_img
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.speed = 8
        self.health = 150
        self.max_health = 150
        self.powerups = {
            'shield': {'active': False, 'duration': 5000, 'start_time': 0},
            'spread': {'active': False, 'duration': 8000, 'start_time': 0}
        }
        self.last_shot = 0
        self.shoot_delay = 200
        self.engine_particles = []

    def update(self, keys, current_time):
        # Movement
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed

        # Screen boundaries
        self.rect.clamp_ip(screen.get_rect())

        # Engine particles
        if random.random() < 0.3:
            self.engine_particles.append(Particle(
                (self.rect.centerx + random.randint(-10, 10), self.rect.bottom),
                (100, 200, 255),
                (random.uniform(-0.5, 0.5), random.randint(1, 3)),
                30
            ))

    def shoot(self, current_time):
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            laser_sound.play()

            if self.powerups['spread']['active']:
                angles = [-15, 0, 15]
                for angle in angles:
                    Bullet(self.rect.center, angle, 'player')
            else:
                Bullet(self.rect.center, 0, 'player')

    def apply_powerup(self, power_type):
        powerup_sound.play()
        if power_type == 'health':
            self.health = min(self.max_health, self.health + 40)
        elif power_type in self.powerups:
            self.powerups[power_type]['active'] = True
            self.powerups[power_type]['start_time'] = pygame.time.get_ticks()

    def check_powerups(self):
        current_time = pygame.time.get_ticks()
        for p in self.powerups.values():
            if p['active'] and current_time - p['start_time'] > p['duration']:
                p['active'] = False

    def draw_ui(self, surface):
        # Health bar
        pygame.draw.rect(surface, (200, 50, 80), (20, 20, 200, 25))
        pygame.draw.rect(surface, (50, 200, 80), (20, 20, 200 * (self.health / self.max_health), 25))

        # Powerup indicators
        y = 60
        for name, p in self.powerups.items():
            if p['active']:
                time_left = (p['duration'] - (pygame.time.get_ticks() - p['start_time'])) / 1000
                text = font.render(f"{name.capitalize()}: {time_left:.1f}s", True, (200, 200, 255))
                surface.blit(text, (20, y))
                y += 30


# Advanced Bullet class with particle trails
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, angle=0, owner='player'):
        super().__init__()
        self.image = pygame.transform.rotate(bullet_img, angle)
        self.rect = self.image.get_rect(center=position)
        self.speed = 12 if owner == 'player' else 8
        self.owner = owner
        self.angle = math.radians(angle)
        self.trail = []

    def update(self):
        self.rect.x += self.speed * math.cos(math.radians(90 + self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(90 + self.angle))

        # Add trail particles
        if random.random() < 0.5:
            self.trail.append(Particle(
                self.rect.center,
                (255, 255, 200) if self.owner == 'player' else (200, 50, 80),
                (random.uniform(-0.5, 0.5), random.uniform(-1, 0)),
                15
            ))

        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()


# Smart Enemy classes
class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), -100))
        self.speed = random.randint(3, 6)
        self.health = 50
        self.attack_cooldown = 2000
        self.last_attack = 0

    def update(self, current_time, player_pos):
        # Advanced movement patterns
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

        # Predictive shooting
        if current_time - self.last_attack > self.attack_cooldown:
            self.attack(player_pos)
            self.last_attack = current_time

    def attack(self, target_pos):
        # Calculate direction to player
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        Bullet(self.rect.center, angle, 'enemy')


class ZigzagEnemy(EnemyBase):
    def __init__(self):
        super().__init__(enemy_imgs[1])
        self.health = 80
        self.speed = 4
        self.angle = 0

    def update(self, current_time, player_pos):
        self.angle += 5
        self.rect.x += math.sin(math.radians(self.angle)) * 3
        super().update(current_time, player_pos)


class BossEnemy(EnemyBase):
    def __init__(self):
        super().__init__(enemy_imgs[2])
        self.health = 500
        self.speed = 2
        self.attack_cooldown = 1000

    def attack(self, target_pos):
        for angle in range(0, 360, 30):
            Bullet(self.rect.center, angle, 'enemy')


# Powerup system
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.types = ['health', 'shield', 'spread']
        self.type = random.choice(self.types)
        self.image = powerup_imgs[self.type]
        self.rect = self.image.get_rect(center=position)
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Game manager class
class GameState:
    def __init__(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.score = 0
        self.wave = 0
        self.game_over = False
        self.all_sprites.add(self.player)

    def spawn_wave(self):
        self.wave += 1
        enemies_to_spawn = [
                               EnemyBase(enemy_imgs[0]) for _ in range(3 + self.wave)
                           ] + [
                               ZigzagEnemy() for _ in range(1 + self.wave // 2)
                           ]
        if self.wave % 5 == 0:
            enemies_to_spawn.append(BossEnemy())

        for enemy in enemies_to_spawn:
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def check_collisions(self):
        # Player bullets hitting enemies
        for bullet in self.bullets:
            if bullet.owner == 'player':
                hits = pygame.sprite.spritecollide(bullet, self.enemies, False)
                for enemy in hits:
                    enemy.health -= 25
                    self.score += 10
                    bullet.kill()
                    if enemy.health <= 0:
                        enemy.kill()
                        self.score += 100
                        if random.random() < 0.2:
                            self.powerups.add(PowerUp(enemy.rect.center))
                        explode_sound.play()

        # Enemy bullets hitting player
        hits = pygame.sprite.spritecollide(self.player, self.bullets, True)
        for _ in hits:
            if not self.player.powerups['shield']['active']:
                self.player.health -= 20
                if self.player.health <= 0:
                    self.game_over = True

        # Powerup collection
        pygame.sprite.spritecollide(self.player, self.powerups, True,
                                    collided=lambda s, p: pygame.sprite.collide_circle(s, p))

    def update(self, keys, current_time):
        if not self.game_over:
            self.player.check_powerups()
            self.all_sprites.update(keys=keys, current_time=current_time)
            self.check_collisions()

            if len(self.enemies) == 0:
                self.spawn_wave()


# Main game loop
def main():
    game = GameState()
    last_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        dt = current_time - last_time
        last_time = current_time

        # Event handling
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.player.shoot(current_time)
            if event.type == pygame.KEYDOWN and game.game_over:
                if event.key == pygame.K_r:
                    game = GameState()

        # Update game state
        if not game.game_over:
            game.update(keys, current_time)

        # Drawing
        screen.blit(background, (0, 0))

        # Draw all sprites with parallax effect
        for sprite in game.all_sprites:
            screen.blit(sprite.image, sprite.rect)

        # Draw UI
        game.player.draw_ui(screen)
        score_text = font.render(f"Score: {game.score}", True, (200, 200, 255))
        screen.blit(score_text, (WIDTH - 200, 20))

        if game.game_over:
            # Modern game over screen
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            game_over_text = font.render("MISSION FAILED", True, (200, 50, 80))
            screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
            restart_text = font.render("Press R to Retry", True, (200, 200, 255))
            screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()