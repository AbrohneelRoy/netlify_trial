python = "Python"
repr(repr(repr(python)))
import pygame
import sys
import random
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Python Bros")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

# Game variables
clock = pygame.time.Clock()
FPS = 60
GRAVITY = 1
SCROLL_THRESH = 200
MAX_LEVELS = 5
current_level = 1
score = 0
game_paused = False
game_over = False
player_alive = True
level_complete = False
mario_size = 1  # 1=small, 2=big, 3=fire
invincible = False
invincible_counter = 0

# Font
font = pygame.font.SysFont('Bauhaus 93', 30)
big_font = pygame.font.SysFont('Bauhaus 93', 70)

# Load sounds
try:
    jump_sound = mixer.Sound('assets/jump.wav')
    coin_sound = mixer.Sound('assets/coin.wav')
    powerup_sound = mixer.Sound('assets/powerup.wav')
    stomp_sound = mixer.Sound('assets/stomp.wav')
    die_sound = mixer.Sound('assets/die.wav')
    level_complete_sound = mixer.Sound('assets/level_complete.wav')
    game_over_sound = mixer.Sound('assets/game_over.wav')
    background_music = mixer.Sound('assets/background.wav')
    background_music.set_volume(0.5)
    background_music.play(-1)
except:
    print("Warning: Sound files not found. Game will run without sound.")


# Load images
def load_image(name, scale=1):
    img = pygame.Surface((50, 50))
    img.fill(SKY_BLUE)
    pygame.draw.rect(img, RED, (10, 30, 30, 20))  # Simple placeholder
    return img


try:
    # Player images
    player_img_small = pygame.image.load('assets/mario_small.png').convert_alpha()
    player_img_big = pygame.image.load('assets/mario_big.png').convert_alpha()

    # Tile images
    dirt_img = pygame.image.load('assets/dirt.png').convert_alpha()
    grass_img = pygame.image.load('assets/grass.png').convert_alpha()
    brick_img = pygame.image.load('assets/brick.png').convert_alpha()
    question_img = pygame.image.load('assets/question.png').convert_alpha()

    # Enemy images
    goomba_img = pygame.image.load('assets/goomba.png').convert_alpha()
    koopa_img = pygame.image.load('assets/koopa.png').convert_alpha()

    # Power-up images
    mushroom_img = pygame.image.load('assets/mushroom.png').convert_alpha()
    flower_img = pygame.image.load('assets/flower.png').convert_alpha()
    coin_img = pygame.image.load('assets/coin.png').convert_alpha()

    # Background
    bg_img = pygame.image.load('assets/background.png').convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Castle image for level end
    castle_img = pygame.image.load('assets/castle.png').convert_alpha()
    castle_img = pygame.transform.scale(castle_img, (150, 150))

except:
    print("Warning: Image files not found. Using placeholder graphics.")
    player_img_small = load_image('mario_small')
    player_img_big = load_image('mario_big')
    dirt_img = pygame.Surface((50, 50))
    dirt_img.fill(BROWN)
    grass_img = pygame.Surface((50, 50))
    grass_img.fill(GREEN)
    brick_img = pygame.Surface((50, 50))
    brick_img.fill(RED)
    question_img = pygame.Surface((50, 50))
    question_img.fill(BROWN)
    pygame.draw.rect(question_img, (255, 255, 0), (10, 10, 30, 30))  # Define YELLOW as (255, 255, 0)
    goomba_img = load_image('goomba')
    koopa_img = load_image('koopa')
    mushroom_img = load_image('mushroom')
    flower_img = load_image('flower')
    coin_img = load_image('coin')
    bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img.fill(SKY_BLUE)
    castle_img = pygame.Surface((150, 150))
    castle_img.fill(GRAY)


# Button class
class Button:
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button
        surface.blit(self.image, self.rect)

        return action


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.reset(x, y, size)

    def update(self, game_over, world, enemy_group, powerup_group, item_box_group, exit_group, water_group):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if not player_alive or game_over or game_paused:
            return

        # Get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_UP] and not self.jumped and not self.in_air:
            try:
                jump_sound.play()
            except:
                pass
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_UP]:
            self.jumped = False
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # Handle animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # Add gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Check for collision
        self.in_air = True
        for tile in world.tile_list:
            # Check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # Check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Check if below the ground (jumping)
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # Check if above the ground (falling)
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        # Check for collision with enemies
        if pygame.sprite.spritecollide(self, enemy_group, False):
            if not invincible:
                self.die()

        # Check for collision with powerups
        if pygame.sprite.spritecollide(self, powerup_group, True):
            try:
                powerup_sound.play()
            except:
                pass
            global mario_size
            if mario_size < 2:
                mario_size = 2
                self.reset(self.rect.x, self.rect.y, 2)
            else:
                mario_size = 3  # Fire power

        # Check for collision with item boxes
        for item_box in item_box_group:
            if pygame.sprite.collide_rect(self, item_box):
                # Hit from below
                if self.rect.bottom < item_box.rect.top + col_thresh:
                    item_box.hit()

        # Check for collision with exit
        level_complete = False
        for exit in exit_group:
            if pygame.sprite.collide_rect(self, exit):
                level_complete = True

        # Check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.die()

        # Update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # Update scroll based on player position
        if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (
                world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
            self.rect.x -= dx
            screen_scroll = -dx
        else:
            screen_scroll = 0

        return screen_scroll, level_complete

    def die(self):
        global player_alive, lives
        player_alive = False
        lives -= 1
        try:
            die_sound.play()
        except:
            pass

    def reset(self, x, y, size):
        if size == 1:
            self.images_right = []
            self.images_left = []
            for i in range(1, 4):
                img_right = player_img_small
                img_right = pygame.transform.scale(img_right, (40, 40))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
        else:
            self.images_right = []
            self.images_left = []
            for i in range(1, 4):
                img_right = player_img_big
                img_right = pygame.transform.scale(img_right, (40, 60))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)

        self.image = self.images_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 1
        self.in_air = True
        self.index = 0
        self.counter = 0


# World class
class World():
    def __init__(self, data):
        self.tile_list = []

        # Load images
        dirt_img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
        grass_img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
        brick_img = pygame.transform.scale(brick_img, (TILE_SIZE, TILE_SIZE))
        question_img = pygame.transform.scale(question_img, (TILE_SIZE, TILE_SIZE))

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  # Dirt
                    img = dirt_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:  # Grass
                    img = grass_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:  # Brick
                    img = brick_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:  # Question block
                    img = question_img
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(goomba_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.direction = 1

    def update(self, world):
        # Move
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

        # Check for collision with tiles
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + self.move_direction, self.rect.y, 40, 40):
                self.move_direction *= -1
                self.move_counter *= -1
                break


# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type  # 'mushroom' or 'flower'
        if type == 'mushroom':
            self.image = pygame.transform.scale(mushroom_img, (40, 40))
        else:
            self.image = pygame.transform.scale(flower_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.vel_y = 0

    def update(self, world):
        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        # Move
        self.rect.x += 2 * self.direction

        # Check for collision with tiles
        for tile in world.tile_list:
            # Horizontal collision
            if tile[1].colliderect(self.rect.x + (2 * self.direction), self.rect.y, 40, 40):
                self.direction *= -1
            # Vertical collision
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, 40, 40):
                if self.vel_y > 0:  # Falling
                    self.rect.bottom = tile[1].top
                    self.vel_y = 0

        self.rect.y += dy


# Item box class
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = pygame.transform.scale(question_img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_count = 0
        self.max_hits = 1

    def hit(self):
        self.hit_count += 1
        if self.hit_count <= self.max_hits:
            try:
                coin_sound.play()
            except:
                pass
            global score
            score += 100
            if self.item_type == 'mushroom':
                powerup_group.add(PowerUp(self.rect.x, self.rect.y - 50, 'mushroom'))
            elif self.item_type == 'flower':
                powerup_group.add(PowerUp(self.rect.x, self.rect.y - 50, 'flower'))


# Exit class
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = castle_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(coin_img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.direction = 1

    def update(self):
        # Bouncing animation
        self.counter += 1
        if self.counter > 10:
            self.direction *= -1
            self.counter = 0
        self.rect.y += self.direction


# Create buttons
restart_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, pygame.Surface((100, 50)))
exit_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 160, pygame.Surface((100, 50)))
start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, pygame.Surface((200, 80)))
resume_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, pygame.Surface((200, 80)))

# Game variables
TILE_SIZE = 50
lives = 3
bg_scroll = 0

# Level data (simplified for example)
level1_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Add platforms and items to level data
level1_data[7][5] = 2
level1_data[7][6] = 2
level1_data[7][7] = 2
level1_data[7][10] = 2
level1_data[7][11] = 2
level1_data[7][12] = 2
level1_data[7][15] = 2
level1_data[7][16] = 2
level1_data[7][17] = 2
level1_data[7][20] = 2
level1_data[7][21] = 2
level1_data[7][22] = 2
level1_data[7][25] = 2
level1_data[7][26] = 2
level1_data[7][27] = 2

# Create sprite groups
enemy_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

# Create world
world = World(level1_data)

# Create player
player = Player(100, SCREEN_HEIGHT - 130, mario_size)

# Add items to the world
item_box_group.add(ItemBox(300, SCREEN_HEIGHT - 180, 'mushroom'))
item_box_group.add(ItemBox(500, SCREEN_HEIGHT - 180, 'flower'))
exit_group.add(Exit(1500, SCREEN_HEIGHT - 180))

# Add enemies
enemy_group.add(Enemy(400, SCREEN_HEIGHT - 90))
enemy_group.add(Enemy(700, SCREEN_HEIGHT - 90))

# Add coins
for i in range(5):
    coin_group.add(Coin(200 + i * 100, SCREEN_HEIGHT - 150))


# Main game loop
def main_game():
    global bg_scroll, current_level, lives, score, game_paused, game_over, player_alive, level_complete, invincible, invincible_counter

    run = True
    while run:
        clock.tick(FPS)

        # Draw background
        screen.blit(bg_img, (0, 0))

        # Draw world
        world.draw()

        # Update and draw groups
        enemy_group.update(world)
        powerup_group.update(world)
        coin_group.update()

        enemy_group.draw(screen)
        powerup_group.draw(screen)
        item_box_group.draw(screen)
        exit_group.draw(screen)
        coin_group.draw(screen)

        # Update player
        if player_alive:
            screen_scroll, level_complete = player.update(game_over, world, enemy_group, powerup_group, item_box_group,
                                                          exit_group, [])
            bg_scroll += screen_scroll

            # Check if level complete
            if level_complete:
                try:
                    level_complete_sound.play()
                except:
                    pass
                current_level += 1
                if current_level <= MAX_LEVELS:
                    # Reset level (in a full game, you'd load a new level here)
                    player.reset(100, SCREEN_HEIGHT - 130, mario_size)
                    bg_scroll = 0
                    level_complete = False
                else:
                    # Game completed
                    draw_text('YOU WIN!', big_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100)
                    if restart_button.draw(screen):
                        # Reset game
                        current_level = 1
                        lives = 3
                        score = 0
                        mario_size = 1
                        player.reset(100, SCREEN_HEIGHT - 130, mario_size)
                        bg_scroll = 0
                        game_over = False
                        player_alive = True
                    if exit_button.draw(screen):
                        run = False

        # Draw player
        if player_alive:
            screen.blit(player.image, (player.rect.x - bg_scroll, player.rect.y))

        # Check for game over
        if not player_alive:
            if lives <= 0:
                game_over = True
                try:
                    game_over_sound.play()
                except:
                    pass
                draw_text('GAME OVER', big_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100)
                if restart_button.draw(screen):
                    # Reset game
                    current_level = 1
                    lives = 3
                    score = 0
                    mario_size = 1
                    player.reset(100, SCREEN_HEIGHT - 130, mario_size)
                    bg_scroll = 0
                    game_over = False
                    player_alive = True
                if exit_button.draw(screen):
                    run = False
            else:
                # Reset level with one less life
                player.reset(100, SCREEN_HEIGHT - 130, mario_size)
                bg_scroll = 0
                player_alive = True

        # Draw HUD
        draw_text(f'LIVES: {lives}', font, WHITE, 20, 20)
        draw_text(f'SCORE: {score}', font, WHITE, 20, 50)
        draw_text(f'LEVEL: {current_level}/{MAX_LEVELS}', font, WHITE, 20, 80)

        # Check for pause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused

        # Pause menu
        if game_paused:
            draw_text('PAUSED', big_font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100)
            if resume_button.draw(screen):
                game_paused = False
            if exit_button.draw(screen):
                run = False

        pygame.display.update()

    pygame.quit()
    sys.exit()


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Start screen
def start_screen():
    run = True
    while run:
        screen.blit(bg_img, (0, 0))
        draw_text('SUPER PYTHON BROS', big_font, WHITE, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 200)

        if start_button.draw(screen):
            run = False
            main_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()