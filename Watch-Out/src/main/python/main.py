import pygame, sys
from button import Button
from asyncio.windows_events import NULL
import os
import time
from threading import Thread
import random
import time
from fileManager import FileManager

pygame.font.init()
pygame.mixer.init()
pygame.init() 
WIDTH, HEIGHT = 1290, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
BG = pygame.image.load("Watch-Out/src/main/python/assets/Background/Background.png")

def get_font(size): 
    return pygame.font.Font("Watch-Out/src/main/python/assets/Font/font.ttf", size)

pygame.display.set_caption("Test1")
W,B,R,G=(255, 255, 255), (0,0,0), (255,0,0), (0,255,0)
FPS=90
OWN_PG_H, OWN_PG_W, BULLET_VEL= 90, 80, 8
ENEMY_NUMBER="0"
ENEMY_PG_img = pygame.image
OWN_PG_img = pygame.image.load(os.path.join("Watch-Out/src/main/python/assets/Prot/prot.gif"))
OWN_PG_img=pygame.transform.scale(OWN_PG_img, (OWN_PG_W,OWN_PG_H))
HP_img = pygame.image.load(os.path.join("Watch-Out/src/main/python/assets/Background/hp.jpg"))
HP_img=pygame.transform.scale(HP_img , (30,25))
OWN_bullets, ENEMY_bullets=NULL, NULL
CANFIRE,FIRED,DIE,isMENU,LOSE,BESTSCORE=False,False,False,True,NULL,0.0
PG_HP=5
LEVELDIFF=[0, 0.3, 0.26, 0.24, 0.21]


def getScore():
    file = open("Watch-Out/src/main/python/data/data.bin", "rb")
    byte = file.read(1)
    byteScore = bytes()
    while byte:
         byteScore=byteScore+ byte
         byte = file.read(1)
    risBin=FileManager.getToFile()
    risFloat=FileManager.bin_to_float(risBin)
    return str(risFloat)
    
def setEnemy():
    global ENEMY_PG_img
    ENEMY_PG_img = pygame.image.load(os.path.join("Watch-Out/src/main/python/assets/Enemy/enemy.gif"))    #ENEMY_PG_img = pygame.image.load(os.path.join("src/main/python/assets/Enemy/enemy"+ENEMY_NUMBER+".gif")) 
    ENEMY_PG_img=pygame.transform.scale(ENEMY_PG_img, (OWN_PG_W,OWN_PG_H))

def timer():
    global FIRED, isMENU, LOSE
    start = time.time()
    while True:
        if FIRED and not LOSE:
            end = time.time()
            if end-start < float(BESTSCORE):
                f=open("Watch-Out/src/main/python/data/data.bin","wb")
                resString = round(end-start, 2)
                byteResult = FileManager.float_to_bin(resString)            
                f.write(bytearray(byteResult, "utf8"))        
            return
        if isMENU or LOSE:
            return

def OWN_handle_bullet(ENEMY_PG):
    global OWN_bullets, ENEMY_NUMBER
    if OWN_bullets:
        OWN_bullets.y-=BULLET_VEL
        if ENEMY_PG.colliderect(OWN_bullets):
            OWN_bullets=NULL
            ENEMY_NUMBER= str(int(ENEMY_NUMBER)+1)
            draw_winner("hai vinto!", True)
            return
                
def ENEMY_handle_bullet(OWN_PG):
    global ENEMY_bullets, PG_HP
    if ENEMY_bullets:
        ENEMY_bullets.y+=BULLET_VEL
        if OWN_PG.colliderect(ENEMY_bullets):
            ENEMY_bullets=NULL
            PG_HP-=1
            draw_winner("hai perso!", True)
    return

def background_window(OWN_PG_img, OWN_PG, ENEMY_PG, ENEMY_PG_img,EXIT,MENU_MOUSE_POS):
    global ENEMY_bullets,CANFIRE,OWN_bullets,FIRED,ENEMY_NUMBER,PG_HP
    WIN.fill(W) 
    WIN.blit(OWN_PG_img,(OWN_PG.x, OWN_PG.y))
    WIN.blit(ENEMY_PG_img,(ENEMY_PG.x, ENEMY_PG.y))
    draw_text = get_font(18).render("LEVEL "+str(ENEMY_NUMBER), 1, B)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, 55))
    draw_text=get_font(15).render(str(PG_HP), 1, B)
    WIN.blit(draw_text,(965, 55))
    WIN.blit(HP_img,(1000, 50))
    if CANFIRE==True and FIRED ==False:
        draw_text = get_font(100).render("Watch Out!", 1, B)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                        2, HEIGHT/2 - draw_text.get_height()/2))
    if OWN_bullets:
        pygame.draw.rect(WIN,B, OWN_bullets)
    if ENEMY_bullets:
        pygame.draw.rect(WIN,B, ENEMY_bullets)
    EXIT.changeColor(MENU_MOUSE_POS)
    EXIT.update(WIN)
    pygame.display.update() 

def changeLevel():
    global WIDTH, HEIGHT, ENEMY_NUMBER
    WIN.fill(W)
    draw_text1 = get_font(80).render("LEVEL "+str(ENEMY_NUMBER), 1, B)
    WIN.blit(draw_text1, (WIDTH/2 - draw_text1.get_width() /
                        2, HEIGHT/2 - draw_text1.get_height()/2))
    pygame.display.update()
    pygame.time.delay(700)
    return
        
def draw_winner(text, go):
    global ENEMY_NUMBER
    WIN.fill(W) 
    draw_text = get_font(100).render(text, 1, B)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                        2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(800)
    if go:
        changeLevel()
        play()
    else:
        main_menu()

def firetimer():
    global CANFIRE, DIE
    DIE=True
    T=random.uniform(1.5, 3)
    time.sleep(T)
    CANFIRE=True
    Scoretimer=Thread(target=timer, args=())
    Scoretimer.start()
    DIE=False
    return

def ENEMY_FIRE(i,ENEMY_PG):
    global ENEMY_bullets,CANFIRE, FIRED,LEVELDIFF, ENEMY_NUMBER, LOSE, isMENU
    while CANFIRE==False:
        pass
    if ENEMY_NUMBER!="0":
        print (LEVELDIFF[int(ENEMY_NUMBER)])
        time.sleep(LEVELDIFF[int(ENEMY_NUMBER)])
        if CANFIRE and not FIRED and not isMENU:
            LOSE=True
            ENEMY_bullets = pygame.Rect(ENEMY_PG.x + OWN_PG_H//2 -5, ENEMY_PG.y + 40, 10, 5)
            FIRED=True
    return

def play(): 
    global OWN_bullets, CANFIRE, FIRED, DIE, ENEMY_NUMBER,isMENU,LOSE,PG_HP
    if isMENU:
         ENEMY_NUMBER,isMENU,PG_HP="0",False,5
    setEnemy()
    image=pygame.image.load("Watch-Out/src/main/python/assets/Background/Quit Rect.png")
    image=pygame.transform.scale(image, (50,20))
    EXIT = Button(image, pos=(90, 50), text_input="MENU", font=get_font(10), base_color="#d7fcd4", hovering_color="White")
    OWN_PG =pygame.Rect((WIDTH//2)-50, HEIGHT-240, 70, 70)
    ENEMY_PG=pygame.Rect((WIDTH//2)-50, HEIGHT/2-200, 70, 70)
    timer=Thread(target=firetimer, args=())
    clock=pygame.time.Clock()
    run=True
    ENEMYT = Thread(target=ENEMY_FIRE, args=(1,ENEMY_PG))
    while(DIE==True):
        time.sleep(0.2)
    CANFIRE, FIRED, LOSE=False,False,NULL
    ENEMYT.start()
    timer.start()
    if(ENEMY_NUMBER=="0"):
        changeLevel()
    while run:
        clock.tick(FPS)
        key_input = pygame.key.get_pressed() 
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        if(ENEMY_NUMBER=="5"):
            isMENU=True
            draw_winner("GAME OVER!", False)
        if(PG_HP==0):
            isMENU=True
            draw_winner("GAME OVER!", False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if key_input[pygame.K_ESCAPE]:
                if not CANFIRE:
                    ENEMY_NUMBER="0"
                    isMENU=True
                    main_menu()      
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EXIT.checkForInput(MENU_MOUSE_POS):
                    if not CANFIRE:
                        ENEMY_NUMBER="0"
                        isMENU=True
                        main_menu()
                if event.button == 1 and OWN_bullets==NULL:
                    if CANFIRE and not FIRED:
                        OWN_bullets = pygame.Rect(OWN_PG.x + OWN_PG_H//2 -5, OWN_PG.y +5, 10, 5)
                        LOSE=False
                        FIRED=True
                    elif not(CANFIRE and FIRED) :
                        LOSE=True
                        FIRED=True
                        PG_HP-=1
                        draw_winner("hai perso!", True)
                    
        OWN_handle_bullet(ENEMY_PG)
        ENEMY_handle_bullet(OWN_PG)
        background_window(OWN_PG_img, OWN_PG, ENEMY_PG, ENEMY_PG_img,EXIT,MENU_MOUSE_POS)  
    
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
    pos=0
    global BESTSCORE;
    score1 = get_font(20).render("Your best score:", 1, (255,255,0))
    BESTSCORE=float(getScore())
    scoreStr = get_font(18).render(getScore(), 1, (255,255,0))
    while True:
        WIN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Watch-Out/src/main/python/assets/Background/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Watch-Out/src/main/python/assets/Background/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Watch-Out/src/main/python/assets/Background/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        WIN.blit(score1, (900, 200))
        WIN.blit(scoreStr, (1020, 230))
        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            PLAY_BUTTON.changeColorArrow(pos, 0)
            OPTIONS_BUTTON.changeColorArrow(pos, 1)
            QUIT_BUTTON.changeColorArrow(pos, 2)
            button.update(WIN)

        key_input = pygame.key.get_pressed() 
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
            if key_input[pygame.K_UP]:
                if pos==0:
                    pos=2
                else:
                    pos-=1
            if key_input[pygame.K_DOWN]:
                if pos==2:
                    pos=0
                else:
                    pos+=1
            if key_input[pygame.K_SPACE]:
                if pos==0:
                    play()
                if pos==1:
                    options()
                else:
                    pygame.quit()
                    sys.exit()
                
        pygame.display.update(  )

main_menu()