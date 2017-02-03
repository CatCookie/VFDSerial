import vfd
import time

display = vfd.BA63("/dev/ttyAMA0")

display.reset()
time.sleep(1)
display._send("    Hallo RasPi!")

display.set_position(2, 3)
display._send("ABC")
