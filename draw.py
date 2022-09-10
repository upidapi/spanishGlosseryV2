import pygame as pg
from data import DataClass
import lisseners
import edit_input

line_data = DataClass()
font = pg.font.SysFont('Helvatical bold', 24)


def change_title(text):
    pg.display.set_caption(text)


def draw_pointer(selected, pointer_pos, surface):
    if selected:
        text = lisseners.Text.get_text()[0:pointer_pos]
        image_pos = font.render(text, True, (255, 0, 0)).get_size()
        start_x = line_data[selected]['x'] + image_pos[0]
        start_y = line_data[selected]['y']
        pg.draw.rect(surface, (0, 0, 0),
                     pg.Rect(start_x, start_y, 2, image_pos[1] + 2))


def draw_lines(selected, surface):
    for i, line in enumerate(line_data):
        if i == selected:
            text_img = font.render(lisseners.Text.get_text(), True, (255, 0, 0))
        else:
            text_img = font.render(line['text'], True, (0, 0, 0))

        surface.blit(text_img, (line['x'], line['y']))


def draw_combine_line(selected, surface):
    if selected and edit_input.EditCallFuncs.get_drag():
        middle = line_data[selected]['x'] + line_data[selected]['width'] // 2, \
                 line_data[selected]['y'] + line_data[selected]['height'] // 2
        pg.draw.line(surface, (0, 0, 0), middle, pg.mouse.get_pos())



