import vfd
import time

d = vfd.BA63("/dev/ttyAMA0")

print d.reset()
time.sleep(1)
print d.write("Hallo RasPi!", 1, 5)


# print display.write("a\r\nb\rcc\ndd\nee\r\nfff\rg")
