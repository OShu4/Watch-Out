from ast import Global
from multiprocessing.connection import wait
from pickle import FALSE
from this import d
import pygame, sys
from button import Button
from asyncio import events
from asyncio.windows_events import NULL
import os
import time
from threading import Thread
import random

pygame.font.init()
pygame.mixer.init()
pygame.init()
#TODO CONTATORE CHE VEDE QUANTO TEMPO PASSA DAL VIA AL TUO CLICK 
WIDTH, HEIGHT = 1289, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
BG = pygame.image.load("src/main/python/assets/Background/Background.png")

def get_font(size): 
    return pygame.font.Font("src/main/python/assets/Font/font.ttf", size)

pygame.display.set_caption("Test1")
W,B=(255, 255, 255), (0,0,0)
FPS=90
OWN_PG_H, OWN_PG_W, BULLET_VEL= 90, 80, 8
ENEMY_NUMBER="0"
ENEMY_PG_img = pygame.image
OWN_PG_img = pygame.image.load(os.path.join("src/main/python/assets/Prot/prot.gif"))
OWN_PG_img=pygame.transform.scale(OWN_PG_img, (OWN_PG_W,OWN_PG_H))
WINNER_FONT = pygame.font.SysFont('Watch-Out/src/main/python/assets/Font/font.ttf', 100)
OWN_bullets, ENEMY_bullets=NULL, NULL
CANFIRE,FIRED,DIE=False,False,False
LEVELDIFF=[0, 0.3, 0.26, 0.24, 0.22]
MENU_MOUSE_POS = pygame.mouse.get_pos()

def setEnemy():
    global ENEMY_PG_img
    ENEMY_PG_img = pygame.image.load(os.path.join("src/main/python/assets/Enemy/enemy.gif"))    #ENEMY_PG_img = pygame.image.load(os.path.join("src/main/python/assets/Enemy/enemy"+ENEMY_NUMBER+".gif")) 
    ENEMY_PG_img=pygame.transform.scale(ENEMY_PG_img, (OWN_PG_W,OWN_PG_H))
    
def OWN_handle_bullet(ENEMY_PG):
    global OWN_bullets, ENEMY_NUMBER
    if OWN_bullets:
        OWN_bullets.y-=BULLET_VEL
        if ENEMY_PG.colliderect(OWN_bullets):
            OWN_bullets=NULL
            ENEMY_NUMBER= str(int(ENEMY_NUMBER)+1)
            draw_winner("hai vinto!")

def ENEMY_handle_bullet(OWN_PG):
    global ENEMY_bullets
    if ENEMY_bullets:
        ENEMY_bullets.y+=BULLET_VEL
        if OWN_PG.colliderect(ENEMY_bullets):
            ENEMY_bullets=NULL
            draw_winner("hai perso!")

def background_window(OWN_PG_img, OWN_PG, ENEMY_PG, ENEMY_PG_img,EXIT):
    global ENEMY_bullets, CANFIRE, OWN_bullets, FIRED, MENU_MOUSE_POS
    WIN.fill(W) 
    WIN.blit(OWN_PG_img,(OWN_PG.x, OWN_PG.y))
    WIN.blit(ENEMY_PG_img,(ENEMY_PG.x, ENEMY_PG.y))
    if CANFIRE==True and FIRED ==False:
        draw_text = get_font(100).render("Watch Out!", 1, B)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                        2, HEIGHT/2 - draw_text.get_height()/2))
    if OWN_bullets:
        pygame.draw.rect(WIN,B, OWN_bullets)
    if ENEMY_bullets:
        pygame.draw.rect(WIN,B, ENEMY_bullets)
    EXIT.update(WIN)
    pygame.display.update() 


def draw_winner(text):
    draw_text = get_font(100).render(text, 1, B)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                        2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(900)
    play()

def firetimer():
    global CANFIRE, DIE
    DIE=True
    T=random.uniform(1.5, 3.5)
    time.sleep(T)
    CANFIRE=True
    DIE=False
    return

def ENEMY_FIRE(i,ENEMY_PG):
    global ENEMY_bullets,CANFIRE, FIRED,LEVELDIFF, ENEMY_NUMBER
    while CANFIRE==False:
        pass
    if ENEMY_NUMBER!="0":
        time.sleep(LEVELDIFF[int(ENEMY_NUMBER)])
        if CANFIRE and FIRED==False:
            ENEMY_bullets = pygame.Rect(ENEMY_PG.x + OWN_PG_H//2 -5, ENEMY_PG.y + 40, 10, 5)
            FIRED=True
    print (ENEMY_NUMBER)
    return

def play(): 
    global OWN_bullets, CANFIRE, FIRED, DIE, ENEMY_NUMBER
    setEnemy()
    EXIT = Button(image=pygame.image.load("src/main/python/assets/Background/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    OWN_PG =pygame.Rect((WIDTH//2)-50, HEIGHT-240, 70, 70)
    ENEMY_PG=pygame.Rect((WIDTH//2)-50, HEIGHT/2-200, 70, 70)
    timer=Thread(target=firetimer, args=())
    clock=pygame.time.Clock()
    run=True
    ENEMYT = Thread(target=ENEMY_FIRE, args=(1,ENEMY_PG))
    while(DIE==True):
        time.sleep(0.2)
    CANFIRE, FIRED=False,False
    ENEMYT.start()
    timer.start()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    
            if event.type == pygame.MOUSEBUTTONDOWN:
                print ("dio cane")
                if EXIT.checkForInput(MENU_MOUSE_POS):
                    print ("dio stronzo")
                    main_menu()
                if event.button == 1 and OWN_bullets==NULL:
                    if CANFIRE and FIRED==False:
                        OWN_bullets = pygame.Rect(OWN_PG.x + OWN_PG_H//2 -5, OWN_PG.y +5, 10, 5)
                        FIRED=True
                    elif CANFIRE==False and FIRED==False:
                        FIRED=True
                        draw_winner("hai perso!")
                    
        OWN_handle_bullet(ENEMY_PG)
        ENEMY_handle_bullet(OWN_PG)
        background_window(OWN_PG_img, OWN_PG, ENEMY_PG, ENEMY_PG_img,EXIT)  
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        WIN.fill("white")
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        WIN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("src/main/python/assets/Background/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("src/main/python/assets/Background/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("src/main/python/assets/Background/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()