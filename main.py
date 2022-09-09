import lisseners
from edit_input import EditCallFuncs
from data import DataClass, new_image
import pygame as pg
import draw

data = DataClass()

pg.init()

# new_image('spa_text_glossary_perfect')

# game_screen = pg.display.set_mode(pg_text_img.get_size())
text_image_dir = 'selected_image.jpg'
pg_text_img = pg.image.load(text_image_dir)

game_screen = pg.display.set_mode((pg_text_img.get_size()))
pg.display.set_caption('add/remove words')
clock = pg.time.Clock()

while True:
    frame_events = pg.event.get()

    lisseners.listen(frame_events)

    for event in frame_events:
        if event.type == pg.QUIT:
            pg.quit()
            # DataJson.save_data_to_jason()
            quit()

    game_screen.fill((255, 255, 255))
    draw.draw_lines(EditCallFuncs.get_selected(), game_screen)

    draw.draw_combine_line(EditCallFuncs.get_selected(), game_screen)
    # DragCheck.draw_select_box()
    EditCallFuncs.edit_modes(frame_events)

    pg.display.flip()
    clock.tick(60)
