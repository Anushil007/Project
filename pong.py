import pygame
import time
from paddle import Paddle
from ball import Ball

pygame.init()
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
Blue = (52, 31, 222)
Red = (238, 15, 15)
Green = (1, 239, 19)


# Sound
pygame.mixer.init()
bouncefx = pygame.mixer.Sound("bounce.ogg")
hitfx = pygame.mixer.Sound("hit.wav")


def text_objects(text1, font1):
    textSurface = font1.render(text1, True, BLACK)
    return textSurface, textSurface.get_rect()


# Opening  new window
size = (800, 600)
window_width = 800
window_height = 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

paddleA = Paddle(Blue, 10, 100)
paddleA.rect.x = 10
paddleA.rect.y = 200

paddleB = Paddle(Red, 10, 100)
paddleB.rect.x = 790
paddleB.rect.y = 200

ball = Ball(Green, 15, 15)
ball.rect.x = 400
ball.rect.y = 200

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (int(x + (w / 2)), int(y + (h / 2)))
    screen.blit(textSurf, textRect)


def quitgame():
    pygame.quit()
    quit()

def rules():
    screen.fill(WHITE)
    largeText = pygame.font.SysFont("comicsansms", 15)
    TextSurf, TextRect = text_objects("1. First to 11 wins. \n 2. Player 1 use w and s for movement and Player 2 use "
                                      "arrow keys", largeText)
    TextRect.center = (int(window_width / 2), int(window_height / 2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(0)

    pygame.display.update()
    time.sleep(5)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(WHITE)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("PONG", largeText)
        TextRect.center = ((window_width / 2), (window_height / 2))
        screen.blit(TextSurf, TextRect)

        button("GO!", 150, 450, 100, 50, Blue, Green, play)
        button("Rules", 550, 450, 100, 50, Red, Green, rules)

        pygame.display.update()
        time.sleep(0)


#  Main Loop
def play():
    carryOn = True
    scoreA = 0
    scoreB = 0

    while carryOn:
        #  Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                carryOn = False  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                    carryOn = False

        # Moving the paddles when the use uses the arrow keys (player B) or "W/S" keys (player A)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddleA.moveUp(5)
        if keys[pygame.K_s]:
            paddleA.moveDown(5)
        if keys[pygame.K_UP]:
            paddleB.moveUp(5)
        if keys[pygame.K_DOWN]:
            paddleB.moveDown(5)

        # Game logic
        all_sprites_list.update()

        # Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x >= 790:
            scoreA += 1
            ball.velocity[0] = -ball.velocity[0]
            bouncefx.play()
        if ball.rect.x <= 0:
            scoreB += 1
            ball.velocity[0] = -ball.velocity[0]
            bouncefx.play()
        if ball.rect.y > 590:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:
            ball.velocity[1] = -ball.velocity[1]

        # Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
            ball.bounce()
            hitfx.play()
        # First, clear the screen to black.
        screen.fill(WHITE)
        # Draw the net
        pygame.draw.line(screen, BLACK, [400, 0], [400, 600], 5)

        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen)

        # Display scores:
        font = pygame.font.Font(None, 74)
        text = font.render(str(scoreA), 1, Blue)
        screen.blit(text, (200, 10))
        text = font.render(str(scoreB), 1, Red)
        screen.blit(text, (600, 10))
        if abs(scoreA) == 11:
            screen.fill(WHITE)
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = text_objects("A WINS", largeText)
            TextRect.center = (int(window_width / 2), int(window_height / 2))
            screen.blit(TextSurf, TextRect)

            button("Again!", 150, 450, 100, 50, Blue, Green, play)
            button("Quit", 550, 450, 100, 50, Red, Green, quitgame)

            pygame.display.update()
            time.sleep(0)

        if abs(scoreB) == 11:
            screen.fill(WHITE)
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = text_objects("B WINS", largeText)
            TextRect.center = (int(window_width / 2), int(window_height / 2))
            screen.blit(TextSurf, TextRect)

            button("Again!", 150, 450, 100, 50, Blue, Green, play)
            button("Quit", 550, 450, 100, 50, Red, Green, quitgame)

            pygame.display.update()
            time.sleep(0)

        pygame.display.flip()

        # Limit to 60 frames per second
        clock.tick(60)


game_intro()
play()
pygame.quit()
