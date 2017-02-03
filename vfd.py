import serial
import sequences

BAUDRATE = 9600
PARITY = serial.PARITY_ODD


class Cursor:
    def __init__(self):
        self.x = 1
        self.y = 1


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

    def reset(self):
        """ Resets the whole display and the cursor is on the first digit. """
        self._send(sequences.CLEAR)
        self.set_position(1, 1)

    def _send(self, content):
        """ Send the content to the display. """
        self.serial.write(content)
        self.serial.flush()

    def set_position(self, line, row):
        """ Sets the cursor to the given position. """
        self._send(sequences.CURSOR_POSITION % (line, row))




