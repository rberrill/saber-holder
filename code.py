"""
File Name: code.py
Description: A program to control an LED strip using an RP2040 SEEED chip.
             The program smoothly cycles the LED colors between two colors.
Author: Richard Berrill
Date Created: September 3, 2023
Last Modified: September 5, 2023
Version: 0.1.2
License: Creative Commons Attribution 4.0 International License (CC BY 4.0)
         For full license details, please refer to the LICENSE file or visit:
         https://creativecommons.org/licenses/by/4.0/
Contact: rberrill@gmail.com
Dependencies: Adafruit_NeoPixel library
"""

import board
import neopixel
import time
import random

# Constants
PIN = board.D0
NUMPIXELS = 13
DEBUG = False  # Set to True for debug messages, False to disable

# Constants for saber_flash
FLASH_COLOR = (240, 255, 0, .5)  # Yellow color
SABER_FLASH_ENABLED = True
SABER_FLASH_CHANCE = 2  # saber flash chance out of 1000
MIN_FLASHES = 4  # Minimum number of flashes
MAX_FLASHES = 10  # Maximum number of flashes
MIN_FLASH_DELAY = 0.0001  # Min delay between flashes (seconds)
MAX_FLASH_DELAY = 0.005  # Max delay between flashes (seconds)
MIN_FLASH_SPREAD = 3  # Minimum number of LEDs the flash will spread to
MAX_FLASH_SPREAD = NUMPIXELS  # Maximum number of LEDs the flash will spread to

# NEOPIXEL setup
strip = neopixel.NeoPixel(PIN, NUMPIXELS, brightness=1.0, auto_write=False)

# Shimmer colors
shimmerColor1 = (0, 149, 255, 0.8)
shimmerColor2 = (0, 174, 255, 0.6)

# Pixel order from left to right
pixelOrder = [9, 10, 8, 11, 7, 12, 6, 5, 0, 4, 1, 3, 2]

# Initialize current and target colors for each pixel
currentColors = [shimmerColor1 for _ in range(NUMPIXELS)]
targetColors = [random.choice([shimmerColor1, shimmerColor2]) for _ in range(NUMPIXELS)]

# Initialize step sizes for each pixel
stepSizes = [random.uniform(0.01, 0.1) for _ in range(NUMPIXELS)]  # Random step sizes between 0.01 and 0.1

def debugPrint(message):
    if DEBUG:
        print(message)

def adjustColor(current, target, step):
    """Adjust the current color towards the target color by a given step."""
    return tuple(current[i] + step * (target[i] - current[i]) for i in range(3))

def displayShimmer():
    if SABER_FLASH_ENABLED and random.randint(1, 1000) <= SABER_FLASH_CHANCE:
        saber_flash()
    else:
        for k in range(NUMPIXELS):
            r, g, b = adjustColor(currentColors[k][:3], targetColors[k][:3], stepSizes[k])
            brightness = targetColors[k][3]
            strip[pixelOrder[k]] = (int(r * brightness), int(g * brightness), int(b * brightness))
            debugPrint(f"LED {pixelOrder[k]} shimmering with color (R: {int(r)}, G: {int(g)}, B: {int(b)}) and brightness {brightness}")

            if all(abs(currentColors[k][i] - targetColors[k][i]) < 1 for i in range(3)):
                targetColors[k] = random.choice([shimmerColor1, shimmerColor2])
                stepSizes[k] = random.uniform(0.001, 0.005)
            currentColors[k] = (r, g, b, brightness)

def set_led_color(led_index, color):
    """Set the color of a specific LED."""
    if 0 <= led_index < NUMPIXELS:
        r, g, b, brightness = color
        strip[pixelOrder[led_index]] = (int(r * brightness), int(g * brightness), int(b * brightness))
        strip.show()

def flash_leds(start_led, flash_spread, color):
    """Illuminate the LEDs based on the starting LED and flash spread."""
    for step in range(-flash_spread, flash_spread + 1):
        set_led_color(start_led + step, color)

def saber_flash():
    start_led = random.randint(0, NUMPIXELS - 1)
    num_flashes = random.randint(MIN_FLASHES, MAX_FLASHES)

    for _ in range(num_flashes):
        flash_spread = random.randint(MIN_FLASH_SPREAD, MAX_FLASH_SPREAD)
        flash_leds(start_led, flash_spread, FLASH_COLOR)
        time.sleep(random.uniform(MIN_FLASH_DELAY, MAX_FLASH_DELAY))
        flash_leds(start_led, flash_spread, (0, 0, 0, 1))
        time.sleep(random.uniform(MIN_FLASH_DELAY, MAX_FLASH_DELAY))

while True:
    displayShimmer()
    strip.show()
