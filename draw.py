import pygame as pg
from data import DataClass
import lisseners

line_data = DataClass()
font = pg.font.SysFont('Helvatical bold', 24)


def change_title(text):
    pg.display.set_caption(text)


def draw_pointer(selected, pointer_pos, surface):
    if selected:
        text = line_data[pointer_pos][0:pointer_pos]
        image_pos = font.render(text, True, (255, 0, 0)).get_size()
        start_x = line_data[pointer_pos]['x'] + image_pos[0] + 2
        pg.draw.rect(surface, (0, 0, 0),
                     pg.Rect(start_x, line_data[pointer_pos]['y'] - 2,
                     image_pos[1] + 4, 4))


def draw_lines(selected, surface):
    for i, line in enumerate(line_data):
        if i == selected:
            text = lisseners.Text.get_text()
        else:
            text = line['text']

        text_img = font.render(text, True, (255, 0, 0))
        surface.blit(text_img, (line['x'], line['y']))


