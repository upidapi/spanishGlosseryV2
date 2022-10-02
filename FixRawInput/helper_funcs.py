def get_mods(event):
    s = event.state
    mods = []

    if s != '??':  # checks if the event has a state, if it doesn't the state is '??' for example 'FocusIn'
        # Manual way to get the modifiers
        ctrl = (s & 0x4) != 0
        alt = (s & 0x8) != 0 or (s & 0x80) != 0
        shift = (s & 0x1) != 0

        if ctrl:
            mods.append('ctrl')
        if alt:
            mods.append('alt')
        if shift:
            mods.append('shift')

    return mods


def get_line_bounding_box(line):
    min_x1, min_y1, max_x2, max_y2 = [1_000_000, 1_000_000, 0, 0]
    words = line["Words"]
    for word in words:
        # converts width/height to coordinates
        x, y, width, height = word["Left"], word["Top"], word["Width"], word["Height"]
        x1, y1, x2, y2 = x, y, x + width, y + height

        # gets the min/max chords of chords to get the bounding box
        min_x1 = min(min_x1, x1)
        min_y1 = min(min_y1, y1)
        max_x2 = max(max_x2, x2)
        max_y2 = max(max_y2, y2)

    # converts coordinate to width/height
    x1, y1, x2, y2 = min_x1, min_y1, max_x2, max_y2
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    x = min(x1, x2)
    y = min(y1, y2)

    return x, y, width, height

