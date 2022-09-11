import lisseners
from edit_input import EditCallFuncs, Basic
from data import DataClass, new_image
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
    global mode, font
    # next mode (return + ctrl)
    for event in frame_events:
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN and pg.key.get_mods() & pg.KMOD_CTRL:
            mode += 1

            if mode == 1:
                pg.display.set_caption('combine/edit/delete lines')
                for i in range(len(data)):
                    Basic.set_line_size(i)

            if mode == 2:
                pg.display.set_caption('combine translations')

    if mode == 0:
        draw.draw_pointer(EditCallFuncs.get_selected(), lisseners.Text.get_pointer_pos(), game_screen)

    if mode == 1:
        draw.draw_pointer(EditCallFuncs.get_selected(), lisseners.Text.get_pointer_pos(), game_screen)
        draw.draw_combine_line(EditCallFuncs.get_selected(), game_screen)

    if mode == 2:
        draw.draw_combine_line(EditCallFuncs.get_selected(), game_screen)


def edit_event_loop():
    frame_events = pg.event.get()
    lisseners.listen(frame_events)

    check_exit(frame_events)
    check_next_mode(frame_events)

    EditCallFuncs.edit_modes(frame_events, mode)

    draw.draw_lines(EditCallFuncs.get_selected(), game_screen)


# new_image('spa_text_glossary_perfect')

# game_screen = pg.display.set_mode(pg_text_img.get_size())
text_image_dir = 'selected_image.jpg'
pg_text_img = pg.image.load(text_image_dir)

font = pg.font.SysFont('Helvatical bold', 24)

game_screen = pg.display.set_mode((pg_text_img.get_size()))
clock = pg.time.Clock()
pg.display.set_caption('add/move/edit lines')

while True:
    game_screen.fill((255, 255, 255))

    edit_event_loop()

    pg.display.flip()
    clock.tick(60)
