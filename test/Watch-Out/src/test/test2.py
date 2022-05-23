from asyncio import events
from asyncio.windows_events import NULL
import pygame
import os
import time
from threading import Thread
import random
from testMenu import *

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test1")
W=(255, 255, 255) 
B=(0,0,0)
FPS=90
OWN_PG_H, OWN_PG_W = 70, 70
OWN_PG_img = pygame.image.load(os.path.join("circle.png"))
OWN_PG_img=pygame.transform.scale(OWN_PG_img, (OWN_PG_W,OWN_PG_H))
ENEMY_PG_img = pygame.image.load(os.path.join("square.png")) 
ENEMY_PG_img=pygame.transform.scale(ENEMY_PG_img, (OWN_PG_W,OWN_PG_H))
BULLET_VEL=10
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
OWN_bullets, ENEMY_bullets=NULL, NULL;
CANFIRE,FIRED,Menu=False,False,True

def OWN_handle_bullet(ENEMY_PG):
    global OWN_bullets
    if OWN_bullets:
        OWN_bullets.y-=BULLET_VEL
        if ENEMY_PG.colliderect(OWN_bullets):
            OWN_bullets=NULL
            draw_winner("hai vinto")
    
def ENEMY_handle_bullet(OWN_PG):
    global ENEMY_bullets
    if ENEMY_bullets:
        ENEMY_bullets.y+=BULLET_VEL
        if OWN_PG.colliderect(ENEMY_bullets):
            ENEMY_bullets=NULL
            draw_winner("hai perso")

def background_window(OWN_PG_img, OWN_PG, ENEMY_PG, ENEMY_PG_img):
    global ENEMY_bullets, CANFIRE, OWN_bullets, FIRED
    WIN.fill(W) 
    WIN.blit(OWN_PG_img,(OWN_PG.x, OWN_PG.y))
    WIN.blit(ENEMY_PG_img,(ENEMY_PG.x, ENEMY_PG.y))
    if CANFIRE==True and FIRED ==False:
        draw_text = WINNER_FONT.render("VIA!", 1, B)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    if OWN_bullets:
        pygame.draw.rect(WIN,B, OWN_bullets)
    if ENEMY_bullets:
        pygame.draw.rect(WIN,B, ENEMY_bullets)
    pygame.display.update() 

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, B)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(900)
    pygame.quit()

def firetimer():
    global CANFIRE
    print("hi")
    T=random.uniform(1.5, 4)
    time.sleep(T)
    CANFIRE=True

def ENEMY_FIRE(i,ENEMY_PG):
    global ENEMY_bullets,CANFIRE, FIRED
    while CANFIRE==False:
        pass
    T=random.uniform(0.1, 0.3)
    print(T)
    time.sleep(T)
    if CANFIRE and FIRED==False:
        ENEMY_bullets = pygame.Rect(ENEMY_PG.x + OWN_PG_H//2 -5, ENEMY_PG.y + 40, 10, 5)
        FIRED=True

def main(): 
    OWN_PG =pygame.Rect((WIDTH//2)-50, 300, 70, 70)
    ENEMY_PG=pygame.Rect((WIDTH//2)-50, 100, 70, 70)
    clock=pygame.time.Clock()
    run=True
    global OWN_bullets, CANFIRE, FIRED, Menu
    ENEMYT = Thread(target=ENEMY_FIRE, args=(1,ENEMY_PG))
    ENEMYT.start()
    timer=Thread(target=firetimer, args=())
    timer.start()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and OWN_bullets==NULL:
                    if CANFIRE and FIRED==False:
                        OWN_bullets = pygame.Rect(OWN_PG.x + OWN_PG_H//2 -5, OWN_PG.y +5, 10, 5)
                        FIRED=True
                    elif CANFIRE==False:
                        draw_winner("HAI PERSO!")
        keys_pressed=pygame.key.get_pressed()
        OWN_handle_bullet(ENEMY_PG)
        ENEMY_handle_bullet(OWN_PG)
        background_window(OWN_PG_img, OWN_PG, ENEMY_PG, ENEMY_PG_img)  

    pygame.quit()

if __name__=="__main__":
    main()