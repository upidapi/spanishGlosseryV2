import pygame as pg

from data.funcs import Handler, SimplifiedJson, Cleaner

from lisseners import EditText
from edit_input import Basic, Check
import draw


def check_exit(frame_events):
    for event in frame_events:
        if event.type == pg.QUIT:
            pg.quit()
            # DataJson.save_data_to_jason()
            quit()


class Mode:
    # global mode, draw_text

    mode = 0
    draw_text = True
    selected_lan = 0

    @staticmethod
    def mode_0_setup():
        # screen setup
        pg.display.set_caption('add/combine/delete/move lines')

        for i in range(len(data)):
            Basic.set_line_size(i)

    @staticmethod
    def mode_1_setup():
        pg.display.set_caption('edit lines')

        combined_data = []
        for pair1, pair2 in zip(Basic.get_translation_pairs(data['all']),
                                Basic.get_translation_pairs(data.get_data2())):
            if len(pair1) == 2 and len(pair2) == 2:
                combined_data.append(pair1[0])
                combined_data.append(pair2[1])
            else:
                combined_data = data['all']
                Mode.mode = 0
                Mode.mode_0_setup()
                break

        data['all'] = combined_data

    @staticmethod
    def mode_2_setup():
        word_data = []
        pairs = Basic.get_translation_pairs(data['all'])
        for pair in pairs:
            word_data.append((pair[0]['text'], pair[1]['text']))

        SimplifiedJson.save_to_jason(word_data, '../load_words/words/ch2/clean_data_full')

    @staticmethod
    def next_mode(frame_events):
        # next mode (return + ctrl)
        for event in frame_events:
            if pg.key.get_mods() & pg.KMOD_CTRL:
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    Mode.mode += 1
                    if Mode.mode == 0:
                        Mode.mode_0_setup()

                    if Mode.mode == 1:
                        Mode.mode_1_setup()

                    if Mode.mode == 2:
                        Mode.mode_2_setup()

                if event.type == pg.KEYDOWN and event.key == pg.K_s:
                    Mode.draw_text = False
                if event.type == pg.KEYUP and event.key == pg.K_s:
                    Mode.draw_text = True

                if event.type == pg.KEYDOWN and event.key == pg.K_w:
                    switch = {0: 1, 1: 0}
                    Mode.selected_lan = switch[Mode.selected_lan]
                    data.switch_data()
                    for i in range(len(data)):
                        Basic.set_line_size(i)


def draw_mode(frame_events):
    global languishes
    if Mode.draw_text:
        EditText.change_text(frame_events)
        game_screen.fill((255, 255, 255))

        draw.draw_lines(Check.get_selected(), game_screen)
        draw.current_lan(game_screen, languishes[Mode.selected_lan])

        if Mode.mode == 0:
            draw.draw_pointer(Check.get_selected(), EditText.get_pointer_pos(), game_screen)
            draw.draw_combine_line(Check.get_selected(), game_screen)
            # draw.draw_translations_box(Basic.find_translation(), game_screen)
            draw.draw_translation_lines(Basic.get_translation_pairs(data['all']), game_screen)
        if Mode.mode == 1:
            draw.draw_pointer(Check.get_selected(), EditText.get_pointer_pos(), game_screen)
            draw.draw_translation_lines(Basic.get_translation_pairs(data['all']), game_screen)

    else:
        game_screen.blit(pg_text_img, (0, 0))


def do_action(frame_events):
    # move / new (right click), combine (left click drag), move (right click), delete (backspace)
    # edit (return)

    for event in frame_events:
        # select / unselect line (left click)
        Check.select_line(event)

        if Mode.mode == 0:
            # check start drag (left click)
            Check.start_drag(event)

            # edit line (return)
            Check.edit_line(event)

            # move / new line (right click)
            Check.new_line(event)

            # combine lines (left click drag)
            Check.combine_line(event)

            # delete line (del)
            Check.delete_line(event)

        if Mode.mode == 1:
            # edit line (return)
            Check.edit_line(event)


def edit_event_loop():
    frame_events = pg.event.get()

    check_exit(frame_events)

    Mode.next_mode(frame_events)
    do_action(frame_events)
    draw_mode(frame_events)


def main():
    global mode, draw_text, game_screen, pg_text_img, data, languishes
    pg.init()
    clock = pg.time.Clock()

    # definitions
    data = Handler()

    # format:
    # lan_1_word  lan_2_word     lan_1_word  lan_2_word
    # lan_1_word  lan_2_word     lan_1_word  lan_2_word
    # lan_1_word  lan_2_word     lan_1_word  lan_2_word
    languishes = 'spa', 'swe'

    text_image_dir = 'data/selected_image.jpg'
    pg_text_img = pg.image.load(text_image_dir)
    game_screen = pg.display.set_mode((pg_text_img.get_size()))

    Mode.mode_0_setup()

    # Cleaner.new_image('spa_text_glossary_perfect', languishes)

    while True:
        edit_event_loop()

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
