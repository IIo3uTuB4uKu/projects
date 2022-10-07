import pygame as pg
import sys
import time
import pyperclip


class TextArea:
    def __init__(self, screen, size, positions, background=(0, 0, 0), text_color=(255, 255, 255)):
        self.surface = pg.Surface((size))
        self.size = size
        self.move_x = 0
        self.move_y = 0
        self.screen = screen
        self.font = pg.font.Font(None, 30)
        self.text = ['']
        self.positions = positions
        self.background = background
        self.text_color = text_color
        self.now_line = 0
        self.coursor_position = 0
        self.drawing_coursor = True
        self.delite = False
        self.button_delete = False
        self.direction = None

        # timers
        self.time_del = time.time()
        self.time_draw_coursor = time.time()
        self.time_move_corsor = time.time()

    def move_coursor(self):
        if self.direction == 'up':
            self.now_line -= 1 if self.now_line > 0 else 0
            self.coursor_position = 0
        if self.direction == 'down':
            self.now_line += 1 if self.now_line < len(self.text) - 1 else 0
            self.coursor_position = 0
        if self.direction == 'left':
            self.coursor_position += 1 if self.coursor_position < len(
                self.text[self.now_line]) else 0
        if self.direction == 'right':
            self.coursor_position -= 1 if self.coursor_position > 0 else 0

    def delite_symbol(self):
        line = self.text[self.now_line]
        if line == '' and not self.button_delete:
            if not self.now_line and len(self.text) == 1:
                return
            temp = self.text[:self.now_line:]
            for x in self.text[self.now_line + 1::]:
                temp.append(x)
            self.text = temp
            self.now_line -= 1 if self.now_line > 0 else 0
            return
        if self.button_delete:
            if self.coursor_position == 0:
                if self.now_line < len(self.text) - 1:
                    self.text[self.now_line] = self.text[self.now_line] + \
                        self.text[self.now_line + 1]
                    self.coursor_position = len(
                        self.text[self.now_line + 1])
                    self.text.pop(self.now_line + 1)
                return
            else:
                self.text[self.now_line] = line[:len(line) - self.coursor_position:] + \
                    line[len(line) - self.coursor_position + 1::]

                self.coursor_position -= 1
        else:
            self.text[self.now_line] = line[:len(line) - self.coursor_position - 1:] + \
                line[len(line) - self.coursor_position::]

    def text_len(self, text_):
        # return text len
        FontObj = pg.font.Font(None, 30)
        TextSurfaceObj = FontObj.render(f'{text_}', True, (0, 0, 0), None)
        return TextSurfaceObj.get_rect()[2]

    def draw_text(self, text_, positions, color, background=None):
        # draw text
        TextSurfaceObj = self.font.render(f'{text_}', True, color, None)
        TextRectObj = TextSurfaceObj.get_rect()
        TextRectObj.x, TextRectObj.y = positions

        self.surface.blit(TextSurfaceObj, TextRectObj)

    def draw(self):
        # mouse
        pos_mouse = pg.mouse.get_pos()
        if pos_mouse[0] > self.positions[0] and pos_mouse[1] - 30 > self.positions[1] and \
            pos_mouse[0] < self.positions[0] + self.size[0] and \
                pos_mouse[1] + 30 < self.positions[1] + self.size[1]:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_IBEAM)
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        # move coursor
        if self.direction and time.time() - self.time_move_corsor > 0.1:
            self.move_coursor()
            self.time_move_corsor = time.time()

        # deliting
        if self.delite and time.time() - self.time_del > 0.1:
            self.delite_symbol()
            self.time_del = time.time()

        # draw text
        self.surface.fill(self.background)
        max_len = max(self.text_len(x) for x in self.text)

        if max_len + self.move_x > self.size[0] - 30:
            self.move_x -= 5
        elif max_len < self.size[0] - 30:
            self.move_x += 5 if self.move_x < 0 else 0

        pos = (5 + self.move_x, 30 + self.move_y)
        for line in self.text:
            if pos[1] > 0 and pos[1] < self.size[1]:
                self.draw_text(line, pos, self.text_color)
            pos = (pos[0], pos[1] + 20)

        if 30 + self.move_y + 20 * len(self.text) > self.size[1] - 30:
            self.move_y -= 5

        # draw coursor
        if self.drawing_coursor:
            len_text = self.text_len(self.text[self.now_line][:len(
                self.text[self.now_line]) - self.coursor_position:])
            coursor = '|' if self.coursor_position == 0 else '|'
            if len_text + 5 + self.move_x < 0:
                self.move_x += 5

            self.draw_text(coursor, (len_text + 5 + self.move_x,
                                     30 + 20 * self.now_line + self.move_y), (0, 0, 0))

        if time.time() - self.time_draw_coursor > 0.7:
            self.drawing_coursor = False if int(self.drawing_coursor) else True
            self.time_draw_coursor = time.time() if self.drawing_coursor else time.time() - 0.5

        # draw border
        pg.draw.rect(self.surface, (55, 55, 55), (0, 0, self.size[0], 20))
        pg.draw.line(self.surface, (55, 55, 55), (0, 0), (0, self.size[1]), 5)
        pg.draw.line(self.surface, (55, 55, 55),
                     (0, self.size[1]), (self.size[0], self.size[1]), 5)
        pg.draw.line(self.surface, (55, 55, 55), (self.size[0], self.size[1]),
                     (self.size[0], 0), 5)

        self.screen.blit(self.surface, self.positions)

    def event_(self, event):
        # look as events
        if event.type == pg.KEYDOWN:
            line = self.text[self.now_line]

            if event.key == pg.K_UP:
                self.direction = 'up'
            if event.key == pg.K_DOWN:
                self.direction = 'down'
            if event.key == pg.K_LEFT:
                self.direction = 'left'
            if event.key == pg.K_RIGHT:
                self.direction = 'right'

            if event.key == pg.K_BACKSPACE:
                self.delite = True
                return

            if event.unicode == '\r':
                temp = self.text[:self.now_line + 1:]
                temp.append('')
                for x in self.text[self.now_line + 1::]:
                    temp.append(x)
                self.text = temp
                self.now_line += 1
                self.coursor_position = 0
                return
            if event.unicode == '\t':
                self.text[self.now_line] = line[:len(line) - self.coursor_position:] + \
                    "    " + line[len(line) - self.coursor_position::]
                return
            if event.unicode == '\x03':
                return
            if event.unicode == '\x16':
                for index, string in enumerate(pyperclip.paste().split('\n')):
                    if self.now_line + index >= len(self.text):
                        self.text.append('')
                    self.text[self.now_line + index] = line[:len(line) - self.coursor_position:] + \
                        f"{string}" + \
                        line[len(line) - self.coursor_position::]
                return
            if event.unicode == '\x7f':
                self.delite = True
                self.button_delete = True
                self.time_del = time.time()
                if self.coursor_position == 0:
                    if self.now_line < len(self.text) - 1:
                        self.text[self.now_line] = self.text[self.now_line] + \
                            self.text[self.now_line + 1]
                        self.coursor_position = len(
                            self.text[self.now_line + 1])
                        self.text.pop(self.now_line + 1)
                else:
                    self.delite_symbol()
                return
            else:
                self.text[self.now_line] = line[:len(line) - self.coursor_position:] + str(
                    event.unicode) + line[len(line) - self.coursor_position::]

        if event.type == pg.KEYUP:
            if event.key == pg.K_BACKSPACE:
                self.delite = False
            if event.unicode == '\x7f':
                self.delite = False
                self.button_delete = False
            if event.key == pg.K_UP:
                self.direction = None
            if event.key == pg.K_DOWN:
                self.direction = None
            if event.key == pg.K_LEFT:
                self.direction = None
            if event.key == pg.K_RIGHT:
                self.direction = None

        if event.type == pg.MOUSEBUTTONDOWN:
            pos_mouse = pg.mouse.get_pos()
            for i, string in enumerate(self.text):
                if pos_mouse[1] - self.positions[1] - 30 >= 0 + 20 * i and \
                        pos_mouse[1] - self.positions[1] - 30 <= 19 + 20 * i:
                    self.now_line = i
                    self.coursor_position = 0
                    if pos_mouse[0] - self.positions[0] - 5 < self.text_len(string) and \
                            pos_mouse[0] - self.positions[0] - 5 > 0:
                        cheked_text = ''
                        for index, item in enumerate(string):
                            if pos_mouse[0] - self.positions[0] - 5 > self.text_len(cheked_text) and \
                                    pos_mouse[0] - self.positions[0] - 5 < self.text_len(cheked_text + item) + 2:
                                self.coursor_position = abs(
                                    index - len(string) + 1)
                                break
                            else:
                                cheked_text += item

                    break
            else:
                self.now_line = len(self.text) - 1
                self.coursor_position = 0
