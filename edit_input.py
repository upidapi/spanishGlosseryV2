from general_funcs import *
from data import DataClass
import pygame as pg
import lisseners

line_data = DataClass()
pg.init()


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
        unsorted_line = line_data['all'].copy()
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
                bounding_box = wh_to_chords(get_multiple_lines_bounding_box(current_lines))
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


class Check:
    selected = None
    drag = False

    # api funcs
    @staticmethod
    def get_selected():
        return Check.selected

    @staticmethod
    def get_drag():
        return Check.drag

    @staticmethod
    def combine_lines(index):
        if Check.selected:
            Basic.combine_lines(Check.selected, index)

    @staticmethod
    def select_line_extra(index):
        Check.selected = index

    # check funcs
    @staticmethod
    def start_drag(event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and\
                lisseners.Mouse.check_over_word() is not None:
            Check.drag = True

    @staticmethod
    def stop_drag(event):
        if event.type == pg.MOUSEBUTTONUP and event.button == 1 and\
                lisseners.Mouse.check_over_word() is not None:
            Check.drag = False

    @staticmethod
    def select_line(event):
        """
        checks if you have selected/unselected a line
        """
        over_line = lisseners.Mouse.check_over_word()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if over_line is not None:
                Check.selected = over_line
                lisseners.Text.set_text(line_data[over_line, 'text'])
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            if lisseners.Text.get_text() == '':
                del line_data[Check.selected]

            lisseners.Text.set_text('')
            Check.selected = None

    @staticmethod
    def move_line(event):
        """
        move line (trigger = right click)

        :param event: the "pg.event"
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and Check.selected is not None:
            # change position
            line_data[Check.selected, 'x'], line_data[Check.selected, 'y'] \
                = pg.mouse.get_pos()

    @staticmethod
    def new_line(event):
        """
        new/move line (trigger = right click)

        :param event: the "pg.event"
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            if Check.selected is None:
                print('new')
                Basic.new_line()

                Check.selected = len(line_data) - 1

            # change position
            Check.move_line(event)

    @staticmethod
    def edit_line(event):
        """
        edit line (trigger = return)

        :param event: the "pg.event"
        """
        if Check.selected is not None and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            if lisseners.Text.get_text() == '':
                del line_data[Check.selected]

            else:
                Basic.edit_line(Check.selected, lisseners.Text.get_text())
                lisseners.Text.set_text('')

            Check.selected = None

    @staticmethod
    def combine_line(event):
        """
        combines the line you're over with you're dragging from (trigger = return)

        :param event: the "pg.event"
        """
        over_line = lisseners.Mouse.check_over_word()

        if event.type == pg.MOUSEBUTTONUP and event.button == 1 and Check.selected is not None:
            if Check.drag and Check.selected != over_line and over_line is not None:
                Basic.combine_lines(Check.selected, over_line)

                if over_line < Check.selected:
                    Check.selected -= 1

                lisseners.Text.set_text(line_data[Check.selected, 'text'])

            Check.drag = False

    @staticmethod
    def delete_line(event):
        """
        delete line (trigger = del)

        :param event: the "pg.event"
        """
        if Check.selected is not None and event.type == pg.KEYDOWN and event.key == pg.K_DELETE:
            del line_data[Check.selected]
            Check.selected = None


# class EditCallFuncs:
#     @staticmethod
#     def edit_modes(frame_events, mode):
#         # move / new (right click)
#         # combine (left click drag), move (right click), delete (backspace)
#         # edit (return)
#
#         for event in frame_events:
#             # select / unselect line (left click)
#             Check.select_line(event)
#
#             if mode == 0:
#                 # move / new line (right click)
#                 Check.move_line(event)
#
#             # noinspection SpellCheckingInspection
#             if mode == 1:
#                 # check start drag (left click)
#                 Check.start_drag(event)
#                 # move line (right click)
#                 Check.move_line(event)
#
#                 # combine lines (left click drag)
#                 Check.combine_line(event)
#
#                 # delete line (del)
#                 Check.delete_line(event)
#
#             if mode == 2:
#                 # edit line (return)
#                 Check.edit_line(event)
