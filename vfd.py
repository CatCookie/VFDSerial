import serial
import constants
import time
import threading
from constants import LINE_LENGTH, LINES


class Cursor:
    def __init__(self):
        self.row = 1
        self.line = 1

    def set_line(self, line):
        self.line = 1 if line < 1 else LINES if line > LINES else line

    def set_row(self, row):
        self.row = 1 if row < 1 else LINE_LENGTH if row > LINE_LENGTH else row

    def add_line(self, lines):
        self.set_line(self.line + lines)

    def add_row(self, rows):
        self.set_row(self.row + rows)

    def __str__(self):
        return "(%s,%s)" % (self.line, self.row)


class BA63:
    """
    Class for handling a Siemens or Wincor/Nixdorf BA63 display via a RS232 serial port.
    """

    def __init__(self, device, baud=constants.BAUDRATE, parity=constants.PARITY):
        """
        Initializes a Display

        The Arguments are the parameters for the serial connection.
        Device, baudrate and parity.
        """
        self.serial = serial.Serial(device, baud, parity=parity)
        self.cursor = Cursor()
        self.threads = []

    def clear(self):
        """ Clears the display but the cursor remains where it was before. """
        self._send(constants.CLEAR)
        return self.cursor

    def reset(self):
        """ Resets the whole display and the cursor is on the first digit. """
        self._send(constants.CLEAR)
        self.set_position(1, 1)
        return self.cursor

    def _send(self, content):
        """ Send the content to the display. """
        self.serial.write(content)
        self.serial.flush()

    def set_position(self, line, row):
        """ Sets the cursor to the given position. """
        self.cursor.set_row(row)
        self.cursor.set_line(line)
        self._send(constants.CURSOR_POSITION % (line, row))
        return self.cursor

    def newline(self):
        """
        Moves the cursor to the next line.
        If the cursor is already in the second line, the line scrolls up.
        """
        self.cursor.add_line(1)
        self._send(constants.CURSOR_LINEFEED)
        return self.cursor

    def carriage_return(self):
        """ Moves the cursor to the start of the line"""
        self.cursor.set_row(1)
        self._send(constants.CURSOR_LINE_START)
        return self.cursor

    def write(self, text, line=None, row=None):
        """
        Writes the given text to the display
        If the text is to long, it will be truncated

        Handles control sequences like carriage return and linefeed separately,
        to update to the correct cursor position.
        """

        if line is not None:
            self.set_position(line, self.cursor.row)

        if row is not None:
            self.set_position(self.cursor.line, row)

        to_send = ''
        for char in text:
            if char == '\r':
                self._write_chunk(to_send)
                to_send = ''
                self.carriage_return()
            elif char == '\n':
                self._write_chunk(to_send)
                to_send = ''
                self.newline()
            else:
                to_send += char

        self._write_chunk(to_send)
        return self.cursor

    def _write_chunk(self, chunk):
        """ Truncates the text which shall be written """
        if self.cursor.row - 1 + len(chunk) > LINE_LENGTH:
            self._send(chunk[0:-((len(chunk) + self.cursor.row - 1) - LINE_LENGTH)])
            self.cursor.set_row(LINE_LENGTH)
        else:
            self.cursor.add_row(len(chunk))
            self._send(chunk)

    def scroll(self, initial_text, line, step_delay=0.25, wrap=False):
        """
        Scrolls the given text on the given line.

        With step_delay you can tweak the scroll speed.
        If wrapping is enabled, the text flows continuously with a space in between the end and the beginning.
        Multiple scrollings on the same line behave like expected.
        """
        def _do():
            i = 0
            while getattr(threading.currentThread(), "do_run", True):
                text = getattr(threading.current_thread(), "text", initial_text)
                if wrap:
                    chars = (text + ' ') * ((LINE_LENGTH + len(text)) / (len(text) + 1) + 1)
                    iteration_length = len(text)
                else:
                    chars = ' ' * (LINE_LENGTH - 1) + text + ' ' * (LINE_LENGTH - 1)
                    iteration_length = LINE_LENGTH + len(text) - 1

                self.write(chars[i:i + LINE_LENGTH], line=line, row=1)
                time.sleep(step_delay)
                if not getattr(threading.currentThread(), "do_pause", False):
                    i = i + 1 if i < iteration_length else 0

        t = threading.Thread(name="Line %s" % line, target=_do)
        self.threads.append(t)
        t.start()


    def scroll_stop(self, line):
        """ Stops the scrolling on the given line """
        thread = [t for t in self.threads if t.name == "Line %s" % line][0]
        thread.do_run = False
        self.threads.remove(thread)
        thread.join()
        self.cursor.set_row(1)
        self.cursor.set_line(line)
        return self.cursor

    def scroll_pause(self, line):
        """ Pauses the scrolling on the given line """
        thread = [t for t in self.threads if t.name == "Line %s" % line][0]
        thread.do_pause = True

    def scroll_continue(self, line):
        """ Continues the scrolling on the given line """
        thread = [t for t in self.threads if t.name == "Line %s" % line][0]
        thread.do_pause = False

    def scroll_update(self, line, text):
        """ updates the scrolling text on the given line """
        thread = [t for t in self.threads if t.name == "Line %s" % line][0]
        thread.text = text
