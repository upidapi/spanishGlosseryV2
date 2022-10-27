def make_answer_sheet():
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
    pass

