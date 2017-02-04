import serial
import sequences

BAUDRATE = 9600
PARITY = serial.PARITY_ODD


class Cursor:
    def __init__(self):
        self.row = 1
        self.line = 1

    def set_line(self, line):
        self.line = 1 if line < 1 else 2 if line > 2 else line

    def set_row(self, row):
        self.row = 1 if row < 1 else 20 if row > 20 else row

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

    def __init__(self, device, baud=BAUDRATE, parity=PARITY):
        """
        Initializes a Display

        The Arguments are the parameters for the serial connection.
        Device, baudrate and parity.
        """
        self.serial = serial.Serial(device, baud, parity=parity)
        self.cursor = Cursor()

    def clear(self):
        """ Clears the display but the cursor remains where it was before. """
        self._send(sequences.CLEAR)
        return self.cursor

    def reset(self):
        """ Resets the whole display and the cursor is on the first digit. """
        self._send(sequences.CLEAR)
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
        self._send(sequences.CURSOR_POSITION % (line, row))
        return self.cursor

    def newline(self):
        """
        Moves the cursor to the next line.
        If the cursor is already in the second line, the line scrolls up.
        """
        self.cursor.add_line(1)
        self._send(sequences.CURSOR_LINEFEED)
        return self.cursor

    def carriage_return(self):
        """ Moves the cursor to the start of the line"""
        self.cursor.set_row(1)
        self._send(sequences.CURSOR_LINE_START)
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
                self.cursor.add_row(len(to_send))
                self._send(to_send)
                to_send = ''
                self.carriage_return()
            elif char == '\n':
                self.cursor.add_row(len(to_send))
                self._send(to_send)
                to_send = ''
                self.newline()
            else:
                to_send += char

        self.cursor.add_row(len(to_send))
        self._send(to_send)
        return self.cursor


