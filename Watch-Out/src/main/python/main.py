from ast import Global
from pickle import FALSE
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
#baco quando il tempo ancora non finisce
WIDTH, HEIGHT = 1289, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

pygame.display.set_caption("Test1")
W,B=(255, 255, 255), (0,0,0)
FPS=90
OWN_PG_H, OWN_PG_W, BULLET_VEL= 70, 70, 8
OWN_PG_img = pygame.image.load(os.path.join("assets/circle.png"))
OWN_PG_img=pygame.transform.scale(OWN_PG_img, (OWN_PG_W,OWN_PG_H))
ENEMY_PG_img = pygame.image.load(os.path.join("assets/square.png")) 
ENEMY_PG_img=pygame.transform.scale(ENEMY_PG_img, (OWN_PG_W,OWN_PG_H))
WINNER_FONT = pygame.font.SysFont('assets/font.ttf', 100)
OWN_bullets, ENEMY_bullets=NULL, NULL;
CANFIRE,FIRED=False,False

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
        draw_text = WINNER_FONT.render("Watch Out!", 1, B)
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
    main_menu()

def firetimer():
    global CANFIRE
    T=random.uniform(1.5, 4)
    time.sleep(T)
    CANFIRE=True
    return

def ENEMY_FIRE(i,ENEMY_PG):
    global ENEMY_bullets,CANFIRE, FIRED
    while CANFIRE==False:
        pass
    T=random.uniform(0.1, 0.2)
    time.sleep(T)
    print (FIRED)
    if CANFIRE and FIRED==False:
        ENEMY_bullets = pygame.Rect(ENEMY_PG.x + OWN_PG_H//2 -5, ENEMY_PG.y + 40, 10, 5)
        FIRED=True
        return

def play(): 
    OWN_PG =pygame.Rect((WIDTH//2)-50, HEIGHT-240, 70, 70)
    ENEMY_PG=pygame.Rect((WIDTH//2)-50, HEIGHT/2-200, 70, 70)
    clock=pygame.time.Clock()
    run=True
    global OWN_bullets, CANFIRE, FIRED
    CANFIRE=False
    FIRED=False
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
                        FIRED=True
                        draw_winner("HAI PERSO!")
        OWN_handle_bullet(ENEMY_PG)
        ENEMY_handle_bullet(OWN_PG)
        background_window(OWN_PG_img, OWN_PG, ENEMY_PG, ENEMY_PG_img)  
    
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

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
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