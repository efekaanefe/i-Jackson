import pygame
pygame.init()

class Particle():
    def __init__(self, x, y, x_vel, y_vel, timer, color, screen):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.timer = timer
        self.color  = color
        self.screen = screen
        
    
    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel
        #self.y_vel += 0.1 # gravity
        self.timer -= 0.3
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), (self.timer))

        radius = self.timer * 2
        self.screen.blit(self.circle_surf(radius, (20,20,60)), (int(self.x)-radius, int(self.y)-radius), special_flags = pygame.BLEND_RGB_ADD)


    def circle_surf(self, radius, color):
        surf = pygame.Surface((radius*2,radius*2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0,0,0))
        return surf
