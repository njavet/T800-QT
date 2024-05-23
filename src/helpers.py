import itertools


def format_msg(message: str, line_length: int = 64) -> str:
    """
    The `format_msg` function splits a text message into lines of maximum
    line_length characters each.
    """
    m_len = len(message)
    # message is smaller than line length and don't need to be changed
    if m_len <= line_length:
        return message

    words = message.split()
    first_word = words[0]
    len_first_word = len(first_word)
    # the first word of the message is longer than the line length
    if line_length <= len_first_word:
        first_word_part0 = first_word[:line_length]
        first_word_part1 = first_word[line_length:]
        msg_rest = ' '.join([first_word_part1] + words[1:])
        return '\n'.join([first_word_part0, format_msg(msg_rest)])

    # take as many words as possible for a line and solve the rest with recursion
    words_length = [len(word) + 1 for word in words]
    ac = itertools.accumulate(words_length, initial=-1)
    tw = itertools.takewhile(lambda wl: wl <= line_length, ac)
    ind = len(list(tw)) - 1
    first_part = ' '.join(words[:ind])
    second_part = format_msg(' '.join(words[ind:]))
    return '\n'.join([first_part, second_part])


