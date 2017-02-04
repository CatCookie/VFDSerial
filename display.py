import vfd
from time import sleep, ctime

d = vfd.BA63("/dev/ttyAMA0")

d.reset()
d.write("Hello World! \r\n", 1, 5)

d.scroll("", line=2, step_delay=0.2)

while 1:
    sleep(0.1)
    d.scroll_update(2, ctime()[0:-4])


