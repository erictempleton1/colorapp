from neopixel import *

import argparse
import signal
import sys
import sqlite3
import time

def signal_handler(signal, time):
    color_wipe(strip, Color(0, 0, 0))
    sys.exit(0)

def opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", action="store_true", help="clear the display on exit")
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)

#  RGB color code definitions
COLOR_CODES = {
    "blue": Color(0, 255, 0),
    "green": Color(0, 0, 255),
    "orange": Color(255, 128, 0),
    "pink": Color(255, 0, 255),
    "purple": Color(127, 0, 255),
    "red": Color(255, 0, 0),
    "white": Color(127, 127, 127),
    "yellow": Color(255, 255, 0)
}

# action dispatcher
ACTIONS = {"wipe": color_wipe}

RUN_TIME = 120  # how long to run each animation in seconds

# LED strip configuration
LED_COUNT = 16  # number of LED pixels
LED_PIN = 18  # GPIO pin connected to the pixels
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45, or 53
LED_STRIP = ws.WS2811_STRIP_GRB  # strip type and color ordering

def color_wipe(strip, colors):
    """Wipe color across the strip, one pixel at a time."""
    timeout_start = time.time()
    while time.time() < timeout_start + RUN_TIME:
        for color in colors:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, COLOR_CODES[color])
                strip.show()
                time.sleep(50/1000.0)

def theater_chase(strip, colors):
    """Movie theater light style chaser animation."""
    timeout_start = time.time()
    while time.time() < timeout_start + RUN_TIME:
        for color in colors:
            for j in range(10):
                for q in range(3):
                    for i in range(0, strip.numPixels(), 3):
                        strip.setPixelColor(i+q, COLOR_CODES[color])
                    strip.show()
                    time.sleep(50/1000.0)
                    for i in range(0, strip.numPixels(), 3):
                        strip.setPixelColor(i+q, 0)

conn = sqlite3.connect("color_app.db")

while True:
    with conn:
        c = conn.cursor()
        c.execute(
            "SELECT * FROM actions WHERE processed = 0 ORDER BY added ASC LIMIT 1;"
        )
        result = c.fetchone()
        if result:
            print "new record: ", result
            c.execute("UPDATE actions SET processing = 1 WHERE id = ?", (result[0],))
            conn.commit()
            print "processing..."
            time.sleep(10)
            c.execute(
                "UPDATE actions SET processing = 0, processed = 1 WHERE id = ?",
                (result[0],)
            )
            conn.commit()
        else:
            # revert to default here
            print "nothing found...waiting"
            time.sleep(10)