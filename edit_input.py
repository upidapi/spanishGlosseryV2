from general_funcs import *
from data import DataClass
import pygame as pg
import lisseners

line_data = DataClass()
pg.init()

# font = pg.font.SysFont('Helvatical bold', 24)


class Basic:
    @staticmethod
    def set_line_size(index):
        text_size = get_size_of_text(line_data[index, 'text'])

        line_data[index, 'width'] = text_size[0]
        line_data[index, 'height'] = text_size[1]

    @staticmethod
    def edit_line(index, text):
        line_data[index, 'text'] = text
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
        one_space = get_size_of_text(' ')[0]
        line_data[l1_index, 'width'] = line_data[l1_index, 'width'] + one_space + line_data[l2_index, 'width']
        line_data[l1_index, 'text'] = line_data[l1_index, 'text'] + ' ' + line_data[l2_index, 'text']
        del line_data[l2_index]

    @staticmethod
    def find_translation():
        unsorted_line = line_data['all']
        unsorted_line.sort(key=lambda x: x['y'])

        tolerance = 40

        last_line = unsorted_line[0]
        line_y_group = []

        y_lines = []

        differance = 0

        for line in unsorted_line:
            differance.append(line['y'] - last_line['y'])
            if last_line['y'] <= line['y'] <= last_line['y'] + tolerance:
                line_y_group.append(line)
            else:
                return_data = get_multiple_lines_bounding_box(line_y_group)
                pos = return_data[0:2]
                size = return_data[2:4]
                y_lines.append((pos, size))

                line_y_group = []

            last_line = line

        return_data = get_multiple_lines_bounding_box(line_y_group)
        pos = return_data[0:2]
        size = return_data[2:4]
        y_lines.append((pos, size))

        print(differance)
        return y_lines


class EditCallFuncs:
    selected_line = None
    drag = False

    @staticmethod
    def get_selected():
        return EditCallFuncs.selected_line

    @staticmethod
    def get_drag():
        return EditCallFuncs.drag

    @staticmethod
    def combine_lines(index):
        if EditCallFuncs.selected_line:
            Basic.combine_lines(EditCallFuncs.selected_line, index)

    @staticmethod
    def select_line(index):
        EditCallFuncs.selected_line = index

    @staticmethod
    def edit_modes(frame_events, mode):
        # move / new line (right click)
        # combine lines (left click drag), edit line (return), delete line (backspace)
        # combine corresponding translations (left click drag)

        # move / new (right click)
        # combine (left click drag), edit (return), delete (backspace)
        # combine translations (left click drag)

        for event in frame_events:
            over_line = lisseners.Mouse.check_over_word()

            # select / unselect line (left click)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if over_line:
                    EditCallFuncs.selected_line = over_line
                    lisseners.Text.set_text(line_data[over_line, 'text'])
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                if lisseners.Text.get_text() == '':
                    del line_data[EditCallFuncs.selected_line]

                lisseners.Text.set_text('')
                EditCallFuncs.selected_line = None

            if mode == 0:
                # move / new line (right click)
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                    if not EditCallFuncs.selected_line:
                        Basic.new_line()

                        EditCallFuncs.selected_line = len(line_data) - 1

                    # change position
                    line_data[EditCallFuncs.selected_line, 'x'], line_data[EditCallFuncs.selected_line, 'y']\
                        = pg.mouse.get_pos()

                # edit line (return)
                if EditCallFuncs.selected_line and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    print('e')
                    if lisseners.Text.get_text() == '':
                        del line_data[EditCallFuncs.selected_line]

                    else:
                        Basic.edit_line(EditCallFuncs.selected_line, lisseners.Text.get_text())
                        lisseners.Text.set_text('')

                    EditCallFuncs.selected_line = None

            if mode == 1:
                # check start drag
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and over_line:
                    EditCallFuncs.drag = True

                # combine lines (left click drag)
                if event.type == pg.MOUSEBUTTONUP and event.button == 1 and EditCallFuncs.selected_line:
                    if EditCallFuncs.drag and over_line and EditCallFuncs.selected_line != over_line:
                        Basic.combine_lines(EditCallFuncs.selected_line, over_line)

                        if over_line < EditCallFuncs.selected_line:
                            EditCallFuncs.selected_line -= 1

                        lisseners.Text.set_text(line_data[EditCallFuncs.selected_line, 'text'])

                    EditCallFuncs.drag = False

                # edit line (return)
                if EditCallFuncs.selected_line and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    if lisseners.Text.get_text() == '':
                        del line_data[EditCallFuncs.selected_line]

                    else:
                        Basic.edit_line(EditCallFuncs.selected_line, lisseners.Text.get_text())
                        lisseners.Text.set_text('')

                    EditCallFuncs.selected_line = None

                # delete line (del)
                if EditCallFuncs.selected_line and event.type == pg.KEYDOWN and event.key == pg.K_DELETE:
                    del line_data[EditCallFuncs.selected_line]
                    EditCallFuncs.selected_line = None

            if mode == 2:
                # check start drag
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and over_line:
                    EditCallFuncs.drag = True

                # combine corresponding translations (left click drag)
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if EditCallFuncs.drag and over_line and EditCallFuncs.selected_line != over_line:
                        pass
                        # todo add the save to corresponding translation

                    EditCallFuncs.drag = False
