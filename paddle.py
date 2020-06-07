import pygame

BLACK = (0, 0, 0)


class Paddle(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in pygame.

    def __init__(self, color, width, height):
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # draw paddle
        pygame.draw.rect(self.image, color, [0, 0,  width, height])

        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y > 590:
            self.rect.y = 590
