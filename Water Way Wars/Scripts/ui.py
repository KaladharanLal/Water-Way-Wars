import pygame


class Text:
    def __init__(self, dis, text="", rect=(0, 0, 0, 0), type=0, size=50, textClr=(255, 255, 255)):
        self.dis = dis
        self.rect = pygame.Rect(rect)
        self.state = True
        self.text_clr = textClr
        self.text = text
        self.text_size = size
        self.font_style = pygame.font.Font('fonts/Milkshake_3de45646d19b2839020f16d637766759.ttf', self.text_size) if type == 0 else pygame.font.Font('fonts/minecraft-font/MinecraftRegular-Bmg3.otf', self.text_size)

    def rend(self):
        if self.state:
            value = self.font_style.render(self.text, True, self.text_clr)
            self.dis.blit(value, (self.rect.centerx - value.get_width()/2, self.rect.centery - value.get_height()/2))

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_cent_pos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def set_size(self, w, h):
        self.rect.width = w
        self.rect.height = h

    def get_font(self, loc):
        self.font_style = pygame.font.Font(loc, self.text_size)


class Button(Text):
    def __init__(self, dis, text, type=1, size=30):
        super().__init__(dis, text, type, size)
        self.clr = (0, 0, 0, 0)
        self.act_clr = (100, 100, 100)
        self.bord_clr = (255, 255, 255)
        self.bord_wid = 2
        self.bord_r = -1
        #self.text = ""
        self.clicked = False
        self.disabled = False

    def rend(self):
        if self.state:
            if self.rect.contains((pygame.mouse.get_pos(), (0, 0))) or self.disabled:
                pygame.draw.rect(self.dis, self.act_clr, self.rect, 0, self.bord_r)
                value = self.font_style.render(self.text, True, self.text_clr, self.act_clr)
            else:
                pygame.draw.rect(self.dis, self.clr, self.rect, 0, self.bord_r)
                value = self.font_style.render(self.text, True, self.text_clr, self.clr)
            pygame.draw.rect(self.dis, self.bord_clr, self.rect, self.bord_wid, self.bord_r)
            self.dis.blit(value, (self.rect.centerx - value.get_width()/2, self.rect.centery - value.get_height()/2))

    def is_clicked(self):
        if not self.disabled and self.state:
            if self.rect.contains((pygame.mouse.get_pos(), (0, 0))) and pygame.mouse.get_pressed()[0]:
                self.clicked = True
            if not pygame.mouse.get_pressed()[0] and self.clicked:
                self.clicked = False
                return True
