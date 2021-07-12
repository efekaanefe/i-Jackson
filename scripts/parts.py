import pygame, os
part_width = 50
part_height = 50

class Part():
    def __init__(self, x, y, vel, screen, type = "screw"):
        self.x = x
        self.y = y
        self.screen  = screen
        self.vel = vel
        self.type = type
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "parts", self.type +".png")), (part_width, part_height))
        self.rect = pygame.Rect(self.x, self.y, part_width, part_height)
    
    #def load_images(self):
        #self.image = pygame.image.load(os.path.join("assets", "parts","screw.png"))

    def update(self):
        self.move()
        self.update_rect()
        self.draw()

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(self.screen, (0,0,0), self.rect)

    def move(self):
        self.y += self.vel
    
    def update_rect(self):
        self.rect.y = self.y


