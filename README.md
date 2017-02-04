# VFDSerial
A Framework to control the Siemens BA63 VF Display over the serial port.

## How to use
You have to modify the display to connect to the standard RS232 and get power.
I won' explain this here, you can find very good tutorials on Google or ask me directly.

Hook up the display via a serial port (if you don't have one, get an USB-Adapter).
Import the `vfd` module and go for it.

    import vfd
    display = vfd.BA63('/dev/ttyAMA0')
    display.write('Hello World')

You can find an extended example in the file `display.py`

Be careful when you use the scrolling features.
Don't start more than one scrolling on the same display line.
They may not behave as you expect.

## Note
For the Raspberry PI you will need an UBS-Serial adapter cable.
..or you have to modify the display to accept the voltage levels of the onboard UART of the Pi.
Feel free to ask me.
