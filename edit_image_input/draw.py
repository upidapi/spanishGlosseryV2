from data.funcs import Handler
from lisseners import EditText
from edit_input import Check
from general_funcs import *
import time

line_data = Handler()
font = pg.font.SysFont('Helvatical bold', 24)


# general definitions
def draw_rgba_rect(surface, color, start, size, outline_width=0, outline_color=(0, 0, 0)):
    # drawing a rect with alpha
    select_rect = pg.Surface(size)  # the size of your rect
    select_rect.set_alpha(color[3])  # alpha level
    select_rect.fill((color[0], color[1], color[2]))  # this fills the entire surface

    surface.blit(select_rect, start)  # (0,0) are the top-left coordinates

    # draws the outline
    pg.draw.rect(surface, outline_color, start + size, outline_width)


def get_line_points(start, end):
    """
    Bresenham's Line Algorithm
    Produces a list of tuples from start and end

    :param start: x1, y1
    :param end: x2, y2
    :return:
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    y_step = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += y_step
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()

    return points


# debug thing
def draw_line_box(surface):
    for line in line_data:
        draw_rgba_rect(surface, (200, 200, 255, 128), (line['x'], line['y']), (line['width'], line['height']),
                       outline_width=1, outline_color=(0, 100, 255))


# normal draws
def draw_translations_box(translation_lines, surface):
    for translations in translation_lines:
        dim = get_multiple_lines_bounding_box(translations)
        pg.draw.rect(surface, (0, 0, 255), dim, 1)


def draw_translation_lines(translation_pairs, surface):
    for translation_pair in translation_pairs:
        if len(translation_pair) == 2:
            dim1 = (translation_pair[0]['x'],
                    translation_pair[0]['y'],
                    translation_pair[0]['width'],
                    translation_pair[0]['height'])

            dim2 = (translation_pair[1]['x'],
                    translation_pair[1]['y'],
                    translation_pair[1]['width'],
                    translation_pair[1]['height'])

            x1, y1 = dim1[0] + dim1[2] // 2, dim1[1] + dim1[3] // 2
            x2, y2 = dim2[0] + dim2[2] // 2, dim2[1] + dim2[3] // 2

            pixels = get_line_points((x1, y1), (x2, y2))
            for pixel in pixels:
                if not mouse_in_line(pixel, translation_pair[0]) and not mouse_in_line(pixel, translation_pair[1]):
                    surface.set_at(pixel, (0, 0, 0))

        else:
            dim = (translation_pair[0]['x'],
                   translation_pair[0]['y'],
                   translation_pair[0]['width'],
                   translation_pair[0]['height'])

            pg.draw.rect(surface, (255, 0, 0), dim, 1)


def draw_pointer(selected, pointer_pos, surface):
    if not Check.get_drag() and selected is not None:
        if EditText.time_since_last_edit() < 0.5 or 0.5 > time.time() % 1:
            text = EditText.get_text()[0:pointer_pos]
            text_size = get_size_of_text(text)

            start_x = line_data[selected]['x'] + get_size_of_text(text)[0]
            start_y = line_data[selected]['y']
            pg.draw.rect(surface, (0, 0, 0),
                         pg.Rect(start_x, start_y, 2, text_size[1] + 2))


def draw_lines(selected, surface):
    for i, line in enumerate(line_data):
        if i == selected:
            text = EditText.get_text()
            text_img = font.render(text, True, (255, 0, 0))

        else:
            text_img = font.render(line['text'], True, (0, 0, 0))

        surface.blit(text_img, (line['x'], line['y']))


def draw_combine_line(selected, surface):
    if selected is not None and Check.get_drag():
        x1, y1 = line_data[selected]['x'] + line_data[selected]['width'] // 2, \
                 line_data[selected]['y'] + line_data[selected]['height'] // 2
        x2, y2 = pg.mouse.get_pos()

        pixels = get_line_points((x1, y1), (x2, y2))
        for pixel in pixels:
            if not mouse_in_line(pixel, line_data[selected]):
                surface.set_at(pixel, (0, 0, 0))