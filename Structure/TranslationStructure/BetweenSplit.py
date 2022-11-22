import re

from Structure.Helpers import OrStatement, ChainStatement


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


# todo make this return a OrStatement(str, '') where it matched
#  that's whats causing problems
def get_between(inp: str, between: tuple[str, str]):
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


def make_between_optional(inp: str, between: tuple[str, str]):
    between_data = get_between(inp, between)

    def recursion(inu):
        out = []
        for thing in inu:
            if type(thing) is list:
                out.append(recursion(thing))
            else:
                out.append(thing)
        if type(inu) is tuple:
            return ChainStatement(*out)
        return OrStatement(ChainStatement(*out), '')

    return recursion(tuple(between_data))


# print(get_between("(he(im)(you))", ("\(", "\)")))
# print(make_between_optional("(he(im)(you))", ("\(", "\)")))
# print(get_between("hello (he( im)( you)) wa; likes", ("\(", "\)")))
# print(make_between_optional("hello (im) wut ((hello) nah (the))", ('\(', '\)')))
