import random
from threading import Thread
import time
import os
from asyncio.windows_events import NULL
import pygame
import sys
from button import Button
from fileManager import FileManager
import spritesheet 

pygame.font.init()
pygame.mixer.init()
pygame.init()

#inizializzazione della finestra di gioco. Altezza e largezza; logo e nome della finestra.
WIDTH, HEIGHT = 1290, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption('Watch-Out!')
programIcon = pygame.image.load('assets/Logo/applogo.png')
pygame.display.set_icon(programIcon)

#definizione delle variabili globali. Colori, FPS, tempo di reazione dei nemici, statistiche dei personaggi, bool di controllo, etc.
W, B, R, G, LIGHT_G= (255, 255, 255), (0, 0, 0), (255,0, 0), (0, 255, 0), (184, 218, 186)
FPS = 120
OWN_PG_H, OWN_PG_W, BULLET_VEL,PG_HP = 90, 80, 8,5
ENEMY_PG_W, ENEMY_PG_H= 90, 80
LEVELDIFF = [0, 0.31, 0.28, 0.27, 0.24]
CANFIRE, FIRED, DIE, isMENU, LOSE, BESTSCORE, EASY_DIFF, Return = False, False, False, True, NULL, 0.0, False, False
lastUpdateProt=0.0
lastUpdateEnemy=0.0
PlaySize=370, 130
OptionSize=360,115
gameMusic = pygame.mixer.Sound(os.path.join('assets/Sounds/musicGame.wav'))
gameMusic.set_volume(0.15)

namePg=["Dummy", "Goblin", "Goblin", "Franco", "rafaR"]

#inizializzazione dei PG.
ENEMY_NUMBER = "0"
ENEMY_PG_img = pygame.image
OWN_PG_img = pygame.image.load("assets/Prot/prot.png").convert_alpha()
OWN_PG_img = spritesheet.SpriteSheet(OWN_PG_img)

#separazione delle sprite dal PNG
animationListOwnPg=[]
for x in range (2):
    animationListOwnPg.append(OWN_PG_img.get_image(x, 24, 27, 3, ((255,255,255,0))))

#oggetti e instanze utili
HP_img = pygame.image.load(os.path.join("assets/Background/hp.png"))
HP_img = pygame.transform.scale(HP_img, (30, 25))
OWN_bullets, ENEMY_bullets = NULL, NULL
image=pygame.image.load("assets/Background/PlayButton.png")
Playimage=pygame.transform.scale(image, PlaySize)
overImageP=pygame.transform.scale(Playimage, (int(PlaySize[0]*1.05), int(PlaySize[1]*1.05)))
overImageO=pygame.transform.scale(Playimage, (int(OptionSize[0]*1.05), int(OptionSize[1]*1.05)))
imageOption = pygame.transform.scale(Playimage, OptionSize)
animationListEnemy=[]

#richiamata restituisce un font
def get_font(size):
    return pygame.font.Font("assets/Font/font.ttf", size)

def setEnemy():
    global ENEMY_PG_img, animationListEnemy, ENEMY_NUMBER, ENEMY_PG_W
    pathJson="assets/Enemy/Json/Enemy"+ ENEMY_NUMBER +".json"
    pathImg="assets/Enemy/Enemy"+ENEMY_NUMBER+".png"
    if ENEMY_NUMBER=="2":
        pathImg="assets/Enemy/Enemy1.png"
        pathJson="assets/Enemy/Json/Enemy1.json"
    ENEMY_PG_img = pygame.image.load(pathImg)
    ENEMY_PG_img = spritesheet.SpriteSheet(ENEMY_PG_img)


    size=FileManager.JsonReader(pathJson)
    animationListEnemy.clear()
    for x in range (2):
        animationListEnemy.append(ENEMY_PG_img.get_image(x, size[0], size[1], 10, ((255,255,255,0))))
    
#conta il tempo di reazione che il player impiega nel cliccare dal via. se il tempo batte il record viene scritto nel file data.bin
def timer():
    global FIRED, isMENU, LOSE, DIE
    start = time.time()
    while not isMENU:
        if isMENU or LOSE:
            return
        if FIRED and not LOSE:
            end = time.time()
            reaction=round((end-start)-((end-start)/7),2)
            if reaction < float(BESTSCORE) or BESTSCORE == 0.0:
                FileManager.writeTO(reaction, "data")
            return

#gestisce i proiettili del giocatore e la collisione con il nemico
def OWN_handle_bullet(ENEMY_PG):
    global OWN_bullets, ENEMY_NUMBER

    if OWN_bullets:
        OWN_bullets.y -= BULLET_VEL
        if ENEMY_PG.colliderect(OWN_bullets):
            hit = pygame.mixer.Sound(os.path.join('assets/Sounds/hit.wav'))
            pygame.mixer.Sound.play(hit)
            OWN_bullets = NULL
            ENEMY_NUMBER = str(int(ENEMY_NUMBER)+1)
            victory = pygame.mixer.Sound(os.path.join('assets/Sounds/victoryLv.wav'))
            victory.set_volume(0.4)
            pygame.mixer.Sound.play(victory)
            draw_winner("hai vinto!", True, G)
    return

#gestisce i proiettili del NPC e la collisione con il giocatore
def ENEMY_handle_bullet(OWN_PG):
    global ENEMY_bullets, PG_HP

    if ENEMY_bullets:
        ENEMY_bullets.y += BULLET_VEL
        if OWN_PG.colliderect(ENEMY_bullets):
            hit = pygame.mixer.Sound(os.path.join('assets/Sounds/lancia.wav'))
            pygame.mixer.Sound.play(hit)
            ENEMY_bullets = NULL
            PG_HP -= 1
            lose = pygame.mixer.Sound(os.path.join('assets/Sounds/loseLv.wav'))
            lose.set_volume(0.8)
            pygame.mixer.Sound.play(lose)
            draw_winner("hai perso!", True, R)
    return

#crea l'animazione dei vari PG alternando i frame
def animation(OWN_PG, ENEMY_PG):
    global lastUpdateProt, lastUpdateEnemy, animationListOwnPg,animationListEnemy, ENEMY_PG_W
    animationCooldown=370
    frameN=0
    currentTime = pygame.time.get_ticks()
    
    if currentTime-lastUpdateProt >= animationCooldown:
        frameN+=1
        lastUpdateProt=currentTime
        if frameN >= len(animationListOwnPg):
            frameN=0
    frame=pygame.transform.scale(animationListOwnPg[frameN], (OWN_PG_W, OWN_PG_H))
    WIN.blit(frame, (OWN_PG.x, OWN_PG.y))
    frame=pygame.transform.scale(animationListEnemy[frameN], (ENEMY_PG_W, ENEMY_PG_H))
    WIN.blit(frame, (ENEMY_PG.x, ENEMY_PG.y))
    return

#si occupa di disegnare la finestra di gioco durante play
def background_window(OWN_PG, ENEMY_PG, EXIT, MENU_MOUSE_POS, ):

    global ENEMY_bullets, CANFIRE, OWN_bullets, FIRED, ENEMY_NUMBER, PG_HP, namePg
    #crea i proiettili del player

    WIN.fill(W)
    backImage=pygame.image.load(os.path.join("assets/Background/gameBack.png"))
    backImage=pygame.transform.scale(backImage,(1290, 720))
    WIN.blit(backImage, (0,0))
    if OWN_bullets:
        pygame.draw.rect(WIN, B, OWN_bullets)
    animation(OWN_PG, ENEMY_PG)

    draw_text = get_font(15).render(str(PG_HP), 1, B)
    WIN.blit(draw_text, (965, 55))
    WIN.blit(HP_img, (1000, 50))
    levelText = get_font(28).render(namePg[int(ENEMY_NUMBER)], 1,"#57a3f2")
    WIN.blit(levelText, (WIDTH/2-65, 100))

    draw_text = get_font(18).render("LEVEL "+str(ENEMY_NUMBER), 1, B)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, 55))
    #scrive Watch-Out! 
    if CANFIRE == True and FIRED == False:
        draw_text = get_font(100).render("Watch Out!", 1, "#db3412")
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))

    #disegna i proiettili degli NPC                          
    if ENEMY_bullets:
        pygame.draw.rect(WIN, B, ENEMY_bullets)

    EXIT.changeColor(MENU_MOUSE_POS)
    EXIT.update(WIN)

    pygame.display.update()
    return
    
#fa la transizione di cambio livello
def changeLevel():
    global WIDTH, HEIGHT, ENEMY_NUMBER

    WIN.fill(W)
    draw_text1 = get_font(80).render("LEVEL "+str(ENEMY_NUMBER), 1, B)
    WIN.blit(draw_text1, (WIDTH/2 - draw_text1.get_width() / 2, HEIGHT/2 - draw_text1.get_height()/2))
    time=750
    if ENEMY_NUMBER=="4":
        draw_text1 = get_font(32).render("Solo tu puoi fermarti!", 1, R)
        WIN.blit(draw_text1, (WIDTH/2 - draw_text1.get_width() / 2, HEIGHT/2+100 - draw_text1.get_height()/2))
        time=1700
    pygame.display.update()
    pygame.time.delay(time)
    pygame.event.clear()
    return

#scrive il vincitore e, a seconda dei casi, riporta a play o a main_menu
def draw_winner(text, go, color):
    global ENEMY_NUMBER, PG_HP, Return, CANFIRE

    WIN.fill(W)
    draw_text = get_font(100).render(text, 1, color)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(900)
    if not go or Return:
        Return=False
        CANFIRE=False
        toMenu()
    if not (ENEMY_NUMBER == "5" or PG_HP == 0):
        changeLevel()
    pygame.event.clear()
    play(ENEMY_NUMBER)

#dorme un tempo casuale e poi da il via libera al fuoco con "WATCH OUT", se il giocatore spara prima perde
def firetimer():
    global CANFIRE, DIE, isMENU, FIRED

    DIE = True
    T = random.uniform(1.5, 3)
    time.sleep(T-0.2)
    if not isMENU and not FIRED:    
        fightSounds=pygame.mixer.Sound(os.path.join('assets/Sounds/fight.wav'))
        fightSounds.play()
        time.sleep(0.2)
        CANFIRE = True

        Scoretimer = Thread(target=timer, args=())
        Scoretimer.start()
    DIE = False
    return

#gestisce il tempo di attesa del NPC e la creazione del proiettile.
def ENEMY_FIRE(i,ENEMY_PG):
    global ENEMY_bullets, CANFIRE, FIRED, LEVELDIFF, ENEMY_NUMBER, LOSE, isMENU, EASY_DIFF, DIE
    while CANFIRE == False and not isMENU:
        pass
    if ENEMY_NUMBER == "0":
        return
    if EASY_DIFF:
        time.sleep(0.38)
    else:
        time.sleep(LEVELDIFF[int(ENEMY_NUMBER)])
    if CANFIRE and not FIRED and not isMENU:
        LOSE = True
        ENEMY_bullets = pygame.Rect(ENEMY_PG.x + OWN_PG_H//2 - 5, ENEMY_PG.y + 40, 10, 5)
        FIRED = True
    return

#controlla se il giocatore puo sparare e, nel caso, genera il proiettile
def check_fire(OWN_PG):
    global CANFIRE, FIRED, OWN_bullets, LOSE, PG_HP
    if CANFIRE and not FIRED:
        OWN_bullets = pygame.Rect(OWN_PG.x + OWN_PG_H//2 - 5, OWN_PG.y + 5, 10, 5)
        Shot = pygame.mixer.Sound(os.path.join('assets/Sounds/pistola.wav'))
        pygame.mixer.Sound.play(Shot)
        LOSE = False
        FIRED = True
    elif not(CANFIRE and FIRED):
        LOSE = True
        FIRED = True
        PG_HP -= 1
        lose = pygame.mixer.Sound(os.path.join('assets/Sounds/loseLv.wav'))
        pygame.mixer.Sound.play(lose)
        draw_winner("hai perso!", True, R)
    return

#si occupa dell'uscita dalla fase di gioco per arrivare nel menu
def toMenu():
    global CANFIRE, ENEMY_NUMBER, isMENU, gameMusic
    gameMusic.stop()
    if not CANFIRE:
        ENEMY_NUMBER = "0"
        isMENU = True
        main_menu()
    return
                              
#funzione che gestisce il gioco in se
def play(N):
    global OWN_bullets, CANFIRE, FIRED, DIE, ENEMY_NUMBER, isMENU, LOSE, PG_HP, Return, lastUpdateProt, lastUpdateEnemy, gameMusic

    ENEMY_NUMBER=N
    #gestione dei casi, come vittoria e sconfitta, e l'arrivo dal menu
    if isMENU:
        pygame.mixer.Sound.play(gameMusic, -1)
        isMENU, PG_HP, Return = False, 5, False
        if ENEMY_NUMBER!="0":
            Return=True
        changeLevel()
    if ENEMY_NUMBER == "5":
        isMENU = True
        Return=False
        if not EASY_DIFF:
            fin = ' '.join(format(ord(x), 'b') for x in "completed")
            FileManager.writeTO(fin, "fin")
        WinGm = pygame.mixer.Sound(os.path.join('assets/Sounds/WinGame.wav'))
        WinGm.play()
        draw_winner("GAME OVER!", False, G)
    if PG_HP == 0:
        loseGm = pygame.mixer.Sound(os.path.join('assets/Sounds/loseGm.wav'))
        loseGm.play()
        isMENU = True
        draw_winner("GAME OVER!", False, R)

    #attesa che i thread in esecuzione muoiano
    while(DIE == True):
        time.sleep(0.2)
    
    #inizializazzione di: Nemico, Bottoni utili, Thread, etc. 
    setEnemy()
    image = pygame.image.load("assets/Background/Quit Rect.png")
    image = pygame.transform.scale(image, (50, 20))
    EXIT = Button(image, pos=(90, 50), text_input="MENU", font=get_font(10), base_color="#d7fcd4", hovering_color="White", overImage=image)
    OWN_PG = pygame.Rect((WIDTH//2)-50, HEIGHT-110, 70, 70)
   
    ENEMY_PG = pygame.Rect((WIDTH//2)-50, HEIGHT/2+50, 70, 70)
    
    timer = Thread(target=firetimer, args=())
    clock = pygame.time.Clock()
    ENEMYT = Thread(target=ENEMY_FIRE, args=(1,ENEMY_PG))

    CANFIRE, FIRED, LOSE = False, False, NULL
    ENEMYT.start()
    timer.start()

    lastUpdateProt=pygame.time.get_ticks()
    lastUpdateEnemy=pygame.time.get_ticks()

    #While che gestisce il livello in se. Si ripete 120 volte al secondo (FPS)
    while True:

        clock.tick(FPS)
        key_input = pygame.key.get_pressed()
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        #gestione eventi, come click del mouse e key premuete
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                isMENU = True
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

        #funzioni di gestione finestra e azzioni
        OWN_handle_bullet(ENEMY_PG)
        ENEMY_handle_bullet(OWN_PG)
        background_window(OWN_PG, ENEMY_PG, EXIT, MENU_MOUSE_POS)

#richiamata su click del pulsante select level. permette di decidere il livello da giocare. Utilizzabile solo se il gioco e' gia stato precedentemente completato
def set_level(): 
    global overImageP, overImageO, imageOption, namePG
    CurrentLevel=0

    #inizializzazione e ridimensionazione delle immagini e conseguente uso delle stesse nella creazione di pulsanti 
    BackGround=pygame.image.load("assets/Background/settingBackground.png")
    BackGroundSetLevel=pygame.image.load("assets/Background/levelSet.png")
    arrowImageUp=pygame.image.load("assets/Background/Arrow.png")

    BackGround=pygame.transform.scale(BackGround, (1290, 720))
    BackGroundSetLevel=pygame.transform.scale(BackGroundSetLevel, (700, 430))     
    arrowImageUp=pygame.transform.scale(arrowImageUp, (150,80))
    arrowImageDown=pygame.transform.rotate(arrowImageUp, 180)
    arrowImageDown=pygame.transform.scale(arrowImageDown, (150,80))
    arrowImageUpOver=pygame.transform.scale(arrowImageUp, (160,85))
    arrowImageDownOver=pygame.transform.scale(arrowImageDown, (160,85))

    PLAY_BUTTON = Button(imageOption, pos=(640, 560), text_input="PLAY", font=get_font(40), base_color=W, hovering_color="#ddffd0", overImage=overImageP)
    ButtonLevelUp = Button(arrowImageUp, pos= (WIDTH/2+160, HEIGHT/2+100), text_input="", font=get_font(30), base_color=B, hovering_color="#ddffd0",overImage=arrowImageUpOver) 
    ButtonLevelDown = Button(arrowImageDown, pos= (WIDTH/2-158, HEIGHT/2+100), text_input="", font=get_font(30), base_color=B, hovering_color="#ddffd0",overImage=arrowImageDownOver) 

    image = pygame.image.load("assets/Background/Quit Rect.png")
    image = pygame.transform.scale(image, (50, 20))
    EXIT = Button(image, pos=(90, 50), text_input="MENU", font=get_font(10), base_color="#d7fcd4", hovering_color="White", overImage=image)

    WIN.blit(BackGround, (0,0))

    #gestisce l'aggiornarsi del menu
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        WIN.blit(BackGround, (0,0))
        ShowName=get_font(32).render(namePg[CurrentLevel], 1,"#db3412")
        levelText = get_font(22).render(("LEVEL  "+ str(CurrentLevel)), 1,"#57a3f2")
        for button in [ButtonLevelUp, ButtonLevelDown, PLAY_BUTTON]:
            button.mouseOver(OPTIONS_MOUSE_POS, 45)
            button.update(WIN)

        EXIT.changeColor(OPTIONS_MOUSE_POS)
        EXIT.update(WIN)
        WIN.blit(BackGroundSetLevel, (WIDTH/2-340, HEIGHT/2-250))
        WIN.blit(ShowName, (WIDTH/2-70, HEIGHT/2-40))
        WIN.blit(levelText, (WIDTH/2-70, HEIGHT/2-100))
        key_input = pygame.key.get_pressed()

        #prende gli eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EXIT.checkForInput(OPTIONS_MOUSE_POS):
                    CurrentLevel=0
                    main_menu()
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

#controlla se il gioco sia gia stato completato
def checkForSelect(music):
    if FileManager.bin_to_str("fin")==" completed":
        music.stop()
        set_level()
    else:
        draw_text = get_font(30).render("Devi prima completare il gioco!", 1, R,"#ddffd0")
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2, (HEIGHT/2 - draw_text.get_height()/2)+15))
        pygame.display.update()
        pygame.time.delay(400)
    return

#menu del gioco, permette di viaggiare nelle funzioni di gioco
def main_menu():

    pos, count = 0, 0
    global BESTSCORE, EASY_DIFF, overImageO, overImageP, imageOption, Playimage, isMENU
    isMENU=True
    bg_img = pygame.image.load(os.path.join("assets/Background/Background.png"))
    bg = pygame.transform.scale(bg_img, (1290, 720))
    WatchOutImage= pygame.image.load("assets/Background/WatchOutPlace.png")
    
    music = pygame.mixer.Sound(os.path.join('assets/Sounds/MenuMusic.wav'))
    music.set_volume(0.1)
    pygame.mixer.Sound.play(music, -1)

    #prende il miglior score dal file data.bin
    score1 = get_font(20).render("Your best score:", 1, "#cda434")
    BESTSCORE = FileManager.getScore()
    scoreStr = get_font(18).render(str(BESTSCORE), 1,"#cda434")

    MENU_TEXT = get_font(30).render("MAIN MENU", True, "#cda434")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 40))

    WatchOutImage=pygame.transform.scale(WatchOutImage, (900, 300))
    WATCH_OUT = get_font(70).render("WATCH OUT!", True, "#db3412")
    TITLE_RECT = WATCH_OUT.get_rect(center=(640, 150))
    
    PLAY_BUTTON = Button(Playimage, pos=(630, 310), text_input="PLAY", font=get_font(50), base_color=W, hovering_color="#ddffd0",overImage=overImageP)
    SELECT_LEVEL = Button(imageOption, pos=(870, 440), text_input="SELECT LEVEL", font=get_font(26), base_color=W, hovering_color="#ddffd0", overImage=overImageO)
    QUIT_BUTTON = Button(imageOption, pos=(640, 560), text_input="QUIT", font=get_font(45), base_color=W, hovering_color="#ddffd0",overImage=overImageO)
    CHANGE_DIFFICULT = Button(imageOption, pos=(400, 440), text_input="SET EASY", font=get_font(26), base_color=W, hovering_color="#ddffd0",overImage=overImageO)

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        SIZE= [50, 25, 25, 40]

        #background dinamico che si muove
        WIN.blit(bg, (count, 0))
        WIN.blit(bg, (WIDTH+count, 0))
        if count == -WIDTH:
            WIN.blit(bg, (WIDTH+count, 0))
            count = 0
        count -= 1

        i=0
        for button in [PLAY_BUTTON, CHANGE_DIFFICULT,SELECT_LEVEL, QUIT_BUTTON]:
            if EASY_DIFF:
                CHANGE_DIFFICULT.base_color = G
                CHANGE_DIFFICULT.hovering_color = "#95c799"
            else:
                CHANGE_DIFFICULT.base_color = W
                CHANGE_DIFFICULT.hovering_color = "#ddffd0"
            button.mouseOver(MENU_MOUSE_POS,SIZE[i])
            button.changeColorArrow(pos, i)
            button.update(WIN)
            i+=1
        
        #disegno delle componenti del menu sulla finestra di gioco
        WIN.blit(score1, (900, 270))
        WIN.blit(scoreStr, (1020, 305))
        WIN.blit(MENU_TEXT, MENU_RECT)
        WIN.blit(WatchOutImage,(180, -55))
        WIN.blit(WATCH_OUT, TITLE_RECT)
        pygame.display.update()
        
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
                    music.stop()
                    play("0")
                elif CHANGE_DIFFICULT.checkForInput(MENU_MOUSE_POS):
                    EASY_DIFF=not EASY_DIFF
                elif SELECT_LEVEL.checkForInput(MENU_MOUSE_POS):
                    checkForSelect(music)
            
            #gestione del movimento tramite freccette e spacebar
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
                        music.stop()
                        play("0")
                    elif pos == 1:
                        EASY_DIFF=not EASY_DIFF
                    elif pos == 2:
                        checkForSelect(music)
                    else:
                        pygame.quit()
                        sys.exit()
                        
            pygame.event.clear()

main_menu()