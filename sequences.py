""" defindes the control sequences for the display """

CLEAR = "\x1B\x5B\x32\x4A"
CURSOR_LINE_START = "\x0D"
CURSOR_LINEFEED = "\x0A"
CURSOR_BACK = "\x08"
CURSOR_CLEAR_TO_LINE_END = "\x1B\x5B\x30\x4B"
CURSOR_POSITION = "\x1B\x5B%s\x3B%s\x48"
