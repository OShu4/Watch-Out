from asyncio import events
import pygame
import os

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test1")
W=(255, 255, 255) 
B=(0,0,0)
FPS=60
OWN_PG_H=70
OWN_PG_W=70
OWN_PG_img = pygame.image.load(os.path.join("circle.png"))
OWN_PG_img=pygame.transform.scale(OWN_PG_img, (OWN_PG_W,OWN_PG_H))
# ENEMY_PG = pygame.image.load(os.path.join("square.jpg")) 
VEL=5;
BULLET_VEL=10
def OWN_PG_movement(keys_pressed, OWN_PG):
    if keys_pressed[pygame.K_a]:
        OWN_PG.x-= VEL
    if keys_pressed[pygame.K_d]:
        OWN_PG.x+= VEL
    if keys_pressed[pygame.K_w]:
            OWN_PG.y-= VEL
    if keys_pressed[pygame.K_s]:
        OWN_PG.y+= VEL

def handle_bullet(bullets):
    for bullet in bullets:
        bullet.y-=BULLET_VEL
        if bullet.y < 0:
            bullets.remove(bullet)

    

def background_window(OWN_PG_img, OWN_PG, bullets):
    WIN.fill(W) 
    WIN.blit(OWN_PG_img,(OWN_PG.x, OWN_PG.y))
    for bullet in bullets:
        pygame.draw.rect(WIN,B, bullet)
    pygame.display.update() 

def main():
    OWN_PG =pygame.Rect((WIDTH//2)-50, 100, 70, 70)
    clock=pygame.time.Clock()
    bullets = []
    run=True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
              if event.button == 1 and len(bullets)<1:
                    bullet = pygame.Rect(OWN_PG.x + OWN_PG_H//2 -5, OWN_PG.y +5, 10, 5)
                    bullets.append(bullet)

        keys_pressed=pygame.key.get_pressed()
        handle_bullet(bullets)
        OWN_PG_movement(keys_pressed, OWN_PG)
        background_window(OWN_PG_img, OWN_PG, bullets)  

    pygame.quit()

if __name__=="__main__":
    main()