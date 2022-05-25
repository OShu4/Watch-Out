G = (0, 255, 0)
import pygame
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, overImage):
        self.image = image
        self.imageSupp=image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.isOvered=False
        self.overImage=overImage

    def get_font(size):
        return pygame.font.Font("Watch-Out/src/main/python/assets/Font/font.ttf", size)

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, G)
        else:
            self.text = self.font.render(self.text_input, True, self.hovering_color)

    def changeColorArrow(self, number, i):
        if number == i:
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            Button.setOver(self)
        else:
            self.text = self.font.render( self.text_input, True, self.base_color)
            Button.unsetOver(self)
    
    def setButton(self, position):
        self.changeColorArrow(position, 0)

    def mouseOver (self, position, f):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image=self.overImage
            self.font=Button.get_font(int(f*1.15))
            if Button.getOver(self):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
        else:
            self.image=self.imageSupp
            self.font=Button.get_font(f)
            if Button.getOver(self):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
                
                
    def setOver(self):
        self.isOvered=True
    
    def unsetOver(self):
        self.isOvered=False
        
    def getOver(self):
        return self.isOvered