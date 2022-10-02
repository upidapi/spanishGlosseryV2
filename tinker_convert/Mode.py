from tinker_convert.TrLines import find_tr_pairs
from tinker_convert.helper_funcs import get_mods
from tinker_convert.CustomEntery import Handler
from tinker_convert.data.Data import save_data


def __init__(global_root, global_languages):
    global root, mode, languages
    root = global_root
    languages = global_languages
    mode = 0

    root.title(f'split/move/add/delete words (lan: {languages[0]})')


def setup_1():
    global mode

    data = Handler.get_data()
    tr_pairs = find_tr_pairs(data)

    # if any of the words doesn't have a translation we can't go to next
    for tr_pair in tr_pairs:
        if len(tr_pair) != 2:
            mode = 0
            return

    Handler.mode = 1

    # if it gets here all words has a translation
    for tr_pair in tr_pairs:
        if Handler.switch:
            tr_pair[0]['self'].saved_text = tr_pair[0]['self'].other_text
            tr_pair[1]['self'].other_text = tr_pair[1]['self'].saved_text
        else:
            tr_pair[0]['self'].other_text = tr_pair[0]['self'].saved_text
            tr_pair[1]['self'].saved_text = tr_pair[1]['self'].other_text

        tr_pair[0]['self'].tk_text.set(tr_pair[0]['self'].saved_text)
        tr_pair[1]['self'].tk_text.set(tr_pair[1]['self'].saved_text)

        tr_pair[0]['self'].update_hit_box(2)
        tr_pair[1]['self'].update_hit_box(2)

    root.title('edit words')


def setup_2():
    # saves the data
    global mode

    data = Handler.get_data()
    tr_pairs = find_tr_pairs(data)

    # if any of the words doesn't have a translation we can't go to next
    for tr_pair in tr_pairs:
        if len(tr_pair) != 2:
            mode = 1
            return

    Handler.mode = 2

    all_text_pairs = []
    for tr_pair in tr_pairs:
        data = (
            tr_pair[0]['text']['main'],
            tr_pair[1]['text']['main'],
        )
        all_text_pairs.append(data)

    save_data(all_text_pairs)


def next_mode(event):
    global mode
    if 'ctrl' in get_mods(event):
        mode += 1

        if mode == 1:
            setup_1()

        if mode == 2:
            setup_2()
