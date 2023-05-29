import pygame
import random

'''
New feature added was a win lose system.
When score is below 5 the player loses.
When score is PERFECT with no bad blocks the player wins.
'''
# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
BLUE = (0,  0,  255)
GREEN = (0, 255, 0)

class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, colour, width, height):
        """ Constructor. Pass in the color of the block,
        and its size. """
 
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """
 
    # -- Methods
    def __init__(self, colour, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([x, y])
        self.image.fill(colour)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
 
    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y
 
    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y
 
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Karston's Sprites")
FONT = pygame.font.SysFont('Comic Sans', 25, True, False)
 
# This is a list of 'sprites.' Each good block in the program is
# added to this list. The list is managed by a class called 'Group.'
good_block_list = pygame.sprite.Group()

# This is a list of 'sprites.' Each bad block in the program is
# added to this list. The list is managed by a class called 'Group.'
bad_block_list = pygame.sprite.Group()
 
# This is a list of every sprite. 
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# Images from opengameart.org
player_image = pygame.image.load("duckie.png")
good_image = pygame.image.load("health_potion.png")
bad_image = pygame.image.load("poison_bottle.png")
background_image = pygame.image.load("background.png")

# Sound from opengameart.org
good_sound = pygame.mixer.Sound("good_block.wav")
bad_sound = pygame.mixer.Sound("bad_block.wav")
border_sound = pygame.mixer.Sound("bump.ogg")

score_word = FONT.render(("SCORE:"), True, WHITE)
lose_text = FONT.render(("YOU LOST!"), True, WHITE)
win_text = FONT.render(("YOU WON!"), True, WHITE)
 
for i in range(50):
    # This represents a block
    block = Block(RED, 20, 15)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width - 10)
    block.rect.y = random.randrange(screen_height - 10)
 
    # Add the block to the list of objects
    bad_block_list.add(block)
    all_sprites_list.add(block)

for i in range(50):
    block = Block(GREEN, 20, 15)

    block.rect.x = random.randrange(screen_width - 10)
    block.rect.y = random.randrange(screen_height - 10)

    good_block_list.add(block)
    all_sprites_list.add(block)
 
# Create a RED player block
player = Player(BLUE, 20, 15)
all_sprites_list.add(player)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True

        # Set Speed based on the key pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_d:
                player.changespeed(3, 0)
            elif event.key == pygame.K_w:
                player.changespeed(0, -3)
            elif event.key == pygame.K_s:
                player.changespeed(0, 3)

        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.changespeed(3, 0)
            elif event.key == pygame.K_d:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_w:
                player.changespeed(0, 3)
            elif event.key == pygame.K_s:
                player.changespeed(0, -3)


    # Calls update on all the sprites
    all_sprites_list.update()

    
    if player.rect.x <= 0:
        player.rect.x = 2
        border_sound.play()
    if player.rect.x >= 680:
        player.rect.x = 678
        border_sound.play()
    if player.rect.y <= 0:
        player.rect.y = 2
        border_sound.play()
    if player.rect.y >= 385:
        player.rect.y = 383
        border_sound.play()

    if score < -5: # If score is less that 5 u lose
        done = True
    if score == 50: # If score is perfect with no bad blocks u win!
        done = True

    score_text = FONT.render(str(score), True, WHITE)
    # Clear the screen
    screen.blit(background_image, [0, 0])

    for block in all_sprites_list:
        if block.image.get_at((0, 0)) == RED:
            screen.blit(bad_image, [block.rect.x, block.rect.y])

    for block in all_sprites_list:
        if block.image.get_at((0, 0)) == GREEN:
            screen.blit(good_image, [block.rect.x, block.rect.y])

    for player in all_sprites_list:
        if player.image.get_at((0, 0)) == BLUE:
            screen.blit(player_image, [player.rect.x, player.rect.y])

    screen.blit(score_word, [275, 360])
            
    # See if the player block has collided with anything.
    bad_blocks_hit_list = pygame.sprite.spritecollide(player, bad_block_list, True)
    good_blocks_hit_list = pygame.sprite.spritecollide(player, good_block_list, True)
 
    # Check the list of collisions.
    for block in bad_blocks_hit_list:
        score -= 1
        bad_sound.play()
    for block in good_blocks_hit_list:
        score += 1
        good_sound.play()

    screen.blit(score_text, [375, 360])
    # Draw all the spites
    #all_sprites_list.draw(screen)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)

while done: # Two ending screens
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = False
    if score <= -5:
        screen.fill(BLACK)
        screen.blit(lose_text, [300, 150])
    if score == 50:
        screen.fill(BLACK)
        screen.blit(win_text, [300, 150])

    pygame.display.flip()

pygame.quit()
