BG_COLOR = '#f0f0f0'
ERROR_COLOR = '#%02x%02x%02x' % (255, 200, 200)


def __init__(global_canvas, global_tk_image):
    global canvas, tk_image

    canvas = global_canvas
    tk_image = global_tk_image


def get_bounding_box(lines):
    min_x1, min_y1, max_x2, max_y2 = [1_000_000, 1_000_000, 0, 0]

    for line in lines:
        x, y, width, height = int(line['x']), int(line['y']), int(line['width']), int(line['height'])
        x1, y1, x2, y2 = x, y, x + width, y + height
        # gets the min/max chords of chords to get the bounding box
        min_x1 = min(min_x1, x1)
        min_y1 = min(min_y1, y1)
        max_x2 = max(max_x2, x2)
        max_y2 = max(max_y2, y2)

    return min_x1, min_y1, max_x2, max_y2


def find_tr_lines(data):
    unsorted_line = data.copy()
    unsorted_line.sort(key=lambda x: x['y'])

    # the percentage you remove from the line
    # 0 -> the line has to overlap with the hotbox
    # 0.5 -> half the line has to overlap
    # 1 -> the center has to overlap
    # 2 -> the whole lines has to be inside

    margins = 1

    current_lines = []
    translations = []
    for line in unsorted_line:
        # if it's empty
        if not current_lines:
            current_lines.append(line)
        else:
            bounding_box = get_bounding_box(current_lines)
            # decreases the line "size" by size * margins
            # line['y']                  + line['height'] * margins / 2
            # line['y'] + line['height'] - line['height'] * margins / 2
            # a + (x - x * m / 2)
            # a + x(1 - m / 2)

            bottom_line = line['y'] + line['height'] * margins / 2
            top_line = line['y'] + line['height'] * (1 - margins / 2)

            if bounding_box[1] <= bottom_line <= bounding_box[3] or \
                    bounding_box[1] <= top_line <= bounding_box[3]:
                current_lines.append(line)
            else:
                translations.append(current_lines)
                current_lines = [line]

    translations.append(current_lines)

    return translations


def find_tr_pairs(data):
    tr_lines = find_tr_lines(data)
    tr_pairs = []

    for trs in tr_lines:
        trs.sort(key=lambda x: x['x'])
        full_trs = (len(trs) // 2)

        for i in range(full_trs):
            line1 = trs[i * 2]
            line2 = trs[i * 2 + 1]
            tr_pairs.append((line1, line2))

        if len(trs) != full_trs * 2:
            tr_pairs.append((trs[-1],))

    return tr_pairs


def draw(data):
    tr_pairs = find_tr_pairs(data)

    canvas.delete("all")
    canvas.create_image(tk_image.width() // 2,
                        tk_image.height() // 2,
                        image=tk_image)  # the x and y is the center apparently

    for tr_pair in tr_pairs:
        if len(tr_pair) == 2:
            x1 = tr_pair[0]['x'] + tr_pair[0]['width'] // 2
            x2 = tr_pair[1]['x'] + tr_pair[1]['width'] // 2
            y1 = tr_pair[0]['y'] + tr_pair[0]['height'] // 2
            y2 = tr_pair[1]['y'] + tr_pair[1]['height'] // 2

            canvas.create_line(x1, y1, x2, y2, fill="black", width=1)

            tr_pair[0]['self'].entry.configure(bg=BG_COLOR)
            tr_pair[1]['self'].entry.configure(bg=BG_COLOR)

        else:
            tr_pair[0]['self'].entry.configure(bg=ERROR_COLOR)


def get_connections(data):
    unsorted_lines = data.copy()
    unsorted_lines.sort(key=lambda x: x['y'])

    margins = 1

    """
    the percentage you remove from the line
    0 -> the line has to overlap with the hotbox
    0.5 -> half the line has to overlap
    1 -> the center has to overlap
    2 -> the whole lines has to be inside
    """

    pairs = []
    indexed = []
    for line in unsorted_lines:
        """
        decreases the line "size" by size * margins
        line['y']                  + line['height'] * margins / 2
        line['y'] + line['height'] - line['height'] * margins / 2
        a + (x - x * m / 2)
        a + x(1 - m / 2)
        """

        bottom_line = line['y'] + line['height'] * margins / 2
        top_line = line['y'] + line['height'] * (1 - margins / 2)

        for j, indexed_line in enumerate(indexed):
            # if the top or bottom of the hit-box collides
            top_hit_box, bottom_hit_box = indexed_line['y'], indexed_line['y'] + indexed_line['height']
            if top_hit_box <= bottom_line <= bottom_hit_box or \
                    top_hit_box <= top_line <= bottom_hit_box:
                pairs.append((indexed_line, line))

        indexed.append(line)

    return pairs


def cn_to(x, pairs):
    x_cn_to = []
    for pair in pairs:
        if x in pair:
            x_cn_to.append(pair)

    return x_cn_to


def debug_show(x):
    print([(part[0]['text']['main'], part[1]['text']['main']) for part in x])


def get_pairs_v2(data):
    pairs = get_connections(data)

    tr_pairs = []
    non_pairs = []

    data.sort(key=lambda x: x['x'])
    while 0 < len(data):
        # a start that is guarantied to not have multiple things before it
        current_point = data[0]
        data.remove(current_point)

        cn_pairs = cn_to(current_point, pairs)

        # this cannot be the best connection
        best_cn = {'text': None, 'x': 1_000_000_000, }
        for cn_pair in cn_pairs:
            # don't reference a paired line
            pairs.remove(cn_pair)

            cn = cn_pair[not cn_pair.index(current_point)]
            if cn['x'] < best_cn['x']:
                best_cn = cn

        if best_cn['text'] is not None:
            tr_pairs.append((current_point, best_cn))
            data.remove(best_cn)

            # don't reference a paired line
            best_cn_cns = cn_to(best_cn, pairs)

            for best_cn_cn in best_cn_cns:
                pairs.remove(best_cn_cn)

        else:
            non_pairs.append(current_point)

    return tr_pairs, non_pairs


def draw_v2(data):
    tr_pairs, non_pairs = get_pairs_v2(data)

    canvas.delete("all")
    canvas.create_image(tk_image.width()//2,
                        tk_image.height()//2,
                        image=tk_image)  # the x and y is the center apparently

    for tr_pair in tr_pairs:
        x1 = tr_pair[0]['x'] + tr_pair[0]['width'] // 2
        x2 = tr_pair[1]['x'] + tr_pair[1]['width'] // 2
        y1 = tr_pair[0]['y'] + tr_pair[0]['height'] // 2
        y2 = tr_pair[1]['y'] + tr_pair[1]['height'] // 2

        canvas.create_line(x1, y1, x2, y2, fill="black", width=1)

        tr_pair[0]['self'].entry.configure(bg=BG_COLOR)
        # it always exists
        # noinspection PyUnresolvedReferences
        tr_pair[1]['self'].entry.configure(bg=BG_COLOR)

    for line in non_pairs:
        line['self'].entry.configure(bg=ERROR_COLOR)




