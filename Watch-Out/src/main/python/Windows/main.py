import random
from threading import Thread
import time
import os
from asyncio.windows_events import NULL
import pygame
import sys
sys.path.append("Watch-Out/src/main/python")
from button import Button
from fileManager import FileManager

pygame.font.init()
pygame.mixer.init()
pygame.init()
WIDTH, HEIGHT = 1290, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.image.load("Watch-Out/src/main/python/assets/Background/Background.png")
BG= pygame.transform.scale(BG, (1290, 720))
def get_font(size):
    return pygame.font.Font("Watch-Out/src/main/python/assets/Font/font.ttf", size)

W, B, R, G, LIGHT_G = (255, 255, 255), (0, 0, 0), (255,0, 0), (0, 255, 0), (184, 218, 186)
FPS = 90
OWN_PG_H, OWN_PG_W, BULLET_VEL = 90, 80, 8
ENEMY_NUMBER = "0"
ENEMY_PG_img = pygame.image
OWN_PG_img = pygame.image.load(os.path.join(
    "Watch-Out/src/main/python/assets/Prot/prot.gif"))
OWN_PG_img = pygame.transform.scale(OWN_PG_img, (OWN_PG_W, OWN_PG_H))
HP_img = pygame.image.load(os.path.join(
    "Watch-Out/src/main/python/assets/Background/hp.png"))
HP_img = pygame.transform.scale(HP_img, (30, 25))
OWN_bullets, ENEMY_bullets = NULL, NULL
CANFIRE, FIRED, DIE, isMENU, LOSE, BESTSCORE, EASY_DIFF = False, False, False, True, NULL, 0.0, False
PG_HP = 5
LEVELDIFF = [0, 0.3, 0.27, 0.26, 0.23]


def setEnemy():
    global ENEMY_PG_img
    # ENEMY_PG_img = pygame.image.load(os.path.join("src/main/python/assets/Enemy/enemy"+ENEMY_NUMBER+".gif"))
    ENEMY_PG_img = pygame.image.load(os.path.join("Watch-Out/src/main/python/assets/Enemy/enemy.gif"))
    ENEMY_PG_img = pygame.transform.scale(ENEMY_PG_img, (OWN_PG_W, OWN_PG_H))


def timer():
    global FIRED, isMENU, LOSE
    start = time.time()
    while True:
        if isMENU or LOSE:
            return
        if FIRED and not LOSE:
            end = time.time()
            if end-start < float(BESTSCORE) or BESTSCORE == 0.0:
                FileManager.writeTO(float(end), start, "data")
            return


def OWN_handle_bullet(ENEMY_PG):
    global OWN_bullets, ENEMY_NUMBER

    if OWN_bullets:
        OWN_bullets.y -= BULLET_VEL
        if ENEMY_PG.colliderect(OWN_bullets):
            OWN_bullets = NULL
            ENEMY_NUMBER = str(int(ENEMY_NUMBER)+1)
            draw_winner("hai vinto!", True, G)
    return


def ENEMY_handle_bullet(OWN_PG):
    global ENEMY_bullets, PG_HP

    if ENEMY_bullets:
        ENEMY_bullets.y += BULLET_VEL
        if OWN_PG.colliderect(ENEMY_bullets):
            ENEMY_bullets = NULL
            PG_HP -= 1
            draw_winner("hai perso!", True, R)
    return


def background_window(OWN_PG_img, OWN_PG, ENEMY_PG, ENEMY_PG_img, EXIT, MENU_MOUSE_POS):

    global ENEMY_bullets, CANFIRE, OWN_bullets, FIRED, ENEMY_NUMBER, PG_HP
    WIN.fill(W)
    backImage=pygame.image.load(os.path.join("Watch-Out/src/main/python/assets/Background/gameBack.png"))
    backImage=pygame.transform.scale(backImage,(1290, 720))
    WIN.blit(backImage, (0,0))
    WIN.blit(OWN_PG_img, (OWN_PG.x, OWN_PG.y))
    WIN.blit(ENEMY_PG_img, (ENEMY_PG.x, ENEMY_PG.y))

    draw_text = get_font(15).render(str(PG_HP), 1, B)
    WIN.blit(draw_text, (965, 55))
    WIN.blit(HP_img, (1000, 50))

    draw_text = get_font(18).render("LEVEL "+str(ENEMY_NUMBER), 1, B)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, 55))

    if CANFIRE == True and FIRED == False:
        draw_text = get_font(100).render("Watch Out!", 1, B)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                             2, HEIGHT/2 - draw_text.get_height()/2))
                             
    if OWN_bullets:
        pygame.draw.rect(WIN, B, OWN_bullets)

    if ENEMY_bullets:
        pygame.draw.rect(WIN, B, ENEMY_bullets)

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
    pygame.event.clear()
    return


def draw_winner(text, go, color):
    global ENEMY_NUMBER, PG_HP

    WIN.fill(W)
    draw_text = get_font(100).render(text, 1, color)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(800)
    if not go:
        main_menu()
    if not (ENEMY_NUMBER == "5" or PG_HP == 0):
        changeLevel()
    pygame.event.clear()
    play(ENEMY_NUMBER)


def firetimer():
    global CANFIRE, DIE

    DIE = True
    T = random.uniform(1.5, 3)
    time.sleep(T)
    CANFIRE = True
    Scoretimer = Thread(target=timer, args=())
    Scoretimer.start()
    DIE = False
    return


def ENEMY_FIRE(i, ENEMY_PG):
    global ENEMY_bullets, CANFIRE, FIRED, LEVELDIFF, ENEMY_NUMBER, LOSE, isMENU, EASY_DIFF
    while CANFIRE == False:
        pass

    if ENEMY_NUMBER == "0":
        return
    if EASY_DIFF:
        time.sleep(0.38 )
    else:
        time.sleep(LEVELDIFF[int(ENEMY_NUMBER)])
    if CANFIRE and not FIRED and not isMENU:
        LOSE = True
        ENEMY_bullets = pygame.Rect(ENEMY_PG.x + OWN_PG_H//2 - 5, ENEMY_PG.y + 40, 10, 5)
        FIRED = True
    return


def check_fire(OWN_PG):
    global CANFIRE, FIRED, OWN_bullets, LOSE, PG_HP
    if CANFIRE and not FIRED:
        OWN_bullets = pygame.Rect(
            OWN_PG.x + OWN_PG_H//2 - 5, OWN_PG.y + 5, 10, 5)
        LOSE = False
        FIRED = True
    elif not(CANFIRE and FIRED):
        LOSE = True
        FIRED = True
        PG_HP -= 1
        draw_winner("hai perso!", True, R)
    return

def toMenu():
    global CANFIRE, ENEMY_NUMBER, isMENU

    if not CANFIRE:
        ENEMY_NUMBER = "0"
        isMENU = True
        main_menu()
    return


def play(N):

    global OWN_bullets, CANFIRE, FIRED, DIE, ENEMY_NUMBER, isMENU, LOSE, PG_HP
    ENEMY_NUMBER=N
    if isMENU:
        isMENU, PG_HP = False, 5
        changeLevel()

    if ENEMY_NUMBER == "5":
        isMENU = True
        if not EASY_DIFF:
            fin = ' '.join(format(ord(x), 'b') for x in "completed")
            FileManager.writeTO(fin, 0, "fin")
        draw_winner("GAME OVER!", False, G)
    


    while(DIE == True):
        time.sleep(0.2)

    setEnemy()
    image = pygame.image.load("Watch-Out/src/main/python/assets/Background/Quit Rect.png")
    image = pygame.transform.scale(image, (50, 20))
    EXIT = Button(image, pos=(90, 50), text_input="MENU", font=get_font(10), base_color="#d7fcd4", hovering_color="White")
    OWN_PG = pygame.Rect((WIDTH//2)-50, HEIGHT-240, 70, 70)
    ENEMY_PG = pygame.Rect((WIDTH//2)-50, HEIGHT/2-200, 70, 70)
    timer = Thread(target=firetimer, args=())
    clock = pygame.time.Clock()
    ENEMYT = Thread(target=ENEMY_FIRE, args=(1, ENEMY_PG))

    CANFIRE, FIRED, LOSE = False, False, NULL
    ENEMYT.start()
    timer.start()


    while True:

        clock.tick(FPS)
        key_input = pygame.key.get_pressed()
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        if PG_HP == 0:
            isMENU = True
            draw_winner("GAME OVER!", False, R)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if key_input[pygame.K_ESCAPE]:
                toMenu()

            if key_input[pygame.K_SPACE]:
                check_fire(OWN_PG)

            if event.type == pygame.MOUSEBUTTONDOWN:
    
                if EXIT.checkForInput(MENU_MOUSE_POS):
                    toMenu()
                if event.button == 1 and OWN_bullets == NULL:
                    check_fire(OWN_PG)

            pygame.event.clear()

        OWN_handle_bullet(ENEMY_PG)
        ENEMY_handle_bullet(OWN_PG)
        background_window(OWN_PG_img, OWN_PG, ENEMY_PG,ENEMY_PG_img, EXIT, MENU_MOUSE_POS)



def change_difficult():
    global EASY_DIFF
    if EASY_DIFF:
        EASY_DIFF = False
    else:
        EASY_DIFF = True
    return

def set_level():

    CurrentLevel=0
    BackGroundSetLevel=pygame.image.load("Watch-Out/src/main/python/assets/Background/levelSet.png")
    arrowImageUp=pygame.image.load("Watch-Out/src/main/python/assets/Background/Arrow.png")
    image=pygame.image.load("Watch-Out/src/main/python/assets/Background/PlayButton.png")
    image=pygame.transform.scale(image, (300, 100))
    BackGroundSetLevel=pygame.transform.scale(BackGroundSetLevel, (700, 430))     
    arrowImageUp=pygame.transform.scale(arrowImageUp, (150,80))
    arrowImageDown=pygame.transform.rotate(arrowImageUp, 180)
    arrowImageDown=pygame.transform.scale(arrowImageDown, (150,80))

    PLAY_BUTTON = Button(image, pos=(640, 560), text_input="PLAY", font=get_font(30), base_color=W, hovering_color="#ddffd0")
    ButtonLevelUp = Button(arrowImageUp, pos= (WIDTH/2+160, HEIGHT/2+100), text_input="", font=get_font(30), base_color=B, hovering_color="#ddffd0") 
    ButtonLevelDown = Button(arrowImageDown, pos= (WIDTH/2-158, HEIGHT/2+100), text_input="", font=get_font(30), base_color=B, hovering_color="#ddffd0") 

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        WIN.fill("white")
        levelText = get_font(22).render(("LEVEL  "+ str(CurrentLevel)), 1,"#57a3f2")
        for button in [ButtonLevelUp, ButtonLevelDown, PLAY_BUTTON]:
            button.update(WIN)

        WIN.blit(BackGroundSetLevel, (WIDTH/2-340, HEIGHT/2-250))
        WIN.blit(levelText, (WIDTH/2-70, HEIGHT/2-100))
        key_input = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    play(str(CurrentLevel))
                elif ButtonLevelUp.checkForInput(OPTIONS_MOUSE_POS):
                    if(CurrentLevel!=4):
                        CurrentLevel+=1
                elif ButtonLevelDown.checkForInput(OPTIONS_MOUSE_POS):
                    if(CurrentLevel!=0):
                        CurrentLevel-=1


            if pygame.KEYDOWN:
                if key_input[pygame.K_ESCAPE]:
                    main_menu()

            pygame.display.update()

def checkForSelect():
    if FileManager.bin_to_str("fin")==c" completed":
        set_level()
    else:
        draw_text = get_font(30).render("Devi prima completare il gioco!", 1, R,"#ddffd0")
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2, (HEIGHT/2 - draw_text.get_height()/2)+15))
        pygame.display.update()
        pygame.time.delay(400)
    return

def main_menu():
    PlaySize=370, 130
    OptionSize=360,110
    pos = 0
    global BESTSCORE, EASY_DIFF
    score1 = get_font(20).render("Your best score:", 1, "#cda434")
    BESTSCORE = FileManager.getScore()
    scoreStr = get_font(18).render(str(BESTSCORE), 1,"#cda434")

    while True:
        WIN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("MAIN MENU", True, "#cda434")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 40))
        WatchOutImage= pygame.image.load("Watch-Out/src/main/python/assets/Background/WatchOutPlace.png")
        WatchOutImage=pygame.transform.scale(WatchOutImage, (900, 300))
        WATCH_OUT = get_font(70).render("WATCH OUT!", True, "#db3412")
        TITLE_RECT = WATCH_OUT.get_rect(center=(640, 150))
        image=pygame.image.load("Watch-Out/src/main/python/assets/Background/PlayButton.png")
        image=pygame.transform.scale(image, PlaySize)
        PLAY_BUTTON = Button(image, pos=(630, 310), text_input="PLAY", font=get_font(50), base_color=W, hovering_color="#ddffd0")
        image = pygame.transform.scale(image, OptionSize)
        CHANGE_DIFFICULT = Button(image, pos=(400, 440), text_input="SET EASY", font=get_font(25), base_color=W, hovering_color="#ddffd0")
        SELECT_LEVEL = Button(image, pos=(870, 440), text_input="SELECT LEVEL", font=get_font(25), base_color=W, hovering_color="#ddffd0")
        QUIT_BUTTON = Button(image, pos=(640, 560), text_input="QUIT", font=get_font(45), base_color=W, hovering_color="#ddffd0")

        WIN.blit(score1, (900, 270))
        WIN.blit(scoreStr, (1020, 305))
        WIN.blit(MENU_TEXT, MENU_RECT)
        WIN.blit(WatchOutImage,(180, -55))
        WIN.blit(WATCH_OUT, TITLE_RECT)
        SIZE= (PlaySize, 50),(OptionSize, 25),(OptionSize, 25),(OptionSize, 45)

        i=0
        for button in [PLAY_BUTTON, CHANGE_DIFFICULT,SELECT_LEVEL, QUIT_BUTTON]:
            if EASY_DIFF:
                CHANGE_DIFFICULT.base_color = G
                CHANGE_DIFFICULT.hovering_color = "#95c799"
            button.mouseOver(MENU_MOUSE_POS,SIZE[i][0],SIZE[i][1])
            button.changeColorArrow(pos, i)
            button.update(WIN)
            i+=1

        key_input = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                elif PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play("0")
                elif CHANGE_DIFFICULT.checkForInput(MENU_MOUSE_POS):
                    change_difficult()
                elif SELECT_LEVEL.checkForInput(MENU_MOUSE_POS):
                    checkForSelect()
               

            if pygame.KEYDOWN:
                if key_input[pygame.K_UP]:
                    if pos == 0:
                        pos = 3
                    else:
                        pos -= 1
                if key_input[pygame.K_DOWN]:
                    if pos == 3:
                        pos = 0
                    else:
                        pos += 1
                if key_input[pygame.K_SPACE]:
                    if pos == 0:
                        play("0")
                    elif pos == 1:
                        change_difficult()
                    elif pos == 2:
                        checkForSelect()
                    else:
                        pygame.quit()
                        sys.exit()
            pygame.event.clear()

        pygame.display.update()

main_menu()