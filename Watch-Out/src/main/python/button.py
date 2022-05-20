G = (0, 255, 0)
import pygame
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
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
            self.isOvered=True
        else:
            self.text = self.font.render( self.text_input, True, self.base_color)
            self.isOvered=False
    
    def setButton(self, position):
        self.changeColorArrow(position, 0)

    def mouseOver (self, position, size, f):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image=pygame.transform.scale(self.image, (int(size[0]*1.05), int(size[1]*1.05)))
            self.font=Button.get_font(int(f*1.15))
            if self.isOvered:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
                return
            self.text = self.font.render(self.text_input, True, self.base_color)
        else:
            self.image=pygame.transform.scale(self.image, (size[0], size[1]))
            self.font=Button.get_font(f)
            if self.isOvered:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
                return
            self.text = self.font.render(self.text_input, True, self.base_color)