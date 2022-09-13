import edit_input
import lisseners
from edit_input import EditCallFuncs, Basic
from data import DataClass
import pygame as pg
import draw

data = DataClass()
mode = 0

pg.init()


def check_exit(frame_events):
    for event in frame_events:
        if event.type == pg.QUIT:
            pg.quit()
            # DataJson.save_data_to_jason()
            quit()


def check_next_mode(frame_events):
    global mode, font, draw_text
    # next mode (return + ctrl)
    # todo change the order things happen 1. 'add/move lines' 2. combine/delete/move 3. edit lines
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

    if draw_text:
        lisseners.listen(frame_events)
        game_screen.fill((255, 255, 255))

        draw.draw_lines(EditCallFuncs.get_selected(), game_screen)

        if mode == 0:
            draw.draw_pointer(EditCallFuncs.get_selected(), lisseners.Text.get_pointer_pos(), game_screen)

        if mode == 1:
            draw.draw_combine_line(EditCallFuncs.get_selected(), game_screen)
            draw.draw_translations_box(edit_input.Basic.find_translation(), game_screen)

        if mode == 2:
            draw.draw_pointer(EditCallFuncs.get_selected(), lisseners.Text.get_pointer_pos(), game_screen)

    else:
        game_screen.blit(pg_text_img, (0, 0))


def edit_event_loop():
    frame_events = pg.event.get()

    check_exit(frame_events)
    check_next_mode(frame_events)

    EditCallFuncs.edit_modes(frame_events, mode)

    # draw.draw_line_box(game_screen)
    # draw.draw_top_line(game_screen)


# new_image('spa_text_glossary_perfect')

# game_screen = pg.display.set_mode(pg_text_img.get_size())
text_image_dir = 'selected_image.jpg'
pg_text_img = pg.image.load(text_image_dir)

font = pg.font.SysFont('Helvatical bold', 24)
clock = pg.time.Clock()

game_screen = pg.display.set_mode((pg_text_img.get_size()))
pg.display.set_caption('add/move lines')

draw_text = True

while True:
    edit_event_loop()

    pg.display.flip()
    clock.tick(60)
