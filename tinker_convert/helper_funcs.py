from typing import Literal


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


def get_mods(event):
    s = event.state

    # Manual way to get the modifiers
    ctrl = (s & 0x4) != 0
    alt = (s & 0x8) != 0 or (s & 0x80) != 0
    shift = (s & 0x1) != 0

    mods = []
    if ctrl:
        mods.append('ctrl')
    if alt:
        mods.append('alt')
    if shift:
        mods.append('shift')

    return mods


# todo might want to switch all "if mod in get_mods" to this instead
def run_if_mod(event, mod: Literal['ctrl', 'alt', 'shift'], func: callable):
    if mod in get_mods(event):
        func()
