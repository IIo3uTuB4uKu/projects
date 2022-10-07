from copy import copy
import pygame as pg


class Button:
    def __init__(self, screen, position, doing, name, min_color, max_color, time_moving=25):
        self.position = position
        self.doing = doing
        self.name = name
        self.screen = screen
        self.center = (position[0] + (position[2] / 2),
                       position[1] + (position[3] / 2))
        self.min_color = min_color
        self.max_color = max_color
        self.color_now = copy(min_color)
        time_moving = 1 if time_moving == 0 else time_moving
        self.multies = [(self.max_color[i] - self.min_color[i]
                         ) / time_moving for i in range(3)]

    def text(self, screen, text_, center, color, background=None, size=30, to_center=False):
        TextSurfaceObj = pg.font.Font(None, size).render(
            f'{text_}', True, color, background)
        TextRectObj = TextSurfaceObj.get_rect()
        if to_center:
            TextRectObj.center = center
        else:
            TextRectObj.x, TextRectObj.y = center

        screen.blit(TextSurfaceObj, TextRectObj)

    def draw(self, click):
        m_pos = (pg.mouse.get_pos()[0],
                 pg.mouse.get_pos()[1])

        if m_pos[0] > self.position[0] and m_pos[1] > self.position[1]:
            if m_pos[0] < self.position[0] + self.position[2] and m_pos[1] < self.position[1] + self.position[3]:
                in_button = True
                if click:
                    return self.doing
            else:
                in_button = False
        else:
            in_button = False

        for i in range(3):
            if in_button:
                self.color_now[i] += self.multies[i] if self.color_now[i] < self.max_color[i] else 0
            else:
                self.color_now[i] -= self.multies[i] if self.color_now[i] > self.min_color[i] else 0

            for i, color in enumerate(self.color_now):
                if color > 255:
                    self.color_now[i] = 255
                if color < 0:
                    self.color_now[i] = 0

        pg.draw.rect(self.screen, self.color_now, self.position)
        self.text(self.screen, self.name, self.center,
                  (21, 45, 74), size=20, to_center=True)
