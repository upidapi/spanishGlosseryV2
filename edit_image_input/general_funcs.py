import pygame as pg

pg.init()
font = pg.font.SysFont('Helvatical bold', 24)


def wh_to_chords(wh: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """
    converts width and height to coordinate position

    :param wh: x, y, width, height
    :return: x1, y1, x2, y2
    """

    x, y, width, height = wh
    return int(x), int(y), int(x + width), int(y + height)


def chords_to_wh(chords: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """
    converts coordinate position to width and height

    :param chords: x1, y1, x2, y2
    :return: x, y, width, height
    """
    x1, y1, x2, y2 = chords

    width = abs(x1 - x2)
    height = abs(y1 - y2)
    x = min(x1, x2)
    y = min(y1, y2)

    return x, y, width, height


def button_click_check(button_size, click_pos=None) -> bool:
    """
    checks if the position is inside the given button size

    :param button_size: the dimensions of the button (x, y, width, height)
    :param click_pos: the click pos (by default the mouse position)
    :return: true/false
    """

    if click_pos is None:
        click_pos = pg.mouse.get_pos()

    x1, y1, x2, y2 = button_size

    if x1 <= click_pos[0] <= x2 and y1 <= click_pos[1] <= y2:
        return True
    return False


def get_size_of_text(text):
    """
    gets the size of the text

    :param text:
    :return: the size of the text (width, height)
    """

    text_img = font.render(text, True, (0, 0, 0))
    return text_img.get_size()


def get_line_bounding_box(line):
    """
    gets the dimensions of the smallest possible box that contain all the words in the line

    :param line: a line (data class)
    :return: the bounding box of the line (x, y, width, height)
    """

    min_x1, min_y1, max_x2, max_y2 = [1_000_000, 1_000_000, 0, 0]
    words = line["Words"]
    for word in words:
        x1, y1, x2, y2 = wh_to_chords((word["Left"], word["Top"], word["Width"], word["Height"]))
        # gets the min/max chords of chords to get the bounding box
        min_x1 = min(min_x1, x1)
        min_y1 = min(min_y1, y1)
        max_x2 = max(max_x2, x2)
        max_y2 = max(max_y2, y2)

    return chords_to_wh((min_x1, min_y1, max_x2, max_y2))


def get_multiple_lines_bounding_box(lines: tuple[any] | list[any]):
    """
    gets the dimensions of the smallest possible box that contain all the lines

    :param lines: multiple lines
    :return: the bounding box of the lines (x, y, width, height)
    """

    min_x1, min_y1, max_x2, max_y2 = [1_000_000, 1_000_000, 0, 0]

    for line in lines:
        x1, y1, x2, y2 = wh_to_chords((line['x'], line['y'], line['width'], line['height']))
        # gets the min/max chords of chords to get the bounding box
        min_x1 = min(min_x1, x1)
        min_y1 = min(min_y1, y1)
        max_x2 = max(max_x2, x2)
        max_y2 = max(max_y2, y2)

    return chords_to_wh((min_x1, min_y1, max_x2, max_y2))


def mouse_in_line(pos, line_data):
    """
    checks if the pos is inside the line

    :param pos:
    :param line_data:
    :return: True if it's inside False otherwise
    """
    x1, y1, x2, y2 = wh_to_chords((line_data['x'], line_data['y'], line_data['width'], line_data['height']))

    if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
        return True
    return False