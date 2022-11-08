import regex

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
                    ^^^^^^^^^^^^    ^^^^^^    ^^^^^^^^^^^^^^^^^^    ^^^^^^
                      optional      text              or             text
"""


# def find_optionals(word: list[dict] | list,
#                    regex_match_expression: str,
#                    match_remove_slice: slice = slice(None, None)):
#     import re
#
#     """
#     :param word: a list of parts of a word
#     :param regex_match_expression: a regex str to try to match to
#     :return: finds and sections the text into optional or necessary parts
#     """
#
#     # adds to optional if the amount of characters between start key and end key is less than remove_ken
#     for i, part in enumerate(word):
#
#         text = part['text']
#         matches = re.finditer(regex_match_expression, text)
#
#         split_words = []
#         next_start = 0
#         for match in matches:
#             start = match.span()[0]
#
#             # text part before match
#             split_words += get_add_part(
#                 text=text[next_start:start],
#                 option=part['type']  # defaults to "parent's" type
#             )
#
#             # match text part
#             split_words += get_add_part(
#                 text=match.group(0)[match_remove_slice],
#                 option='optional'
#             )
#
#             next_start = match.span()[1]
#
#         # text part after last match
#         split_words += get_add_part(
#             text=text[next_start:len(text)],
#             option=part['type']  # defaults to "parent's" type
#         )
#
#         # the i+1 is so that the current part doesn't get added
#         word = word[:i] + split_words + word[(i + 1):]
#
#     return word


def find_x(re_ex, inp):
    matches = regex.finditer(re_ex, inp, overlapped=True)
    for match in matches:
        print(match)


# find_x(r'/[^/]*/', '/a/b/c/')
find_x(r'\([^\(\)]*\)', '(a(b)c)')
