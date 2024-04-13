from waveshare_epd import epd7in5b_V2
import time

epd = epd7in5b_V2.EPD()

print("Clearing screen")

epd.init()
epd.Clear()
epd.sleep()

exit()
