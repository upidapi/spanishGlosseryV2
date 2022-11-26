from Structure.Helpers import get_all_next_possible, get_start_points
from Structure.Constructor import convert


def get_text_starts(structure):
    # allows you to skip leading spaces
    # e.g. if you'd need " abc", technically, for "(el) abc"
    # you can instead use "abc"
    text_starts = []  # where the actual text starts (in the example the "a" pos)
    possible = get_start_points(structure)
    next_starts = []
    i = 0
    while True:
        for possibility in possible:
            if structure[possibility] == " ":
                next_start = get_all_next_possible(possibility, structure)

                for part in next_start:
                    if part is None:
                        text_starts.append(possibility)
                    else:
                        next_starts.append(part)
            else:
                text_starts.append(possibility)

        if len(next_starts) == 0:
            return text_starts

        possible = next_starts
        next_starts = []

        i += 1


def check_correct(inp: str, structure) -> bool:
    """
    checks if the inp follows the structure
    :param inp: the thing to check if it follows the structure
    :param structure: consists of ChainStatements, OrStatements and str(s)
    :return: whether if inp follows the structure
    """
    inp = inp.strip()

    possible = get_text_starts(structure)
    if None in possible and len(inp) == 0:
        return True
    possible = [possibility for possibility in possible if possibility is not None]

    next_starts = []
    i = 0
    while True:
        # allows you to skip trailing spaces
        # e.g. if you'd need "abc ", technically, for "abc /ue/"
        # you can instead use "abc"

        char = inp[i] if i < len(inp) else " "

        for possibility in possible:
            p_char = structure[possibility]

            if p_char == char:
                next_start = get_all_next_possible(possibility, structure)

                for part in next_start:
                    if part is None:
                        if i >= len(inp) - 1:
                            return True
                    else:
                        next_starts.append(part)

        if len(next_starts) == 0:
            return False

        possible = next_starts
        next_starts = []
        i += 1


# data = convert("((el) abc) /ue/; likes /ie/")
# data.multi_line_print()
# print(check_correct("", data))
