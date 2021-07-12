import pygame, os

class Robot():
    def __init__(self, x, y, width, height, screen):
        self.x  = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.vel = 5

        self.rect = pygame.Rect((self.x, self.y, width, height))
        self.left_sprite = []
        self.right_sprite = []
        self.sprite = None
        self.load_images()
        self.rect = pygame.Rect(self.x, self.y, self.width,self.height) 
        self.current_sprite = 0
        self.update_sprite_incrementation()

        self.health = 1

    def update(self):
        self.current_sprite += self.sprite_incrementation
        if int(self.current_sprite)>=len(self.left_sprite):
            self.current_sprite = 0
        self.update_rect()
        self.draw()
        self.move()

    def update_sprite_incrementation(self):
        self.sprite_incrementation = abs(self.vel/50)

    def load_images(self):
        for i in range(7):
            self.left_sprite.append(
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "robot",f"L{i}.png")),(self.width,self.height)))
            self.right_sprite.append(
                pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "robot",f"R{i}.png")),(self.width,self.height)))

    def draw(self):
        self.sprite = self.left_sprite if self.vel<0 else self.right_sprite

        #Micheal Jackson fun?
        self.sprite = self.right_sprite if self.vel<0 else self.left_sprite

        self.screen.blit(self.sprite[int(self.current_sprite)], (self.x, self.y))
        #pygame.draw.rect(self.screen, (0,0,0), self.rect)

    def move(self):
        self.x += self.vel
    
    def update_rect(self):
        self.rect.x = self.x



