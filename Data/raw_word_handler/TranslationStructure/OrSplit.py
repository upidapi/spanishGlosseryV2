import re

from Data.raw_word_handler.HelperFunctions import get_next_open_scopes


class SplitPatterns:
    """
    >>> re.findall(SplitPatterns.restrictive("/"), "hello im/you are/hes the car/bicycle/house")
    ['im/you', 'are/hes']
    >>> re.findall(SplitPatterns.normal("/"), "hello im/you are/hes the car/bicycle/house")
    ['im/you', 'are/hes', 'car/bicycle/house']
    >>> re.findall(SplitPatterns.permissive("/"), "hello im/you are/hes the car/bicycle/house")
    ['im/you are/hes', 'car/bicycle/house']
    >>> re.findall(SplitPatterns.greedy("/"), "hello im/you are/hes the car/bicycle/house")
    ['im/you are/hes the car/bicycle/house']
    """

    LARGE_NUMBER = 1000

    @staticmethod
    def mater_function(at, space_tolerance, extra_or_statements):
        wc = f"[^ {at}]+"  # word capture

        return re.compile(
            f"(?:(?<=^)|(?<= ))"  # is at start or starts with " "
            f"({wc}{at}"  # word before
            f"(?: |){wc}"  # first word inside
            f"(?: {wc}){{,{space_tolerance}}}{at}"  # extra words 
            f"{{,{extra_or_statements}}}"  # extra or statements
            f"{wc})"  # word after
            f"(?:(?=$)|(?= ))")  # is at end or ends with " ")

    @staticmethod
    def restrictive(at):
        return SplitPatterns.mater_function(at, 0, 0)

    @staticmethod
    def normal(at):
        return SplitPatterns.mater_function(at, 0, SplitPatterns.LARGE_NUMBER)

    @staticmethod
    def permissive(at):
        return SplitPatterns.mater_function(at, 1, SplitPatterns.LARGE_NUMBER)

    @staticmethod
    def greedy(at):
        return SplitPatterns.mater_function(at, SplitPatterns.LARGE_NUMBER, SplitPatterns.LARGE_NUMBER)

    @staticmethod
    def test_all(at, test_str):
        exclusions = ["__", "test_all", "mater_function"]
        valid = [func for func in dir(SplitPatterns)
                 if callable(getattr(SplitPatterns, func))
                 and not any(func.startswith(exclude) for exclude in exclusions)]

        for func in valid:
            print(func, re.findall(getattr(SplitPatterns, func)(at), test_str))


# while True:
#     pointer = get_next_open_scopes()
