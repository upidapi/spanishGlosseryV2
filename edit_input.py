from data import DataClass
import pygame as pg
import lisseners

line_data = DataClass()
font = pg.font.SysFont('Helvatical bold', 24)


class Basic:
    @staticmethod
    def set_line_size(index):
        text = line_data[index]['text']
        text_img = font.render(text, True, (0, 0, 0))
        text_size = text_img.get_size()

        line_data[index]['width'] = text_size[0]
        line_data[index]['height'] = text_size[1]

    @staticmethod
    def edit_line(index, text):
        line_data[index]['text'] = text
        Basic.set_line_size(index)

    @staticmethod
    def new_line():
        data = {
            'text': '',
            'x': 0,
            'y': 0,
            'width': 0,
            'height': 0
        }

        line_data.append(data)

    @staticmethod
    def combine_lines(l1_index, l2_index):
        # gets the width of one space
        space_img = font.render(' ', True, (0, 0, 0))
        one_space = space_img.get_size()[0]
        line_data[l1_index, 'width'] = line_data[l1_index, 'width'] + one_space + line_data[l2_index, 'width']
        line_data[l1_index, 'text'] = line_data[l1_index, 'text'] + ' ' + line_data[l2_index, 'text']
        del line_data[l2_index]


class EditCallFuncs:
    selected_line = None
    drag = [False, None]

    @staticmethod
    def combine_lines(index):
        if EditCallFuncs.selected_line:
            Basic.combine_lines(index, EditCallFuncs.selected_line)

    @staticmethod
    def select_line(index):
        EditCallFuncs.selected_line = index

    @staticmethod
    def edit_modes(frame_events):
        # move / new line (right click)
        # combine lines (left click drag), edit line (return), delete line (backspace)
        # combine corresponding translations (left click drag)

        # move / new (right click)
        # combine (left click drag), edit (return), delete (backspace)
        # combine translations (left click drag)

        mode = 0

        for event in frame_events:
            # general things

            # next mode (return + ctrl)
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN and pg.key.get_mods() & pg.KMOD_CTRL:
                mode += 1

                if mode == 0:
                    select_line = lisseners.Mouse(1, EditCallFuncs.selected_line)

                if mode == 1:
                    combine_line = lisseners.Mouse(2, EditCallFuncs.combine_lines)
                    new_line = lisseners.Mouse(3, Basic.new_line)

            over_line = lisseners.Mouse.check_over_word()

            # select / unselect line (left click)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if over_line:
                    EditCallFuncs.selected_line = over_line
                    lisseners.Text.set_text(line_data[over_line, 'text'])
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                EditCallFuncs.selected_line = None

            # check start drag
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and over_line:
                EditCallFuncs.drag = True

            if mode == 0:
                # move / new line (right click)
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                    if not EditCallFuncs.selected_line:
                        Basic.new_line()

                    last_item = len(line_data)
                    # change position
                    line_data[last_item, 'x'], line_data[last_item, 'y'] = pg.mouse.get_pos()

            if mode == 1:
                # combine lines (left click drag)
                if event.type == pg.MOUSEBUTTONUP and event.button == 1 and EditCallFuncs.selected_line:
                    if EditCallFuncs.drag and over_line and EditCallFuncs.selected_line != over_line:
                        Basic.combine_lines(EditCallFuncs.selected_line, over_line)

                    EditCallFuncs.drag = False

                # edit line (return)
                if EditCallFuncs.selected_line and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    Basic.edit_line(EditCallFuncs.selected_line, lisseners.Text.get_text())

                # delete line (backspace)
                if EditCallFuncs.selected_line and event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                    del line_data[EditCallFuncs.selected_line]

            if mode == 2:
                # combine corresponding translations (left click drag)
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if EditCallFuncs.drag and over_line and EditCallFuncs.selected_line != over_line:
                        pass
                        # todo add the save to corresponding translation

                    EditCallFuncs.drag = False
