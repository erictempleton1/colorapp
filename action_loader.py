#from neopixel import *

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

# action dispatcher
ACTIONS = {
    "color_wipe": color_wipe,
    "theater": theater_chase
}

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(
    LED_COUNT, 
    LED_PIN, 
    LED_FREQ_HZ, 
    LED_DMA, 
    LED_INVERT, 
    LED_BRIGHTNESS, 
    LED_CHANNEL, 
    LED_STRIP
)
# Intialize the library (must be called once before other functions).
strip.begin()

conn = sqlite3.connect("color_app.db")

while True:
    with conn:
        c = conn.cursor()
        c.execute(
            "SELECT * FROM actions WHERE processed = 0 ORDER BY added ASC LIMIT 1;"
        )
        action = c.fetchone()
        if action:
            c.execute(
                "SELECT value FROM colors WHERE action_id = ?", (action[0],)
            )
            colors = [color[0] for color in c.fetchall()]

            print "action:", action[1], "|", "colors:", colors
            ACTIONS[action](strip, colors)

            c.execute("UPDATE actions SET processing = 1 WHERE id = ?", (action[0],))
            conn.commit()
            c.execute(
                "UPDATE actions SET processing = 0, processed = 1 WHERE id = ?",
                (action[0],)
            )
            conn.commit()
        else:
            # revert to default and wait for update
            colors = ["green", "red", "white"]
            print "nothing found...waiting"
            ACTIONS["color_wipe"](strip, colors)
            ACTIONS["theater"](strip, colors)
