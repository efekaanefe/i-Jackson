import pygame,os,sys
from pygame.constants import QUIT
from scripts.main import *
pygame.init()
WIN=SCREEN
#start button
START=pygame.transform.scale(pygame.image.load(os.path.join("assets","menu","start.png")),(200,100))
button1= START.get_rect()
button1.x=WIDTH//2-START.get_width()//2 - 450+150
button1.y=HEIGHT//2 -START.get_height()//2-150

#quit button
QUIT=pygame.transform.scale(pygame.image.load(os.path.join("assets","menu","quit.png")),(200,100))
button2=START.get_rect()
button2.x=WIDTH//2 - QUIT.get_width()//2 - 450+150
button2.y=HEIGHT//2 - QUIT.get_height()//2+200-150

#info button
INFO=pygame.transform.scale(pygame.image.load(os.path.join("assets","menu","info.png")),(200,100))
button3=INFO.get_rect()
button3.x=WIDTH//2 -INFO.get_width()//2 - 450 +150
button3.y=HEIGHT//2 -INFO.get_height()//2+100-150


#font type
font=pygame.font.SysFont("Helvetica", 20)

#background
BG=pygame.transform.scale(pygame.image.load(os.path.join("assets","menu","bg.png")),(WIDTH,HEIGHT))

clock=pygame.time.Clock()

INFO_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","menu","info_bg.png")),(WIDTH,HEIGHT))
MUSIC_ON = pygame.transform.scale(pygame.image.load(os.path.join("assets","menu","music_on.png")),(75,75))
MUSIC_OFF = pygame.transform.scale(pygame.image.load(os.path.join("assets","menu","music_off.png")),(75,75))


def main_menu():
    click=False
    music_on = True
    while True:
        #WIN.fill((255,0,0))
        WIN.blit(BG,(0,0))

        mx,my=pygame.mouse.get_pos()

        WIN.blit(START,button1)
        WIN.blit(QUIT,button2)
        WIN.blit(INFO,button3)
        if button1.collidepoint(mx, my):
            if click:
                if music_on:
                    pygame.mixer.music.play(loops=-1)
                main()
        if button2.collidepoint(mx,my):
            if click:
                pygame.quit()
                sys.exit()
        if button3.collidepoint(mx,my):
            if click:
                info()
        
        click=False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key==pygame.K_m:
                    music_on = not music_on
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button== 1:
                    click=True
                    if WIDTH-music_png.get_width()<mx<WIDTH and HEIGHT-music_png.get_height()<my<HEIGHT:
                        music_on = not music_on
                

        music_png = MUSIC_ON if music_on else MUSIC_OFF
        
        WIN.blit(music_png, (WIDTH-music_png.get_width(),HEIGHT-music_png.get_height()))
        
        pygame.display.update()
        clock.tick(75)


def info():
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    run=False
        
        WIN.blit(INFO_BG,(0,0))
        pygame.display.update()

main_menu()