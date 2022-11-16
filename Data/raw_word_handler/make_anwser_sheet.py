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
# from helper_functions import set_pointer_data, get_pointer_data, get_next_open_scopess


def split(inp, at):
    return re.split(at, inp)


def get_combined_matches(inp, between: tuple[str, str]):
    if not inp and type(inp) is list:
        return []

    starts = [x for x in re.finditer(between[0], inp)]
    stops = [x for x in re.finditer(between[1], inp)]
    ordered = [{"text": x.group(0), "span": x.span(), "start": False, "stop": False}
               for x in re.finditer(f"{between[0]}|{between[1]}", inp)]

    for i in range(len(ordered)):
        if any(
                ordered[i]["text"] == start.group(0) and
                ordered[i]["span"][0] == start.span()[0] for
                start in starts
        ):
            ordered[i]["start"] = True

        if any(
                ordered[i]["text"] == stop.group(0) and
                ordered[i]["span"][0] == stop.span()[0] for
                stop in stops
        ):
            ordered[i]["stop"] = True

    return ordered


def get_between(inp, between: tuple[str, str]):
    # todo currently it removes unnecessary parentheses might cause problems
    """
    :param inp: ex "a ((b) c (d)) (e)"
    :param between: ex ("\(", "\)")
    :return: a, ((b), c, (d)), e
    """
    def add_between(a, b):
        # if there is nothing between don't add it
        part = inp[a: b]
        if part == "":
            return []
        return [part]

    ordered_matches = get_combined_matches(inp, between)

    valid = []
    last_end = 0
    i = 0

    while True:
        if i == len(ordered_matches):
            break

        if ordered_matches[i]["start"]:
            # I don't know why it's here
            # valid += inp[ordered_matches[i]["span"][1]: ordered_matches[i]["span"][1]]

            count = 1

            for j in range(i + 1, len(ordered_matches)):
                # prioritising stopping
                if ordered_matches[j]['stop']:
                    count -= 1
                elif ordered_matches[j]['start']:
                    count += 1

                if count == 0:
                    # adds the part before capture
                    before_start = ordered_matches[i]["span"][0]
                    valid += add_between(last_end, before_start)
                    last_end = ordered_matches[j]["span"][1]

                    # adds the captured part as well as processing the insides
                    after_start = ordered_matches[i]["span"][0] + 1
                    before_stop = ordered_matches[j]["span"][1] - 1
                    sub_span = inp[after_start: before_stop]

                    sub_between = get_between(sub_span, between)
                    if sub_between:
                        valid.append(sub_between)

                    # continue after capture to not reprocess the last capture
                    # note it's not j + 1 due to the i += 1 after
                    i = j
                    break

        i += 1

    return valid + add_between(last_end, len(inp))


# print(get_between("hello im a ((blue) duck)", ("/", "/")))
# print(split("hello; hi", ";"))

# x = [1, 2, 3, 4]
# x[2:3] = ["a", "b", "c"]
# print(x)


def clean(inp):
    re_splits = [";", ":", "\|"]

    parts = [inp]

    for re_split in re_splits:
        for i in range(len(parts)):
            parts[i] = split(parts[i], re_split)

    print(parts)

# SplitPatterns.test_all("/", "hello im/you are/hes the car/green fast bicycle//house")
