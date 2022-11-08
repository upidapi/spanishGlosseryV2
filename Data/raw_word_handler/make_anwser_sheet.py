# import regex

"""
makes an answer_sheet that the check_correct.py can use to check if a word was typed right

to do this it uses the following parts
    () => chain statement
        # used manly to chain 'or statements' and 'text statements'

        (a, b, c)
        if you're at 'a' you have to go to next 'b'
        you always have to go to the next index

    [] => or statement
        (x, [a, b, c], y)
        if you're at 'x' you have to go to 'a', 'b' or 'c'
        if you're at 'a', 'b' or 'c' you have to go to y

        when entering you can go to any index (in the list) when entering
        when exiting you have to go to after the list

using these we can also create
    optionals => ['optional text', '']
        a part that doesn't have to be typed but can be (if you start you can't end)

    or => ['text 1', 'text 2']
        an or statement (se more above)

    full_sheet => (['text 1', ''], 'text 2', ['text 3', 'text 4'], 'text 4') # (e.g)
                   ^^^^^^^^^^^^^^  ^^^^^^^
                      optional
"""
import re


def rm_invalid():

def capture_between(inp, a, b):
    between = []

    # finds all possible between instances
    starts = [x for x in re.finditer(a, inp)]
    stops = [x for x in re.finditer(b, inp)]

    for start in starts:
        # start_text = start.group(0)
        start_start = start.span()[0]
        # start_end = start.span()[1]

        for stop in stops:
            stop_end = stop.span()[1]
            if start_start < stop_end:
                between.append(inp[start_start:stop_end])

    # remove invalid between instances
    for i, instance in enumerate(between):
        for char in instance:
            if char:
                pass


def tes(imp, start, end, a, b):
    for i in range(start, end):
        # if it starts with a
        re.findall(f"^{a}", imp[i:])



capture_between('hej (vad) nä d(ej)', '\(', '\)')
