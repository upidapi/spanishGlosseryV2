from lisseners import Text
from edit_input import Basic, Check
# new image is needed
from data import DataClass, new_image
import pygame as pg
import draw


def check_exit(frame_events):
    for event in frame_events:
        if event.type == pg.QUIT:
            pg.quit()
            # DataJson.save_data_to_jason()
            quit()


def check_next_mode(frame_events):
    global mode, draw_text
    # next mode (return + ctrl)
    for event in frame_events:
        if pg.key.get_mods() & pg.KMOD_CTRL:
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                mode += 1

                if mode == 1:
                    pg.display.set_caption('combine/delete/move lines')

                    for i in range(len(data)):
                        Basic.set_line_size(i)

                if mode == 2:
                    # todo run autocorrect one every word (languish based on translation)
                    pg.display.set_caption('edit lines')

            if event.type == pg.KEYDOWN and event.key == pg.K_s:
                draw_text = False
            if event.type == pg.KEYUP and event.key == pg.K_s:
                draw_text = True


def draw_mode(frame_events):
    if draw_text:
        Text.save_text_input(frame_events)
        game_screen.fill((255, 255, 255))

        draw.draw_lines(Check.get_selected(), game_screen)

        if mode == 0:
            draw.draw_pointer(Check.get_selected(), Text.get_pointer_pos(), game_screen)

        if mode == 1:
            draw.draw_combine_line(Check.get_selected(), game_screen)
            draw.draw_translations_box(Basic.find_translation(), game_screen)
            draw.draw_translation_lines(Basic.find_translation(), game_screen)

        if mode == 2:
            draw.draw_pointer(Check.get_selected(), Text.get_pointer_pos(), game_screen)

    else:
        game_screen.blit(pg_text_img, (0, 0))


def do_action(frame_events):
    # move / new (/ edit) (right click)
    # combine (left click drag), move (right click), delete (backspace)
    # edit (return)

    for event in frame_events:
        # select / unselect line (left click)
        Check.select_line(event)

        if mode == 0:
            # move / new line (right click)
            Check.move_line(event)

            # edit line (return)
            Check.edit_line(event)

            # edit line (return)
            Check.new_line(event)

        if mode == 1:
            # check start drag (left click)
            Check.start_drag(event)

            # move line (right click)
            Check.move_line(event)

            # combine lines (left click drag)
            Check.combine_line(event)

            # delete line (del)
            Check.delete_line(event)

        if mode == 2:
            # edit line (return)
            Check.edit_line(event)


def edit_event_loop():
    frame_events = pg.event.get()

    check_exit(frame_events)

    check_next_mode(frame_events)
    do_action(frame_events)
    draw_mode(frame_events)


def main():
    global mode, draw_text, game_screen, pg_text_img, data
    # new_image('spa_text_glossary_perfect')

    mode = 0
    draw_text = True

    data = DataClass()
    print(data[0])
    pg.init()
    clock = pg.time.Clock()

    text_image_dir = 'selected_image.jpg'
    pg_text_img = pg.image.load(text_image_dir)
    # new_image('spa_text_glossary_perfect')

    game_screen = pg.display.set_mode((pg_text_img.get_size()))
    pg.display.set_caption('add/move lines')

    while True:
        edit_event_loop()

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
