def format_msg(message: str, line_length: int = 48) -> str:
    """
    The `format_msg` function splits a text message into lines of maximum 48
    characters each.
    :return: The `format_msg` method returns a formatted message where the
    original message text is split into lines with a maximum of 48 characters
    per line. The method processes the input message text to ensure that each
    line does not exceed the character limit and handles cases where words are
    too long or lines are too long. The formatted message is returned as a single
    string with line breaks.
    """
    lines = []
    words = message.split()
    curr = 0
    curr_line = []
    for i, word in enumerate(words):
        curr += len(word)
        # Case 1: the word is too long for a single line
        if len(word) > line_length:
            if len(curr_line) == 0:
                while word:
                    lines.append(word[:line_length])
                    word = word[line_length:]
            else:
                lines.append(' '.join(curr_line))
                while word:
                    curr_line.append(word[:line_length])
                    word = word[line_length:]
                    lines.append(' '.join(curr_line))
                curr = 0
                curr_line = []
        # Case 2: the line is too long and has more than 48 characters
        elif curr > line_length:
            curr_line.append(word)
            lines.append(' '.join(curr_line))
            curr = 0
            curr_line = []
        # Case 3: the line still has space
        else:
            curr_line.append(word)

    lines.append(' '.join(curr_line))
    new_msg = '\n'.join(lines)
    return new_msg
