import pygame
import os
import sys

# Still not fixed these, leave them for now.
WIDTH = 1280
HEIGHT = 600
PLAYER_HEIGHT = 20
PLAYER_WIDTH = 59
Level_select = 3
FPS = 60
ANIMATION = 10  # for when they move
clock = pygame.time.Clock()  # sets internal clock for the game
# Player life
LIFE = 200
TAKE_LIFE = 20
# Actions, these are good I found and because we have the FPS they should be consistent
GRAVITY = 20
MOVING_SPEED = 10
# Not used yet

JUMP_HEIGHT = 360  # This is actually double
PLAYER1_X = 500
PLAYER1_Y = 441

HIT_TIME = 100


class Platform(pygame.sprite.Sprite):
    # Defines size, position and colour of platform objects
    def __init__(self, size_x, size_y, pos_x, pos_y, colour):
        super().__init__()
        self.surface = pygame.Surface((size_x, size_y))
        self.rect = self.surface.get_rect(midtop=(pos_x, pos_y))
        self.surface.fill(colour)
        self.rect.x = pos_x
        self.rect.y = pos_y
        # draws the platform on the game screen

    def draw(self):
        screen.blit(self.surface, self.rect)


class Player(pygame.sprite.Sprite):
    # Probably need to add separate colours for each player, but then aagin we have the sprites?
    def __init__(self, x, y):
        super().__init__()
        # These are not used but DO NO CHANGE.
        self.x = x
        self.y = y
        # the life rectangles for each player
        self.life = pygame.Rect(100, 100, LIFE, 30)
        self.life2 = pygame.Rect(1300, 100, LIFE, 30)
        # PLayer hitboxes
        self.hitbox = pygame.Rect(self.x, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
        self.hitbox2 = pygame.Rect(self.x + 400, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
        # Used in the jump function.
        self.jump1 = False
        self.jump2 = False
        self.jumpCount = JUMP_HEIGHT
        self.jumpCount2 = JUMP_HEIGHT
        # Hitting things
        self.hit = False
        self.hitCount = HIT_TIME
        self.arm = pygame.Rect(self.hitbox.x + 20, self.hitbox.y, 15, 5)
        self.dir = 1

        self.hit2 = False
        self.hitCount2 = HIT_TIME
        self.arm2 = pygame.Rect(self.hitbox.x + 20, self.hitbox.y, 15, 5)
        self.dir2 = -1
        # Updates the player, called after every action.

    def show(self, colour, screen, platforms,STAGE, bc):
        background_box = screen.get_rect()
        
        screen.blit(bc, background_box)
        for i in platforms:
            i.draw()
        
        pygame.draw.rect(screen, colour, self.hitbox)
        pygame.draw.rect(screen, colour, self.hitbox2)
        pygame.draw.rect(screen, colour, self.life)
        pygame.draw.rect(screen, colour, self.life2)
        if self.hit:
            pygame.draw.rect(screen, pygame.Color("green"), self.arm)
        if self.hit2:
            pygame.draw.rect(screen, pygame.Color("green"), self.arm2)

    def reset(self):
        global plColor

        if self.hitbox.y >= 940:
            self.hitbox = pygame.Rect(self.x, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
            self.getHit(1)
           
        if self.hitbox2.y >= 940:
            self.hitbox2 = pygame.Rect(self.x + 400, self.y, PLAYER_HEIGHT, PLAYER_WIDTH)
            self.getHit(2)
          

        # Static move, can mess around with acceleration later

    def move(self):
        global plColor

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.hitbox.move_ip(-MOVING_SPEED, 0)
         
            self.dir = -1
        if keys[pygame.K_d]:
            self.hitbox.move_ip(MOVING_SPEED, 0)
         
            self.dir = 1

        if keys[pygame.K_LEFT]:
            self.hitbox2.move_ip(-MOVING_SPEED, 0)
        
            self.dir2 = -1
        if keys[pygame.K_RIGHT]:
            self.hitbox2.move_ip(MOVING_SPEED, 0)
         
            self.dir2 = 1

        # Static jump, can mess around with equation later. We can try double jump later, shouldn't be too bad.

    def jump(self):

        global plColor
        if self.jump1:
            if self.jumpCount >= JUMP_HEIGHT / 2:
                self.hitbox.move_ip(0, -GRAVITY)
                self.jumpCount -= GRAVITY
             
            elif self.jumpCount >= 0:
                self.hitbox.move_ip(0, GRAVITY)
                self.jumpCount -= GRAVITY
               
            else:
                self.jump1 = False
                self.jumpCount = JUMP_HEIGHT

        if self.jump2:
            if self.jumpCount2 >= JUMP_HEIGHT / 2:
                self.hitbox2.move_ip(0, -GRAVITY)
                self.jumpCount2 -= GRAVITY
              
            elif self.jumpCount2 >= 0:
                self.hitbox2.move_ip(0, GRAVITY)
                self.jumpCount2 -= GRAVITY
              
            else:
                self.jump2 = False
                self.jumpCount2 = JUMP_HEIGHT

# Only hits in one direction. Potential solutions: implement direction? or implement 2 buttons to hit for each direction
    # Also arm isn't attached, it sort of drags behind, not sure how much of a problem it is.
    # Also no actual collsion yet.
    def hitting(self):
        global screen

        if self.hit:
            if self.hitCount >= 0:
                if self.dir == 1:
                    self.arm = pygame.Rect(self.hitbox.x + 20, self.hitbox.y, 15, 5)
                else:
                    self.arm = pygame.Rect(self.hitbox.x - 15, self.hitbox.y, 15, 5)
                # pygame.draw.rect(screen,pygame.Color('green') , arm)
                self.hitCount -= 5
              
            else:
                self.hit = False
                self.hitCount = HIT_TIME
            

        if self.hit2:
            if self.hitCount2 >= 0:
                if self.dir2 == 1:
                    self.arm2 = pygame.Rect(self.hitbox2.x + 20, self.hitbox2.y, 15, 5)
                else:
                    self.arm2 = pygame.Rect(self.hitbox2.x - 15, self.hitbox2.y, 15, 5)
                # pygame.draw.rect(screen,pygame.Color('green') , arm)
                self.hitCount2 -= 5
              
            else:
                self.hit2 = False
                self.hitCount2 = HIT_TIME
              

    # Gets called whenever the player gets hit and reduces that players life.
    def getHit(self, player):
        if player == 1:
            self.life.inflate_ip(-TAKE_LIFE, 0)
         
        if player == 2:
            self.life2.inflate_ip(-TAKE_LIFE, 0)
          

    # For this need a timer and a way to make the player flash?
    def invincible(self):
        pass


class Stage:

    def __init__(self, level_select):
        self.level_select = level_select

    def Level_load(self):
# =============================================================================
#         background = pygame.image.load(os.path.join('images', 'background' + str(Level_select) + '.png')).convert()
#         background_box = screen.get_rect()  # Fits background to screen
#         screen.blit(background, background_box)
# =============================================================================

        if self.level_select == 1:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(WIDTH, 1, WIDTH // 2, HEIGHT - 100, GREEN))
            platforms.add(Platform(300, 20, WIDTH // 1.95, HEIGHT // 3, BLACK))
            platforms.add(Platform(200, 20, WIDTH // 4, HEIGHT // 2, BLACK))
            platforms.add(Platform(200, 20, WIDTH // 1.3, HEIGHT // 2, BLACK))

        if self.level_select == 2:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(100, 20, WIDTH // 2.5, HEIGHT - 100, BLACK))
            platforms.add(Platform(100, 20, WIDTH // 1.4, HEIGHT - 100, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 1.8, HEIGHT - 230, BLACK))
            platforms.add(Platform(300, 20, WIDTH // 1.95, HEIGHT // 3, BLACK))
            platforms.add(Platform(200, 20, WIDTH // 4, HEIGHT // 2, BLACK))
            platforms.add(Platform(200, 20, WIDTH // 1.3, HEIGHT // 2, BLACK))

        if self.level_select == 3:
            platforms = pygame.sprite.Group()
            platforms.add(Platform(150, 20, WIDTH // 2.65, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 1.6, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 2, HEIGHT // 4, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 1.1, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 9, HEIGHT // 1.75, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 4, HEIGHT // 1.3, BLACK))
            platforms.add(Platform(150, 20, WIDTH // 1.3, HEIGHT // 1.3, BLACK))
            
            return platforms
            # Draws platforms
    def background_load(self):
        
        background = pygame.image.load(os.path.join('images', 'background' + str(Level_select) + '.png')).convert()
        return background

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)


SKY = (102, 178, 255)
GREY = (38, 38, 38)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Designated ALPHA colour, if you need something to exist but not be seen make it this colour
bgColor = pygame.Color("white")
fgColor = pygame.Color("black")
plColor = SKY
STAGE = Stage(Level_select)
level = STAGE.Level_load()
bc = STAGE.background_load()
# Initialise our players
PLAYER = Player(PLAYER1_X, PLAYER1_Y)
PLAYER.show(plColor, screen, level,STAGE,bc)

while True:
    # all our events, might be worth putting into a method later, leave for now.
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break
    elif e.type == pygame.KEYDOWN:
        if e.key == pygame.K_w:
            PLAYER.jump1 = True
        if e.key == pygame.K_UP:
            PLAYER.jump2 = True
        if e.key == pygame.K_s:
            PLAYER.hit = True
        if e.key == pygame.K_DOWN:
            PLAYER.hit2 = True
        if e.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
    Level_select = 1
    # All the actions
    PLAYER.move()
    PLAYER.jump()
    #PLAYER.falling()
    PLAYER.hitting()
    PLAYER.reset()
    # Update the display
    PLAYER.show(plColor, screen, level,STAGE,bc)
    pygame.display.update()

pygame.quit()
